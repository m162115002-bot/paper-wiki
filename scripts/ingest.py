"""
ingest.py — 學術論文 LLM Wiki 本機自動匯入腳本（Gemini API）

依循 AGENTS.md 規範，支援：
  1. 單篇精讀模式（預設）：python scripts\\ingest.py --pdf "raw\\papers\\你的論文.pdf"
  2. 批次匯入模式：        python scripts\\ingest.py --batch

共用 paper-wiki\\.venv 虛擬環境（只需已安裝 google-genai 與 pydantic，無須額外套件）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Structured Output Schemas ----------
class ConceptDraft(BaseModel):
    slug: str = Field(..., description="全小寫 ASCII slug，例如 cbt-i")
    title: str = Field(..., description="繁體中文標題")
    english_term: str = Field(..., description="英文專有名詞")
    category: str = Field(..., description="英文分類標籤，如 sleep_intervention")
    one_line_summary: str = Field(..., description="一句話繁體中文摘要")
    body_markdown: str = Field(..., description="構念頁正文 Markdown（不含 YAML Frontmatter）")


class MethodDraft(BaseModel):
    slug: str = Field(..., description="全小寫 ASCII slug，例如 isi-scale")
    title: str = Field(..., description="繁體中文標題")
    english_term: str = Field(..., description="英文全名與縮寫")
    method_type: str = Field(
        default="scale",
        description="scale / statistical_model / paradigm / biomarker",
    )
    one_line_summary: str = Field(..., description="一句話繁體中文摘要")
    body_markdown: str = Field(..., description="方法／量表頁正文 Markdown（不含 YAML Frontmatter）")


class PaperIngestOutput(BaseModel):
    slug: str = Field(..., description="firstauthor-year-short-topic 全小寫 ASCII slug")
    title: str
    authors: List[str]
    year: int
    journal: str
    doi: str = Field(default="原文未報告")
    apa_citation: str = Field(..., description="完整 APA 7th 英文參考文獻")
    sample_size: str = Field(..., description="樣本數 N，例如 N = 120 或 N/A（綜論）")
    population: str
    design: str = Field(..., description="研究設計，例如 RCT / cross_sectional / review")
    measures: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    executive_summary: str = Field(..., description="給使用者互動確認的 4–6 句繁體中文核心摘要")
    paper_body_markdown: str = Field(
        ...,
        description="符合 AGENTS.md 4.1 節之完整單篇文獻頁正文 Markdown（含統計數據 Markdown 表格、核心發現與頁碼、限制與批判評析；不含 YAML Frontmatter）",
    )
    new_concepts: List[ConceptDraft] = Field(
        default_factory=list, description="建議新建的 1–3 個核心構念頁"
    )
    new_methods: List[MethodDraft] = Field(
        default_factory=list, description="建議新建的 1–2 個方法或量表頁"
    )


SYSTEM_PROMPT = """你是嚴謹的學術論文 LLM Wiki 維護專家，嚴格遵守以下規範：
1. 全文使用繁體中文撰寫，專有名詞首次出現保留英文原文，文內引用與參考文獻統一採 APA 7th 英文格式。
2. 所有內部連結一律使用標準相對路徑 Markdown 連結（例如 `../concepts/slug.md`），嚴禁使用 `[[Wikilink]]`。
3. 忠實保留原始統計數值（N, M, SD, t, F, beta, r, d, p, 95% CI 等）並整理成 Markdown 表格，原文未報告者明寫「原文未報告」，嚴禁編造數據。
4. 清楚區分「原文陳述」與「批判評析／跨篇推論」，關鍵發現須標註原文頁碼。
5. slug 一律使用全小寫英數字與連字號（-），不得包含中文或空白。
"""


def _sanitize_slug(raw: str) -> str:
    s = re.sub(r"[^a-z0-9-]+", "-", raw.lower()).strip("-")
    return s or "untitled-paper"


def _yaml_list(items: List[str]) -> str:
    if not items:
        return "[]"
    return "\n" + "\n".join(f'  - "{str(x).replace(chr(34), chr(39))}"' for x in items)


def _call_gemini_ingest(pdf_path: Path, existing_wiki_index: str, model: str) -> PaperIngestOutput:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "找不到環境變數 GEMINI_API_KEY！請先在 PowerShell 執行：\n"
            '  $env:GEMINI_API_KEY="貼上你的API_KEY"'
        )
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    pdf_bytes = pdf_path.read_bytes()

    prompt = f"""請完整閱讀這份原始論文 PDF（原檔名：{pdf_path.name}），並輸出結構化知識庫匯入資料。

