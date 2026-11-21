"""Automatic PDF ingestion + key figure/chart cropping into raw/assets/<slug>/ and wiki/."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import List, Tuple

from llm_client import GeminiStructuredClient
from schemas import FigureCropSpec, PaperIngestOutput

INGEST_SYSTEM_PROMPT = """你是嚴謹的學術論文 LLM Wiki 維護與圖表定位專家，嚴格遵守以下規範：
1. 全文以繁體中文撰寫，專有名詞首次出現保留英文原文，文內引用與參考文獻統一採 APA 7th 英文格式。
2. 所有內部連結一律使用標準相對路徑 Markdown 連結（例如 `../concepts/slug.md`），嚴禁使用 `[[Wikilink]]`。
3. 忠實保留原始統計數值並整理成 Markdown 表格，原文未報告者明寫「原文未報告」。
4. 仔細掃描整份 PDF 的每一頁，找出值得嵌入簡報的「關鍵統計圖表、實驗裝置圖、模型示意圖或量表原圖」（最多 8 張），在 `figures` 欄位提供精準的 PDF 頁碼（1-indexed）與 0–1000 正規化裁切座標（ymin, xmin, ymax, xmax），只框選圖形本體（不含過長文字圖說）。
5. 所有 slug 與圖片檔名一律使用全小寫英數字與連字號（-）。
"""


def _sanitize_slug(raw: str) -> str:
    s = re.sub(r"[^a-z0-9-]+", "-", (raw or "").lower()).strip("-")
    return s or "untitled-paper"


def _sanitize_img_name(raw: str, idx: int) -> str:
    stem = Path(raw or f"fig-{idx}").stem
    clean = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-") or f"fig-{idx}"
    return f"{clean}.png"


def _yaml_list(items: List[str]) -> str:
    if not items:
        return "[]"
    return "\n" + "\n".join(f'  - "{str(x).replace(chr(34), chr(39))}"' for x in items)


def crop_figures_from_pdf(
    pdf_path: Path,
    figures: List[FigureCropSpec],
    assets_dir: Path,
    repo_root: Path,
) -> List[Tuple[str, str]]:
    """Render specified PDF pages and crop figure bounding boxes into assets_dir."""
    if not figures:
        return []
    import pypdfium2 as pdfium

    assets_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    num_pages = len(pdf)
    saved: List[Tuple[str, str]] = []

    try:
        for idx, fig in enumerate(figures, start=1):
            pno = fig.page_number
            if pno < 1 or pno > num_pages:
                continue
            ymin, xmin, ymax, xmax = fig.ymin, fig.xmin, fig.ymax, fig.xmax
            if ymax <= ymin + 20 or xmax <= xmin + 20:
                continue

            page = pdf[pno - 1]
            img = page.render(scale=2.5).to_pil()
            w, h = img.size

            # Add 1.5% safety margin so edges are never clipped
            pad_x = int(w * 0.015)
            pad_y = int(h * 0.015)
            left = max(0, int(w * (xmin / 1000.0)) - pad_x)
            top = max(0, int(h * (ymin / 1000.0)) - pad_y)
            right = min(w, int(w * (xmax / 1000.0)) + pad_x)
            bottom = min(h, int(h * (ymax / 1000.0)) + pad_y)

            crop = img.crop((left, top, right, bottom))
            fname = _sanitize_img_name(fig.filename, idx)
            out_file = assets_dir / fname
            crop.save(out_file)
            rel = str(out_file.relative_to(repo_root)).replace("\\", "/")
            saved.append((rel, fig.caption))
            print(f"[Figure] 已自動擷取第 {pno} 頁圖表 -> {rel} ({crop.size[0]}x{crop.size[1]})", flush=True)
    finally:
        pdf.close()

    return saved


def already_ingested_map(repo_root: Path) -> dict[str, str]:
    """Return mapping of raw PDF filename -> paper slug already in wiki/papers/."""
    found: dict[str, str] = {}
    papers_dir = repo_root / "wiki" / "papers"
    if not papers_dir.exists():
        return found
    for md in papers_dir.glob("*.md"):
        if md.name == "_index.md":
            continue
        m = re.search(
            r"^source_file:\s*[\x22\x27]?([^\x22\x27\n]+)[\x22\x27]?",
            md.read_text(encoding="utf-8", errors="ignore"),
            flags=re.MULTILINE,
        )
        if m:
            found[m.group(1).strip()] = md.stem
    return found


def _load_existing_indexes(repo_root: Path) -> str:
    parts = []
    for rel in ("wiki/papers/_index.md", "wiki/concepts/_index.md", "wiki/methods/_index.md"):
        p = repo_root / rel
        if p.exists():
            parts.append(f"=== {rel} ===\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def _append_table_row(index_path: Path, slug_link: str, row_md: str) -> None:
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8")
    if slug_link in text:
        return
    m = re.search(r"^count:\s*(\d+)", text, flags=re.MULTILINE)
    if m:
        text = re.sub(
            r"^count:\s*\d+", f"count: {int(m.group(1)) + 1}", text, count=1, flags=re.MULTILINE
        )
    today = dt.date.today().isoformat()
    text = re.sub(r"^updated_at:\s*.*$", f"updated_at: {today}", text, count=1, flags=re.MULTILINE)
    index_path.write_text(text.rstrip() + "\n" + row_md + "\n", encoding="utf-8")


def _sync_top_index(repo_root: Path) -> None:
    wiki = repo_root / "wiki"
    counts = {
        k: len([p for p in (wiki / k).glob("*.md") if p.name != "_index.md"])
        for k in ("papers", "concepts", "methods", "synthesis")
    }
    today = dt.date.today().isoformat()
    (wiki / "index.md").write_text(
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


def ingest_pdf_with_figures(
    repo_root: Path,
    pdf_path: Path,
    client: GeminiStructuredClient,
) -> Tuple[List[str], List[str]]:
    """Ingest a PDF into wiki/ AND crop its key figures into raw/assets/<slug>/."""
    print(f"[Ingest] 開始解析 PDF 並偵測關鍵圖表：{pdf_path.name}", flush=True)
    existing_idx = _load_existing_indexes(repo_root)
    prompt = f"""請完整閱讀這份原始論文 PDF（原檔名：{pdf_path.name}），完成兩項任務：
