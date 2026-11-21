"""LangGraph StateGraph v3: Auto PDF Ingest & Figure Crop -> Outline (HITL 1) -> Map-Reduce Slides (HITL 2) -> HTML (HITL 3) -> Archive."""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Union

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send, interrupt

from html_builder import build_pastel_html_deck
from llm_client import GeminiStructuredClient
from pdf_ingest import already_ingested_map, ingest_pdf_with_figures
from retrieval import retrieve_wiki_context
from schemas import (
    AutoCheckResult,
    GraphState,
    OutlineSchema,
    UnitSlidesOutput,
)

MAX_RETRIES = 2

SYSTEM_WIKI_GROUNDING = """你是嚴謹的學術簡報規劃與撰寫專家，必須嚴格遵守以下鐵律：
1. 所有內容、統計數據、實驗結果與 APA 7th 引用必須 100% 來自提供的 Wiki 內容，嚴禁自行編造或混入未收錄之外部文獻。
2. 若證據不足或知識庫尚未收錄，必須於 wiki_gap_note 欄位標註 `[Wiki 缺口: 目前知識庫尚未收錄 XX]`。
3. 全文使用繁體中文，專有名詞保留英文原文，引用格式統一採 APA 7th 英文格式。
4. 講者備忘錄（speaker_notes）須為自然流暢、可直接照念的口語講稿。
5. 請積極將 `available_assets` 中與該頁主題相符的圖表路徑填入 `asset_path`（原樣複製相對路徑）。
"""


def _get_client() -> GeminiStructuredClient:
    return GeminiStructuredClient()


# ---------- Node 0a: Auto PDF Ingest & Figure Extraction ----------
def node_ingest_pdfs(state: GraphState) -> Dict[str, Any]:
    repo_root = Path(state["repo_root"])
    raw_dir = repo_root / "raw" / "papers"
    ingested_map = already_ingested_map(repo_root)
    client = _get_client()

    targets: List[Path] = []
    if state.get("pdf_path"):
        p = Path(state["pdf_path"])
        if not p.is_absolute():
            p = (repo_root / p).resolve()
        if p.exists():
            slug = ingested_map.get(p.name)
            has_assets = bool(slug and (repo_root / "raw" / "assets" / slug).exists() and any((repo_root / "raw" / "assets" / slug).glob("*.png")))
            if not slug or (state.get("force_extract_figures") and not has_assets):
                targets.append(p)
            else:
                print(f"[Ingest] {p.name} 已收錄且已有圖表，跳過重複匯入。", flush=True)
    elif state.get("auto_ingest", True) and raw_dir.exists():
        for pdf in sorted(raw_dir.glob("*.pdf")):
            if pdf.name not in ingested_map:
                targets.append(pdf)

    all_written: List[str] = []
    all_figs: List[str] = []
    for pdf in targets:
        w, f = ingest_pdf_with_figures(repo_root, pdf, client)
        all_written.extend(w)
        all_figs.extend(f)

    return {"ingested_files": all_written, "extracted_figures": all_figs}


# ---------- Node 0b: Wiki 3-Tier Retrieval ----------
def node_retrieve(state: GraphState) -> Dict[str, Any]:
    repo_root = Path(state["repo_root"])
    context_pack, assets, used = retrieve_wiki_context(repo_root, state["topic"])
    print(f"[Retrieve] 已載入 {len(used)} 份 Wiki 檔案、偵測到 {len(assets)} 張可用圖表。", flush=True)
    return {
        "context_pack": context_pack,
        "available_assets": assets,
        "wiki_files_used": used,
        "outline_retries": 0,
        "unit_retries": {},
        "html_retries": 0,
    }


# ---------- Node 1: Outline ----------
def node_outline(state: GraphState) -> Dict[str, Any]:
    client = _get_client()
    feedback = state.get("outline_feedback", "")
    prev_issues = (state.get("outline_check") or {}).get("issues", [])
    prompt = f"""請根據以下 Wiki 內容，規劃一份學術口頭報告的結構化大綱：
- 主題：{state['topic']}
- 目標頁數：約 {state.get('target_slides', 20)} 頁
- 目標時長：約 {state.get('target_minutes', 25)} 分鐘
- 視覺風格：{state.get('style', '日式可愛粉彩風')}
- 可用圖片清單（raw/assets，請優先分配到合適頁面）：{json.dumps(state.get('available_assets', []), ensure_ascii=False)}
- 前次檢核問題：{json.dumps(prev_issues, ensure_ascii=False)}
- 使用者修改意見：{feedback or '無'}

Wiki 內容：
{state['context_pack']}
"""
    outline = client.generate_structured(
        SYSTEM_WIKI_GROUNDING, prompt, OutlineSchema, temperature=0.25
    )
    return {
        "outline": outline.model_dump(),
        "outline_retries": state.get("outline_retries", 0) + 1,
    }