目前知識庫既有索引（供你避免重複建立已存在的概念／方法頁，並可建立正確相對路徑連結）：
{existing_wiki_index}

請確保 `paper_body_markdown` 包含以下完整區塊：
## 1. 書目資訊（APA 7th）
## 2. 研究問題與假設
## 3. 研究對象與方法
## 4. 關鍵統計數據整理（Markdown 表格）
## 5. 核心發現（原文陳述，標註頁碼）
## 6. 研究限制與批判評析（區分原文限制與批判思考）
## 7. 關聯概念與方法頁面（使用標準相對路徑連結）
"""

    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt,
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=PaperIngestOutput,
            temperature=0.2,
        ),
    )
    return PaperIngestOutput.model_validate_json(response.text)


def _load_existing_indexes(repo_root: Path) -> str:
    parts = []
    for rel in [
        "wiki/papers/_index.md",
        "wiki/concepts/_index.md",
        "wiki/methods/_index.md",
    ]:
        p = repo_root / rel
        if p.exists():
            parts.append(f"=== {rel} ===\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def _append_table_row(index_path: Path, slug_link: str, row_md: str) -> bool:
    if not index_path.exists():
        return False
    text = index_path.read_text(encoding="utf-8")
    if slug_link in text:
        return False
    # Update count in frontmatter
    m = re.search(r"^count:\s*(\d+)", text, flags=re.MULTILINE)
    if m:
        new_count = int(m.group(1)) + 1
        text = re.sub(
            r"^count:\s*\d+", f"count: {new_count}", text, count=1, flags=re.MULTILINE
        )
    today = dt.date.today().isoformat()
    text = re.sub(
        r"^updated_at:\s*.*$", f"updated_at: {today}", text, count=1, flags=re.MULTILINE
    )
    text = text.rstrip() + "\n" + row_md + "\n"
    index_path.write_text(text, encoding="utf-8")
    return True


def _sync_top_index(repo_root: Path) -> None:
    wiki = repo_root / "wiki"
    counts = {
        "papers": len([p for p in (wiki / "papers").glob("*.md") if p.name != "_index.md"]),
        "concepts": len([p for p in (wiki / "concepts").glob("*.md") if p.name != "_index.md"]),
        "methods": len([p for p in (wiki / "methods").glob("*.md") if p.name != "_index.md"]),
        "synthesis": len([p for p in (wiki / "synthesis").glob("*.md") if p.name != "_index.md"]),
    }
    today = dt.date.today().isoformat()
    idx_path = wiki / "index.md"
    idx_path.write_text(
        f"""---
title: 論文知識庫總目錄
updated_at: {today}
total_papers: {counts['papers']}
total_concepts: {counts['concepts']}
total_methods: {counts['methods']}
total_synthesis: {counts['synthesis']}
---

# 論文知識庫總目錄（Wiki Index）

本頁為知識庫頂層導覽入口。查詢或匯入文獻時，請依 [AGENTS.md](../AGENTS.md) 之三段式檢索策略，先以本地搜尋定位，再查閱下方分類索引。

## 核心導覽
- [研究領域總覽（Overview）](./overview.md)
- [操作時間軸紀錄（Log）](./log.md)

## 分類索引
| 分類 | 索引入口 | 收錄篇數 | 說明 |
| :--- | :--- | ---: | :--- |
| 單篇文獻 | [papers/_index.md](./papers/_index.md) | {counts['papers']} | 單篇論文摘要、統計數據表格、擷取圖表與批判評析 |
| 構念與理論 | [concepts/_index.md](./concepts/_index.md) | {counts['concepts']} | 跨文獻核心概念定義、理論模型與共識／分歧 |
| 方法與量表 | [methods/_index.md](./methods/_index.md) | {counts['methods']} | 常用量表、研究典範、生理指標與統計模型 |
| 綜合與缺口 | [synthesis/_index.md](./synthesis/_index.md) | {counts['synthesis']} | 跨篇比較表、矛盾結果追蹤、研究缺口與高價值查詢回存 |
""",
        encoding="utf-8",
    )


def _write_wiki_files(
    repo_root: Path,
    pdf_path: Path,
    data: PaperIngestOutput,
    status: str = "reviewed",
) -> List[str]:
    today = dt.date.today().isoformat()
    slug = _sanitize_slug(data.slug)
    wiki = repo_root / "wiki"
    written: List[str] = []

    # 1. Write paper page
    paper_file = wiki / "papers" / f"{slug}.md"
    paper_frontmatter = f"""---