1. 產出符合 AGENTS.md 的結構化論文 Wiki 頁、統計數據 Markdown 表格與關聯構念／方法頁。
2. 標出 PDF 中所有具教學或口報價值的關鍵圖表（如統計圖、理論模型圖、實驗裝置圖、量表原圖），於 `figures` 欄位填寫精準頁碼與 0–1000 裁切座標。

目前知識庫既有索引：
{existing_idx}
"""
    data = client.generate_structured(
        INGEST_SYSTEM_PROMPT,
        prompt,
        PaperIngestOutput,
        temperature=0.2,
        pdf_bytes=pdf_path.read_bytes(),
    )

    today = dt.date.today().isoformat()
    slug = _sanitize_slug(data.slug)
    wiki = repo_root / "wiki"
    assets_dir = repo_root / "raw" / "assets" / slug

    # 1. Crop figures automatically
    cropped = crop_figures_from_pdf(pdf_path, data.figures, assets_dir, repo_root)
    fig_section = ""
    if cropped:
        lines = ["\n## 自動擷取之關鍵圖表"]
        for rel_path, caption in cropped:
            rel_from_paper = f"../../{rel_path}"
            lines.append(f"\n### {caption}\n![{caption}]({rel_from_paper})")
        fig_section = "\n".join(lines) + "\n"

    # 2. Write wiki/papers/<slug>.md
    written: List[str] = []
    paper_file = wiki / "papers" / f"{slug}.md"
    paper_file.write_text(
        f"""---
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
status: reviewed
tags:{_yaml_list(data.tags)}
ingested_at: {today}
updated_at: {today}
---

# {data.title}

返回 [單篇文獻索引](./_index.md) ｜ [知識庫總目錄](../index.md)

{data.paper_body_markdown}
{fig_section}
""",
        encoding="utf-8",
    )
    written.append(f"wiki/papers/{slug}.md")

    first_author = data.authors[0].split(",")[0] if data.authors else "Unknown"
    author_label = f"{first_author} et al. ({data.year})" if len(data.authors) > 1 else f"{first_author} ({data.year})"
    tags_str = ", ".join(f"`{t}`" for t in data.tags[:5])
    _append_table_row(
        wiki / "papers" / "_index.md",
        f"./{slug}.md",
        f"| [{data.title}](./{slug}.md) | {author_label} | {data.journal} | {data.sample_size} | `{data.design}` | `reviewed` | {tags_str} |",
    )

    # 3. Write new concepts & methods
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
status: reviewed
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
                f"| [{c.title}](./{c_slug}.md) | {c.english_term} | `{c.category}` | 1 | `reviewed` | {c.one_line_summary} |",
            )

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
status: reviewed
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
                f"| [{m.title}](./{m_slug}.md) | {m.english_term} | `{m.method_type}` | 1 | `reviewed` | {m.one_line_summary} |",
            )

    _sync_top_index(repo_root)
    log_path = wiki / "log.md"
    if log_path.exists():
        entry = (
            f"\n## [{today}] ingest | {author_label} {data.title}\n"
            f"- 影響檔案：{', '.join(f'`{w}`' for w in written)}；擷取圖表 {len(cropped)} 張\n"
            f"- 摘要：{data.executive_summary}\n"
        )
        log_path.write_text(log_path.read_text(encoding="utf-8").rstrip() + "\n" + entry, encoding="utf-8")

    return written, [rel for rel, _ in cropped]
