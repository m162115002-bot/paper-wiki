"""CLI runner for Slide Graph v3 (One-stop PDF Ingest + Figure Crop + Map-Reduce HTML Slides)."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from ch11_demo_data import CH11_META, CH11_SLIDES
from html_builder import build_pastel_html_deck


def run_demo_ch11(repo_root: Path) -> None:
    out = repo_root / "outputs" / "slides-html" / "ch11-nature-symptoms-of-pain-slides.html"
    build_pastel_html_deck(repo_root, CH11_META, CH11_SLIDES, out)
    print(f"[DEMO OK] 已離線生成第 11 章日式可愛粉彩 HTML 簡報：{out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Slide Graph v3 (PDF 自動匯入＋擷圖＋LangGraph 簡報一條龍)")
    parser.add_argument("--demo-ch11", action="store_true", help="離線生成第 11 章示範 HTML")
    sub = parser.add_subparsers(dest="cmd")

    p_start = sub.add_parser("start", help="從 PDF 自動匯入、擷圖並產出大綱（於 HITL 1 暫停）")
    p_start.add_argument("--pdf", default=None, help="選填：指定 raw/papers/ 內的單一 PDF；省略則自動掃描所有尚未匯入的 PDF")
    p_start.add_argument("--force-extract-figures", action="store_true", help="若 PDF 已在 Wiki 但尚無圖表，強制補擷取圖表")
    p_start.add_argument("--topic", required=True)
    p_start.add_argument("--presenter", default="黃少杰")
    p_start.add_argument("--course", default="健康心理學")
    p_start.add_argument("--date", default="2026/11/21")
    p_start.add_argument("--duration", type=int, default=25)
    p_start.add_argument("--slides", type=int, default=20)
    p_start.add_argument("--slug", default="presentation")
    p_start.add_argument("--thread-id", required=True)

    p_resume = sub.add_parser("resume", help="從人工關卡續跑")
    p_resume.add_argument("--thread-id", required=True)
    p_resume.add_argument("--approve", action="store_true")
    p_resume.add_argument("--feedback", default="")
    p_resume.add_argument("--retry-units", nargs="*", default=[])
    p_resume.add_argument("--action", default="approve", choices=["approve", "restyle", "edit_content"])

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]

    if args.demo_ch11:
        run_demo_ch11(repo_root)
        return

    if not args.cmd:
        parser.print_help()
        return

    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.types import Command
    from graph import build_slide_graph

    db_path = Path(__file__).resolve().parent / ".checkpoints.db"
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    app = build_slide_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": args.thread_id}}

    if args.cmd == "start":
        initial_state = {
            "repo_root": str(repo_root),
            "pdf_path": args.pdf,
            "auto_ingest": True,
            "force_extract_figures": args.force_extract_figures,
            "topic": args.topic,
            "presenter": args.presenter,
            "course": args.course,
            "date": args.date,
            "style": "日式可愛粉彩風",
            "target_minutes": args.duration,
            "target_slides": args.slides,
            "slug": args.slug,
        }
        result = app.invoke(initial_state, config=config)
        print(json.dumps(result.get("__interrupt__", result), ensure_ascii=False, indent=2, default=str))
    elif args.cmd == "resume":
        payload = {
            "approved": args.approve,
            "feedback": args.feedback,
            "retry_units": args.retry_units,
            "action": args.action,
        }
        result = app.invoke(Command(resume=payload), config=config)
        print(
            json.dumps(
                result.get("__interrupt__", {"status": "done", "html": result.get("html_output_path")}),
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )


if __name__ == "__main__":
    main()