def auto_check_outline(state: GraphState) -> Dict[str, Any]:
    outline = state.get("outline") or {}
    issues: List[str] = []
    units = outline.get("units", [])
    total_slides = sum(len(u.get("slides", [])) for u in units)
    target = state.get("target_slides", 20)
    if total_slides < max(5, target - 4) or total_slides > target + 4:
        issues.append(f"總頁數 {total_slides} 偏離目標 {target} 頁過多")
    avail = set(state.get("available_assets", []))
    for u in units:
        for sl in u.get("slides", []):
            ap = sl.get("planned_asset")
            if ap and ap not in avail:
                issues.append(f"P.{sl.get('slide_no')} 指定圖片不存在：{ap}")
    check = AutoCheckResult(passed=len(issues) == 0, issues=issues)
    return {"outline_check": check.model_dump()}


def route_after_outline_check(state: GraphState) -> Literal["node_outline", "hitl_outline"]:
    check = state.get("outline_check") or {}
    if not check.get("passed") and state.get("outline_retries", 0) <= MAX_RETRIES:
        return "node_outline"
    return "hitl_outline"


def hitl_outline(state: GraphState) -> Dict[str, Any]:
    decision = interrupt(
        {
            "gate": "HITL_1_OUTLINE",
            "message": "請確認大綱結構。滿意請執行 resume --approve；想調整請執行 resume --feedback '修改意見'。",
            "extracted_figures": state.get("extracted_figures", []),
            "outline": state.get("outline"),
            "auto_check": state.get("outline_check"),
        }
    )
    if isinstance(decision, dict) and decision.get("approved"):
        return {"outline_feedback": ""}
    fb = decision.get("feedback", "請調整大綱架構") if isinstance(decision, dict) else str(decision)
    return {"outline_feedback": fb, "outline_retries": 0}


def fan_out_units(state: GraphState) -> Union[str, List[Send]]:
    if state.get("outline_feedback"):
        return "node_outline"
    units = (state.get("outline") or {}).get("units", [])
    return [
        Send(
            "unit_writer",
            {
                "unit": u,
                "context_pack": state["context_pack"],
                "available_assets": state.get("available_assets", []),
                "style": state.get("style", "日式可愛粉彩風"),
                "feedback": state.get("content_feedback", ""),
            },
        )
        for u in units
    ]


# ---------- Stage 2: Map-Reduce Parallel Unit Writer ----------
def unit_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = _get_client()
    unit = payload["unit"]
    prompt = f"""請為以下單元撰寫每一頁的完整投影片規格（含結論式標題、精簡要點、表格、圖片配對、粉彩貼紙、可直接照念的繁體中文口語講稿、頁尾 APA 7th 出處）：
單元大綱：{json.dumps(unit, ensure_ascii=False)}
可用圖片：{json.dumps(payload.get('available_assets', []), ensure_ascii=False)}
風格：{payload.get('style', '日式可愛粉彩風')}
修改提示：{payload.get('feedback', '無')}

Wiki 內容：
{payload['context_pack']}
"""
    result = client.generate_structured(
        SYSTEM_WIKI_GROUNDING, prompt, UnitSlidesOutput, temperature=0.3
    )
    return {"unit_slides": {result.unit_id: [s.model_dump() for s in result.slides]}}


def node_reduce_and_check(state: GraphState) -> Dict[str, Any]:
    repo_root = Path(state["repo_root"])
    unit_map = state.get("unit_slides") or {}
    outline_units = (state.get("outline") or {}).get("units", [])
    retries = dict(state.get("unit_retries") or {})

    merged: List[Dict[str, Any]] = []
    failed_units: List[str] = []
    flagged_slides: List[int] = []
    issues: List[str] = []

    for u in outline_units:
        uid = u["unit_id"]
        slides = unit_map.get(uid, [])
        if not slides:
            failed_units.append(uid)
            issues.append(f"單元 {uid} 缺少投影片產出")
            continue

        unit_has_error = False
        for sl in slides:
            no = sl.get("slide_no", 0)
            ap = sl.get("asset_path")
            if ap and not (repo_root / ap).exists():
                unit_has_error = True
                issues.append(f"P.{no} ({uid}) 圖片路徑不存在：{ap}")
            if len(sl.get("bullets", [])) > 6:
                unit_has_error = True
                issues.append(f"P.{no} ({uid}) 要點超過 6 條")
            if not (sl.get("apa_citation") or "").strip():
                unit_has_error = True
                issues.append(f"P.{no} ({uid}) 缺少頁尾 APA 7th 出處")
            if sl.get("wiki_gap_note") or sl.get("is_key_slide") or sl.get("flag_reason"):
                flagged_slides.append(no)
            merged.append(sl)

        if unit_has_error:
            retries[uid] = retries.get(uid, 0) + 1
            if retries[uid] <= MAX_RETRIES:
                failed_units.append(uid)
            else:
                for sl in slides:
                    flagged_slides.append(sl.get("slide_no", 0))

    merged.sort(key=lambda s: s.get("slide_no", 0))
    flagged_slides = sorted(set(flagged_slides))
    check = AutoCheckResult(
        passed=len(failed_units) == 0 and len(issues) == 0,
        issues=issues,
        failed_unit_ids=failed_units,
        flagged_slide_nos=flagged_slides,
    )
    return {
        "merged_slides": merged,
        "unit_retries": retries,
        "failed_unit_ids": failed_units,
        "flagged_slide_nos": flagged_slides,
        "content_check": check.model_dump(),
    }