title: "{data.title.replace('"', "'")}"
authors:{_yaml_list(data.authors)}
year: {data.year}
journal: "{data.journal.replace('"', "'")}"
doi: "{data.doi.replace('"', "'")}"
source_file: "{pdf_path.name}"
sample_size: "{data.sample_size.replace('"', "'")}"
population: "{data.population.replace('"', "'")}"
design: "{data.design.replace('"', "'")}"
measures:{_yaml_list(data.measures)}
status: {status}
tags:{_yaml_list(data.tags)}
ingested_at: {today}
updated_at: {today}
---

# {data.title}

返回 [單篇文獻索引](./_index.md) ｜ [知識庫總目錄](../index.md)

{data.paper_body_markdown}
"""
    paper_file.write_text(paper_frontmatter, encoding="utf-8")
    written.append(f"wiki/papers/{slug}.md")

    first_author = data.authors[0].split(",")[0] if data.authors else "Unknown"
    author_label = f"{first_author} et al. ({data.year})" if len(data.authors) > 1 else f"{first_author} ({data.year})"
    tags_str = ", ".join(f"`{t}`" for t in data.tags[:5])
    _append_table_row(
        wiki / "papers" / "_index.md",
        f"./{slug}.md",
        f"| [{data.title}](./{slug}.md) | {author_label} | {data.journal} | {data.sample_size} | `{data.design}` | `{status}` | {tags_str} |",
    )

    # 2. Write new concept pages (only if not already existing)
    for c in data.new_concepts:
        c_slug = _sanitize_slug(c.slug)
        c_file = wiki / "concepts" / f"{c_slug}.md"
        if not c_file.exists():
            c_file.write_text(
                f"""---
title: "{c.title.replace('"', "'")}"
english_term: "{c.english_term.replace('"', "'")}"
category: "{c.category}"
related_papers_count: 1
status: {status}
tags:{_yaml_list(data.tags[:4])}
updated_at: {today}
---

# {c.title}（{c.english_term}）

返回 [構念與理論索引](./_index.md) ｜ [知識庫總目錄](../index.md)

{c.body_markdown}

## 收錄文獻
- [{author_label}](../papers/{slug}.md)
""",
                encoding="utf-8",
            )
            written.append(f"wiki/concepts/{c_slug}.md")
            _append_table_row(
                wiki / "concepts" / "_index.md",
                f"./{c_slug}.md",
                f"| [{c.title}](./{c_slug}.md) | {c.english_term} | `{c.category}` | 1 | `{status}` | {c.one_line_summary} |",
            )

    # 3. Write new method pages (only if not already existing)
    for m in data.new_methods:
        m_slug = _sanitize_slug(m.slug)
        m_file = wiki / "methods" / f"{m_slug}.md"
        if not m_file.exists():
            m_file.write_text(
                f"""---
title: "{m.title.replace('"', "'")}"
english_term: "{m.english_term.replace('"', "'")}"
method_type: "{m.method_type}"
related_papers_count: 1
status: {status}
tags:{_yaml_list(data.tags[:4])}
updated_at: {today}
---

# {m.title}（{m.english_term}）

返回 [方法與量表索引](./_index.md) ｜ [知識庫總目錄](../index.md)

{m.body_markdown}