def route_after_reduce(state: GraphState) -> Union[str, List[Send]]:
    failed = state.get("failed_unit_ids") or []
    if failed:
        outline_units = {u["unit_id"]: u for u in (state.get("outline") or {}).get("units", [])}
        return [
            Send(
                "unit_writer",
                {
                    "unit": outline_units[uid],
                    "context_pack": state["context_pack"],
                    "available_assets": state.get("available_assets", []),
                    "style": state.get("style", "日式可愛粉彩風"),
                    "feedback": "; ".join((state.get("content_check") or {}).get("issues", [])),
                },
            )
            for uid in failed
            if uid in outline_units
        ]
    if state.get("flagged_slide_nos"):
        return "hitl_flagged_slides"
    return "node_build_html"


def hitl_flagged_slides(state: GraphState) -> Dict[str, Any]:
    flagged_nos = set(state.get("flagged_slide_nos") or [])
    flagged_payload = [s for s in state.get("merged_slides", []) if s.get("slide_no") in flagged_nos]
    decision = interrupt(
        {
            "gate": "HITL_2_FLAGGED_SLIDES",
            "message": "以下為標記之重點頁／含 Wiki 缺口頁，請確認。放行請執行 resume --approve。",
            "flagged_slides": flagged_payload,
            "content_check": state.get("content_check"),
        }
    )
    if isinstance(decision, dict) and decision.get("approved"):
        return {"failed_unit_ids": [], "flagged_slide_nos": [], "content_feedback": ""}
    retry_units = decision.get("retry_units", []) if isinstance(decision, dict) else []
    fb = decision.get("feedback", "") if isinstance(decision, dict) else str(decision)
    return {"failed_unit_ids": retry_units, "content_feedback": fb}


def route_after_hitl2(state: GraphState) -> Union[str, List[Send]]:
    retry_units = state.get("failed_unit_ids") or []
    if retry_units:
        outline_units = {u["unit_id"]: u for u in (state.get("outline") or {}).get("units", [])}
        return [
            Send(
                "unit_writer",
                {
                    "unit": outline_units[uid],
                    "context_pack": state["context_pack"],
                    "available_assets": state.get("available_assets", []),
                    "style": state.get("style", "日式可愛粉彩風"),
                    "feedback": state.get("content_feedback", ""),
                },
            )
            for uid in retry_units
            if uid in outline_units
        ]
    return "node_build_html"


# ---------- Stage 3: HTML Build & Fixed Verification ----------
def node_build_html(state: GraphState) -> Dict[str, Any]:
    repo_root = Path(state["repo_root"])
    slug = state.get("slug", "presentation")
    out_html = repo_root / "outputs" / "slides-html" / f"{slug}-slides.html"
    deck_meta = {
        "deck_title": (state.get("outline") or {}).get("deck_title", state["topic"]),
        "presenter": state.get("presenter", ""),
        "course": state.get("course", ""),
        "date": state.get("date", dt.date.today().strftime("%Y/%m/%d")),
    }
    build_pastel_html_deck(repo_root, deck_meta, state.get("merged_slides", []), out_html)
    return {
        "html_output_path": str(out_html),
        "html_retries": state.get("html_retries", 0) + 1,
    }