## 使用本工具之收錄文獻
- [{author_label}](../papers/{slug}.md)
""",
                encoding="utf-8",
            )
            written.append(f"wiki/methods/{m_slug}.md")
            _append_table_row(
                wiki / "methods" / "_index.md",
                f"./{m_slug}.md",
                f"| [{m.title}](./{m_slug}.md) | {m.english_term} | `{m.method_type}` | 1 | `{status}` | {m.one_line_summary} |",
            )

    # 4. Sync top index & append log.md
    _sync_top_index(repo_root)
    log_path = wiki / "log.md"
    op = "ingest" if status == "reviewed" else "batch-ingest"
    log_entry = (
        f"\n## [{today}] {op} | {author_label} {data.title}\n"
        f"- 影響檔案：{', '.join(f'`{w}`' for w in written)}\n"
        f"- 摘要：{data.executive_summary}\n"
    )
    if log_path.exists():
        log_path.write_text(
            log_path.read_text(encoding="utf-8").rstrip() + "\n" + log_entry,
            encoding="utf-8",
        )
    return written


def _already_ingested_sources(repo_root: Path) -> set[str]:
    found: set[str] = set()
    papers_dir = repo_root / "wiki" / "papers"
    if not papers_dir.exists():
        return found
    for md in papers_dir.glob("*.md"):
        if md.name == "_index.md":
            continue
        m = re.search(r'^source_file:\s*["\']?([^"\'\n]+)["\']?', md.read_text(encoding="utf-8"), flags=re.MULTILINE)
        if m:
            found.add(m.group(1).strip())
    return found


def ingest_single(repo_root: Path, pdf_path: Path, model: str, auto_yes: bool, status: str = "reviewed") -> None:
    if not pdf_path.exists():
        print(f"[錯誤] 找不到 PDF 檔案：{pdf_path}")
        sys.exit(1)

    print(f"[1/4] 讀取原始 PDF：{pdf_path.name}")
    existing_idx = _load_existing_indexes(repo_root)

    print(f"[2/4] 呼叫 Gemini API（模型：{model}）解析論文內容，請稍候...")
    data = _call_gemini_ingest(pdf_path, existing_idx, model)

    print("\n================ 論文摘要預覽 ================")
    print(f"標題：{data.title}")
    print(f"APA：{data.apa_citation}")
    print(f"Slug：{data.slug}")
    print(f"摘要：{data.executive_summary}")
    print(f"預計新建構念頁：{len(data.new_concepts)} 頁 ｜ 方法頁：{len(data.new_methods)} 頁")
    print("=============================================\n")

    if not auto_yes:
        ans = input("確認寫入 Wiki 並更新索引嗎？[Y/n]：").strip().lower()
        if ans not in ("", "y", "yes"):
            print("已取消寫入。")
            return

    print("[3/4] 寫入 Wiki 頁面中...")
    written = _write_wiki_files(repo_root, pdf_path, data, status=status)

    print("[4/4] 完成！已新增／更新以下檔案：")
    for w in written:
        print(f"  - {w}")
    print("  - wiki/index.md & 各分類 _index.md & wiki/log.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="論文 PDF 自動匯入 LLM Wiki 工具")
    parser.add_argument("--pdf", help="單篇精讀模式：指定 raw/papers/ 內的 PDF 路徑")
    parser.add_argument("--batch", action="store_true", help="批次匯入模式：自動匯入 raw/papers/ 中尚未收錄的所有 PDF")
    parser.add_argument("--yes", "-y", action="store_true", help="跳過互動確認直接寫入")
    parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        help="Gemini 模型名稱（預設讀取 GEMINI_MODEL 或使用 gemini-3.5-flash-lite）",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    if args.batch:
        raw_dir = repo_root / "raw" / "papers"
        ingested = _already_ingested_sources(repo_root)
        pending = [p for p in sorted(raw_dir.glob("*.pdf")) if p.name not in ingested]
        if not pending:
            print("raw/papers/ 中所有 PDF 皆已收錄，沒有待匯入的新檔案！")
            return
        print(f"偵測到 {len(pending)} 篇未收錄 PDF，開始批次匯入（status: draft）：")
        for idx, pdf in enumerate(pending, start=1):
            print(f"\n--- 批次進度 {idx}/{len(pending)} ---")
            ingest_single(repo_root, pdf, args.model, auto_yes=True, status="draft")
        print("\n批次匯入全部完成！")
        return

    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.is_absolute():
            pdf_path = (repo_root / pdf_path).resolve()
        ingest_single(repo_root, pdf_path, args.model, auto_yes=args.yes, status="reviewed")
        return

    parser.print_help()


if __name__ == "__main__":
    main()