def auto_check_html(state: GraphState) -> Dict[str, Any]:
    html_path = Path(state["html_output_path"])
    issues: List[str] = []
    if not html_path.exists():
        issues.append("HTML 檔案尚未產生")
    else:
        txt = html_path.read_text(encoding="utf-8")
        if "raw/assets/" in txt:
            issues.append("偵測到未轉為 Base64 之本地圖片路徑")
        if "@media print" not in txt:
            issues.append("缺少 @media print 列印分頁樣式")
        # Fixed regex: only count actual <section class="slide ..."> elements!
        slide_count = len(re.findall(r'<section class="slide\s', txt))
        expected = len(state.get("merged_slides", []))
        if slide_count != expected:
            issues.append(f"HTML 投影片數 ({slide_count}) 與規格 ({expected}) 不符")
    check = AutoCheckResult(passed=len(issues) == 0, issues=issues)
    return {"html_check": check.model_dump()}


def route_after_html_check(state: GraphState) -> Literal["node_build_html", "hitl_final_review"]:
    check = state.get("html_check") or {}
    if not check.get("passed") and state.get("html_retries", 0) <= MAX_RETRIES:
        return "node_build_html"
    return "hitl_final_review"


def hitl_final_review(state: GraphState) -> Dict[str, Any]:
    decision = interrupt(
        {
            "gate": "HITL_3_FINAL_HTML",
            "message": f"請於瀏覽器開啟 {state.get('html_output_path')} 檢視。通過請執行 resume --action approve。",
            "html_output_path": state.get("html_output_path"),
            "html_check": state.get("html_check"),
        }
    )
    if isinstance(decision, dict):
        return {
            "final_action": decision.get("action", "approve"),
            "failed_unit_ids": decision.get("retry_units", []),
            "content_feedback": decision.get("feedback", ""),
        }
    return {"final_action": "approve"}


def route_after_final_review(state: GraphState) -> Union[str, List[Send]]:
    action = state.get("final_action", "approve")
    if action == "restyle":
        return "node_build_html"
    if action == "edit_content" and state.get("failed_unit_ids"):
        return route_after_hitl2(state)
    return "node_archive_and_log"


# ---------- Node 4: Archive & Log ----------
def node_archive_and_log(state: GraphState) -> Dict[str, Any]:
    repo_root = Path(state["repo_root"])
    log_path = repo_root / "wiki" / "log.md"
    today = dt.date.today().isoformat()
    rel_html = Path(state["html_output_path"]).relative_to(repo_root)
    entry = (
        f"\n## [{today}] slides | {state['topic']}\n"
        f"- 影響檔案：`{rel_html}`\n"
        f"- 摘要：透過 LangGraph v3 一條龍管線（自動匯入與圖表擷取＋分單元並行）產出 {len(state.get('merged_slides', []))} 頁日式可愛粉彩單檔 HTML 簡報。\n"
    )
    if log_path.exists():
        log_path.write_text(
            log_path.read_text(encoding="utf-8").rstrip() + "\n" + entry,
            encoding="utf-8",
        )
    return {}


def build_slide_graph(checkpointer=None):
    builder = StateGraph(GraphState)

    builder.add_node("node_ingest_pdfs", node_ingest_pdfs)
    builder.add_node("node_retrieve", node_retrieve)
    builder.add_node("node_outline", node_outline)
    builder.add_node("auto_check_outline", auto_check_outline)
    builder.add_node("hitl_outline", hitl_outline)
    builder.add_node("unit_writer", unit_writer)
    builder.add_node("node_reduce_and_check", node_reduce_and_check)
    builder.add_node("hitl_flagged_slides", hitl_flagged_slides)
    builder.add_node("node_build_html", node_build_html)
    builder.add_node("auto_check_html", auto_check_html)
    builder.add_node("hitl_final_review", hitl_final_review)
    builder.add_node("node_archive_and_log", node_archive_and_log)

    builder.add_edge(START, "node_ingest_pdfs")
    builder.add_edge("node_ingest_pdfs", "node_retrieve")
    builder.add_edge("node_retrieve", "node_outline")
    builder.add_edge("node_outline", "auto_check_outline")
    builder.add_conditional_edges(
        "auto_check_outline",
        route_after_outline_check,
        {"node_outline": "node_outline", "hitl_outline": "hitl_outline"},
    )
    builder.add_conditional_edges("hitl_outline", fan_out_units)
    builder.add_edge("unit_writer", "node_reduce_and_check")
    builder.add_conditional_edges("node_reduce_and_check", route_after_reduce)
    builder.add_conditional_edges("hitl_flagged_slides", route_after_hitl2)
    builder.add_edge("node_build_html", "auto_check_html")
    builder.add_conditional_edges(
        "auto_check_html",
        route_after_html_check,
        {"node_build_html": "node_build_html", "hitl_final_review": "hitl_final_review"},
    )
    builder.add_conditional_edges("hitl_final_review", route_after_final_review)
    builder.add_edge("node_archive_and_log", END)

    return builder.compile(checkpointer=checkpointer)
