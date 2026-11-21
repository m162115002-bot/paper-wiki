"""Single-file portable Japanese Cute Pastel HTML slide builder."""
from __future__ import annotations

import base64
import html
import json
import mimetypes
from pathlib import Path
from typing import Any, Dict, List

# 10 adorable original Japanese pastel SVG stickers
STICKERS: Dict[str, str] = {
    "brain": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <ellipse cx="48" cy="52" rx="34" ry="27" fill="#FADCE4" stroke="#7A545D" stroke-width="2.6"/>
      <path d="M25 46 C20 34, 34 23, 46 28 C54 20, 72 25, 72 40 C79 44, 78 60, 68 65 C65 75, 50 76, 46 70 C36 76, 22 70, 22 57 C16 54, 17 45, 25 46 Z" fill="#FDE8EE" stroke="#7A545D" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M47 28 C47 38, 49 48, 47 68" stroke="#E8A5B8" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <circle cx="36" cy="50" r="3" fill="#4A3B36"/><circle cx="58" cy="50" r="3" fill="#4A3B36"/>
      <ellipse cx="31" cy="55" rx="4.2" ry="2.5" fill="#F6A6BC" opacity="0.8"/>
      <ellipse cx="63" cy="55" rx="4.2" ry="2.5" fill="#F6A6BC" opacity="0.8"/>
      <path d="M43 54 Q47 59 51 54" stroke="#4A3B36" stroke-width="2.3" fill="none" stroke-linecap="round"/>
      <path d="M72 20 L74 14 L76 20 L82 22 L76 24 L74 30 L72 24 L66 22 Z" fill="#FFE082"/>
    </svg>""",
    "bandaid": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <g transform="rotate(-28 48 48)">
        <rect x="14" y="34" width="68" height="28" rx="14" fill="#FFE5D4" stroke="#7A545D" stroke-width="2.6"/>
        <rect x="36" y="34" width="24" height="28" fill="#FFFDF9" stroke="#7A545D" stroke-width="2.2"/>
        <circle cx="24" cy="44" r="2" fill="#D99B82"/><circle cx="24" cy="52" r="2" fill="#D99B82"/>
        <circle cx="72" cy="44" r="2" fill="#D99B82"/><circle cx="72" cy="52" r="2" fill="#D99B82"/>
        <path d="M48 53 C44 49, 41 46, 43 43 C45 41, 47 42, 48 44 C49 42, 51 41, 53 43 C55 46, 52 49, 48 53 Z" fill="#F28CA6"/>
      </g>
      <circle cx="74" cy="24" r="4" fill="#FADCE4"/><circle cx="22" cy="72" r="3.5" fill="#D8F1E7"/>
    </svg>""",
    "sleep_cloud": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <path d="M24 66 H72 C80 66, 84 60, 82 52 C80 45, 73 43, 69 44 C67 33, 55 27, 45 32 C38 30, 30 35, 29 44 C20 44, 15 51, 17 58 C18 63, 21 66, 24 66 Z" fill="#EAE3FA" stroke="#695A8A" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M37 52 Q40 55 43 52" stroke="#4A3B36" stroke-width="2.3" fill="none" stroke-linecap="round"/>
      <path d="M55 52 Q58 55 61 52" stroke="#4A3B36" stroke-width="2.3" fill="none" stroke-linecap="round"/>
      <ellipse cx="34" cy="56" rx="3.8" ry="2.2" fill="#F5B4C6" opacity="0.8"/>
      <ellipse cx="64" cy="56" rx="3.8" ry="2.2" fill="#F5B4C6" opacity="0.8"/>
      <path d="M47 56 Q49 58 51 56" stroke="#4A3B36" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M72 16 A11 11 0 1 0 83 27 A8 8 0 1 1 72 16 Z" fill="#FFE082" stroke="#B58A2A" stroke-width="2"/>
      <text x="16" y="30" font-size="11" font-weight="700" fill="#8C78B8">zZ</text>
    </svg>""",
    "bell": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <path d="M48 18 C34 18, 26 29, 26 45 L22 60 H74 L70 45 C70 29, 62 18, 48 18 Z" fill="#FFF2B8" stroke="#8C6D2E" stroke-width="2.6" stroke-linejoin="round"/>
      <circle cx="48" cy="65" r="7" fill="#F7C96E" stroke="#8C6D2E" stroke-width="2.4"/>
      <circle cx="41" cy="43" r="2.7" fill="#4A3B36"/><circle cx="55" cy="43" r="2.7" fill="#4A3B36"/>
      <path d="M45 48 Q48 51 51 48" stroke="#4A3B36" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <path d="M18 28 L12 24 M78 28 L84 24 M48 10 L48 14" stroke="#E8A2B4" stroke-width="3" stroke-linecap="round"/>
    </svg>""",
    "neuron": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <path d="M48 16 L54 34 L74 28 L61 46 L78 58 L58 60 L60 78 L46 64 L32 76 L37 57 L18 54 L36 44 L24 28 L42 35 Z" fill="#D8F1E7" stroke="#3F7D69" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="43" cy="46" r="2.7" fill="#4A3B36"/><circle cx="54" cy="46" r="2.7" fill="#4A3B36"/>
      <ellipse cx="38" cy="51" rx="3.4" ry="2" fill="#F5A8BC" opacity="0.8"/>
      <ellipse cx="59" cy="51" rx="3.4" ry="2" fill="#F5A8BC" opacity="0.8"/>
      <path d="M46 51 Q48.5 54 51 51" stroke="#4A3B36" stroke-width="2.1" fill="none" stroke-linecap="round"/>
    </svg>""",
    "capsule": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <g transform="rotate(-32 48 48)">
        <rect x="20" y="32" width="56" height="32" rx="16" fill="#D8F1E7" stroke="#5B6E68" stroke-width="2.6"/>
        <path d="M48 32 H60 A16 16 0 0 1 60 64 H48 Z" fill="#FADCE4" stroke="#5B6E68" stroke-width="2.6"/>
        <circle cx="38" cy="46" r="2.5" fill="#4A3B36"/><circle cx="58" cy="46" r="2.5" fill="#4A3B36"/>
        <path d="M45 51 Q48 54 51 51" stroke="#4A3B36" stroke-width="2.1" fill="none" stroke-linecap="round"/>
      </g>
      <path d="M74 20 L76 14 L78 20 L84 22 L78 24 L76 30 L74 24 L68 22 Z" fill="#FFE082"/>
    </svg>""",
    "ice": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <rect x="22" y="22" width="52" height="52" rx="14" fill="#DCEFF9" stroke="#517B96" stroke-width="2.6"/>
      <path d="M30 30 H44 M30 37 H36" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
      <circle cx="40" cy="49" r="2.8" fill="#4A3B36"/><circle cx="56" cy="49" r="2.8" fill="#4A3B36"/>
      <path d="M45 55 Q48 58 51 55" stroke="#4A3B36" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <ellipse cx="35" cy="54" rx="3.6" ry="2" fill="#F5B2C6" opacity="0.75"/>
      <ellipse cx="61" cy="54" rx="3.6" ry="2" fill="#F5B2C6" opacity="0.75"/>
    </svg>""",
    "heart_chat": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <path d="M22 24 H74 A12 12 0 0 1 86 36 V58 A12 12 0 0 1 74 70 H42 L26 80 L30 70 H22 A12 12 0 0 1 10 58 V36 A12 12 0 0 1 22 24 Z" fill="#FFE8DC" stroke="#8A5E4E" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M48 60 C38 52, 32 45, 36 39 C39 34, 45 35, 48 40 C51 35, 57 34, 60 39 C64 45, 58 52, 48 60 Z" fill="#F48AA8" stroke="#8A5E4E" stroke-width="2"/>
    </svg>""",
    "sunflower": """<svg viewBox="0 0 96 96" class="sticker-svg" aria-hidden="true">
      <g fill="#FFE48F" stroke="#9A7732" stroke-width="2">
        <ellipse cx="48" cy="20" rx="8" ry="12"/><ellipse cx="48" cy="76" rx="8" ry="12"/>
        <ellipse cx="20" cy="48" rx="12" ry="8"/><ellipse cx="76" cy="48" rx="12" ry="8"/>
        <ellipse cx="28" cy="28" rx="9" ry="9"/><ellipse cx="68" cy="28" rx="9" ry="9"/>
        <ellipse cx="28" cy="68" rx="9" ry="9"/><ellipse cx="68" cy="68" rx="9" ry="9"/>
      </g>
      <circle cx="48" cy="48" r="20" fill="#D9A87E" stroke="#704D34" stroke-width="2.5"/>
      <circle cx="42" cy="46" r="2.6" fill="#4A3B36"/><circle cx="54" cy="46" r="2.6" fill="#4A3B36"/>
      <path d="M44 52 Q48 56 52 52" stroke="#4A3B36" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <ellipse cx="37" cy="51" rx="3.4" ry="2" fill="#F7A7B8" opacity="0.8"/>
      <ellipse cx="59" cy="51" rx="3.4" ry="2" fill="#F7A7B8" opacity="0.8"/>
    </svg>""",
    "faces_scale": """<svg viewBox="0 0 180 60" class="sticker-svg-wide" aria-hidden="true">
      <g stroke="#5D4B45" stroke-width="2">
        <circle cx="24" cy="30" r="16" fill="#D8F1E7"/>
        <circle cx="19" cy="27" r="1.8" fill="#4A3B36"/><circle cx="29" cy="27" r="1.8" fill="#4A3B36"/>
        <path d="M19 33 Q24 38 29 33" fill="none" stroke-linecap="round"/>
        <circle cx="68" cy="30" r="16" fill="#FFF3C4"/>
        <circle cx="63" cy="27" r="1.8" fill="#4A3B36"/><circle cx="73" cy="27" r="1.8" fill="#4A3B36"/>
        <path d="M63 34 H73" fill="none" stroke-linecap="round"/>
        <circle cx="112" cy="30" r="16" fill="#FFE5D4"/>
        <circle cx="107" cy="27" r="1.8" fill="#4A3B36"/><circle cx="117" cy="27" r="1.8" fill="#4A3B36"/>
        <path d="M107 36 Q112 32 117 36" fill="none" stroke-linecap="round"/>
        <circle cx="156" cy="30" r="16" fill="#FADCE4"/>
        <path d="M149 25 L153 28 M163 25 L159 28" stroke-linecap="round"/>
        <path d="M150 37 Q156 32 162 37" fill="none" stroke-linecap="round"/>
      </g>
    </svg>""",
}


def _to_data_uri(img_path: Path) -> str:
    mime = mimetypes.guess_type(str(img_path))[0] or "image/png"
    b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _esc(text: str) -> str:
    return html.escape(text or "")


def build_pastel_html_deck(
    repo_root: Path,
    deck_meta: Dict[str, Any],
    slides: List[Dict[str, Any]],
    output_path: Path,
) -> Path:
    """Compile structured slides into a self-contained Japanese cute pastel HTML deck."""
    rendered_slides: List[str] = []
    overview_items: List[str] = []
    notes_data: List[Dict[str, Any]] = []

    total = len(slides)

    for idx, sl in enumerate(slides, start=1):
        tint = sl.get("theme_tint", "pink")
        sticker_key = sl.get("sticker", "brain")
        sticker_svg = STICKERS.get(sticker_key, STICKERS["brain"])
        unit_badge = _esc(sl.get("unit_badge", ""))
        title = _esc(sl.get("action_title", ""))
        subtitle = _esc(sl.get("subtitle", "") or "")
        apa = _esc(sl.get("apa_citation", ""))
        est_min = sl.get("est_minutes", 1.5)

        notes_data.append(
            {
                "no": idx,
                "title": sl.get("action_title", ""),
                "unit": sl.get("unit_badge", ""),
                "minutes": est_min,
                "notes": sl.get("speaker_notes", ""),
            }
        )
        overview_items.append(
            f'<button class="ov-item tint-{tint}" data-goto="{idx - 1}" type="button">'
            f'<span class="ov-num">P.{idx:02d}</span>'
            f'<span class="ov-unit">{unit_badge}</span>'
            f'<span class="ov-title">{title}</span>'
            f"</button>"
        )

        # Cover slide special layout
        if idx == 1:
            presenter = _esc(deck_meta.get("presenter", "黃少杰"))
            course = _esc(deck_meta.get("course", "健康心理學"))
            date_str = _esc(deck_meta.get("date", "2026/11/21"))
            bullets_html = "".join(
                f"<li>{_esc(b)}</li>" for b in sl.get("bullets", [])
            )
            slide_html = f"""
            <section class="slide slide-cover tint-{tint}" data-index="{idx - 1}">
              <div class="washi-tape tape-left"></div>
              <div class="washi-tape tape-right"></div>
              <div class="cover-inner">
                <div class="cover-badge">{unit_badge}</div>
                <div class="cover-stickers">
                  {STICKERS['brain']}
                  {STICKERS['bandaid']}
                  {STICKERS['sleep_cloud']}
                </div>
                <h1 class="cover-title">{title}</h1>
                <p class="cover-sub">{subtitle}</p>
                <div class="cover-meta">
                  <span class="meta-pill">報告者：{presenter}</span>
                  <span class="meta-pill">課程：{course}</span>
                  <span class="meta-pill">日期：{date_str}</span>
                </div>
                <ul class="cover-highlights">{bullets_html}</ul>
              </div>
              <footer class="slide-footer">
                <span class="apa-text">{apa}</span>
                <span class="page-chip">{idx} / {total}</span>
              </footer>
            </section>
            """
            rendered_slides.append(slide_html)
            continue

        # Highlight stat badges
        stats_html = ""
        if sl.get("highlight_stats"):
            cards = []
            for st in sl["highlight_stats"]:
                cards.append(
                    f'<div class="stat-pill">'
                    f'<div class="stat-val">{_esc(st.get("value", ""))}</div>'
                    f'<div class="stat-lbl">{_esc(st.get("label", ""))}</div>'
                    f"</div>"
                )
            stats_html = f'<div class="stat-row">{"".join(cards)}</div>'

        # Bullets
        bullets_html = ""
        if sl.get("bullets"):
            items = "".join(f"<li>{_esc(b)}</li>" for b in sl["bullets"])
            bullets_html = f'<ul class="pastel-list">{items}</ul>'

        # Table
        table_html = ""
        tbl = sl.get("table")
        if tbl and tbl.get("headers"):
            ths = "".join(f"<th>{_esc(h)}</th>" for h in tbl["headers"])
            trs = []
            for r in tbl.get("rows", []):
                tds = "".join(f"<td>{_esc(c)}</td>" for c in r)
                trs.append(f"<tr>{tds}</tr>")
            table_html = (
                f'<div class="table-wrap"><table class="pastel-table">'
                f"<thead><tr>{ths}</tr></thead>"
                f'<tbody>{"".join(trs)}</tbody></table></div>'
            )

        # Wiki gap badge if present
        gap_html = ""
        if sl.get("wiki_gap_note"):
            gap_html = f'<div class="gap-banner">{_esc(sl["wiki_gap_note"])}</div>'

        # Embedded asset figure (Base64)
        asset_html = ""
        has_asset = False
        if sl.get("asset_path"):
            full_img = repo_root / sl["asset_path"]
            if full_img.exists():
                has_asset = True
                uri = _to_data_uri(full_img)
                cap = _esc(sl.get("asset_caption", "") or "")
                asset_html = f"""
                <figure class="figure-frame">
                  <div class="mini-tape"></div>
                  <img src="{uri}" alt="{cap}" class="zoomable-img" loading="lazy" />
                  <figcaption>{cap} <span class="zoom-hint">（點擊放大）</span></figcaption>
                </figure>
                """

        body_cls = "slide-body two-col" if has_asset else "slide-body one-col"
        right_col = f'<div class="col-media">{asset_html}</div>' if has_asset else ""

        slide_html = f"""
        <section class="slide tint-{tint}" data-index="{idx - 1}">
          <header class="slide-header">
            <div class="header-left">
              <span class="unit-pill">{unit_badge}</span>
              <h2 class="action-title">{title}</h2>
              {f'<p class="slide-sub">{subtitle}</p>' if subtitle else ''}
            </div>
            <div class="header-sticker">{sticker_svg}</div>
          </header>
          <div class="{body_cls}">
            <div class="col-text">
              {stats_html}
              {bullets_html}
              {table_html}
              {gap_html}
            </div>
            {right_col}
          </div>
          <footer class="slide-footer">
            <span class="apa-text">{apa}</span>
            <span class="page-chip">{idx} / {total}</span>
          </footer>
        </section>
        """
        rendered_slides.append(slide_html)

    doc_title = _esc(deck_meta.get("deck_title", "Chapter 11: 疼痛的本質與症狀"))
    notes_json = json.dumps(notes_data, ensure_ascii=False)

    full_html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{doc_title}</title>
<style>
  :root {{
    --bg-cream: #FFFDF7;
    --ink: #4A3B36;
    --ink-soft: #75625C;
    --pink: #FADCE4;
    --pink-deep: #D96B8A;
    --mint: #D8F1E7;
    --mint-deep: #3F8B72;
    --lemon: #FFF3C4;
    --lemon-deep: #B58124;
    --lavender: #EAE3FA;
    --lavender-deep: #6F5AA8;
    --peach: #FFE5D4;
    --peach-deep: #C46F4B;
    --card-bg: #FFFFFF;
    --radius: 26px;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    font-family: "Hiragino Maru Gothic ProN", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    color: var(--ink);
    background-color: var(--bg-cream);
    background-image: radial-gradient(#F3DFDF 1.2px, transparent 1.2px);
    background-size: 22px 22px;
  }}
  .app-shell {{
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }}
  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 20px;
    background: rgba(255, 253, 247, 0.94);
    border-bottom: 2px dashed #F0D9DF;
    flex-shrink: 0;
  }}
  .brand {{
    font-weight: 800;
    font-size: 0.95rem;
    color: var(--ink);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .progress-wrap {{
    flex: 1;
    max-width: 340px;
    height: 10px;
    background: #F4EAE6;
    border-radius: 999px;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #F49BB4, #F7C97E, #7CCBB0);
    border-radius: 999px;
    transition: width 0.25s ease;
  }}
  .top-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
  }}
  .btn {{
    appearance: none;
    border: 2px solid #EAD7DD;
    background: #FFFFFF;
    color: var(--ink);
    border-radius: 999px;
    padding: 6px 13px;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.12s ease, background 0.15s ease;
    white-space: nowrap;
  }}
  .btn:hover {{ background: #FFF0F4; transform: translateY(-1px); }}
  .btn.active {{ background: var(--pink); border-color: var(--pink-deep); }}
  .stage-area {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 22px;
    overflow: hidden;
    position: relative;
  }}
  .deck {{
    width: 100%;
    max-width: 1180px;
    height: 100%;
    max-height: 700px;
    position: relative;
  }}
  .slide {{
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    background: var(--card-bg);
    border-radius: var(--radius);
    border: 3px solid #F2D8E0;
    box-shadow: 0 12px 30px rgba(155, 114, 118, 0.12);
    padding: 24px 30px 16px;
    position: relative;
    overflow: hidden;
  }}
  .slide.active {{ display: flex; animation: fadeIn 0.22s ease; }}
  @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

  .slide.tint-pink {{ border-color: #F4CBD7; }}
  .slide.tint-mint {{ border-color: #BFE6D8; }}
  .slide.tint-lemon {{ border-color: #F6E09D; }}
  .slide.tint-lavender {{ border-color: #D7CCF2; }}
  .slide.tint-peach {{ border-color: #F6CEB7; }}

  .slide.tint-pink .unit-pill {{ background: var(--pink); color: #8B3B55; }}
  .slide.tint-mint .unit-pill {{ background: var(--mint); color: #266450; }}
  .slide.tint-lemon .unit-pill {{ background: var(--lemon); color: #7C5414; }}
  .slide.tint-lavender .unit-pill {{ background: var(--lavender); color: #4E3B82; }}
  .slide.tint-peach .unit-pill {{ background: var(--peach); color: #8A4528; }}

  /* Cover */
  .slide-cover {{
    background: linear-gradient(155deg, #FFF7F9 0%, #FFFDF7 52%, #F3FBF8 100%);
    justify-content: space-between;
    text-align: center;
  }}
  .washi-tape {{
    position: absolute;
    top: -10px;
    width: 130px;
    height: 30px;
    opacity: 0.72;
    border-radius: 6px;
  }}
  .tape-left {{ left: 32px; background: var(--pink); transform: rotate(-10deg); }}
  .tape-right {{ right: 32px; background: var(--mint); transform: rotate(9deg); }}
  .cover-inner {{
    margin: auto;
    max-width: 860px;
    padding: 12px;
  }}
  .cover-badge {{
    display: inline-block;
    background: var(--lemon);
    color: #7A5413;
    font-weight: 800;
    font-size: 0.9rem;
    padding: 6px 18px;
    border-radius: 999px;
    margin-bottom: 12px;
  }}
  .cover-stickers {{
    display: flex;
    justify-content: center;
    gap: 14px;
    margin-bottom: 10px;
  }}
  .cover-stickers .sticker-svg {{ width: 70px; height: 70px; }}
  .cover-title {{
    margin: 6px 0 8px;
    font-size: clamp(1.7rem, 3.2vw, 2.5rem);
    line-height: 1.25;
    color: var(--ink);
  }}
  .cover-sub {{
    margin: 0 0 18px;
    font-size: 1.05rem;
    color: var(--ink-soft);
    font-weight: 600;
  }}
  .cover-meta {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 16px;
  }}
  .meta-pill {{
    background: #FFFFFF;
    border: 2px solid #F0D9DF;
    border-radius: 999px;
    padding: 6px 16px;
    font-weight: 700;
    font-size: 0.92rem;
  }}
  .cover-highlights {{
    list-style: none;
    padding: 0;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
  }}
  .cover-highlights li {{
    background: rgba(255, 255, 255, 0.85);
    border: 1.5px dashed #E2C6CE;
    border-radius: 14px;
    padding: 6px 12px;
    font-size: 0.86rem;
    color: var(--ink-soft);
  }}

  /* Content Header */
  .slide-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 14px;
    border-bottom: 2px dashed #F1E3E6;
    padding-bottom: 10px;
    flex-shrink: 0;
  }}
  .unit-pill {{
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 800;
    padding: 4px 13px;
    border-radius: 999px;
    margin-bottom: 6px;
  }}
  .action-title {{
    margin: 0;
    font-size: clamp(1.18rem, 2.1vw, 1.56rem);
    line-height: 1.3;
    color: var(--ink);
  }}
  .slide-sub {{
    margin: 4px 0 0;
    font-size: 0.9rem;
    color: var(--ink-soft);
  }}
  .header-sticker {{ flex-shrink: 0; }}
  .sticker-svg {{ width: 62px; height: 62px; display: block; }}
  .sticker-svg-wide {{ width: 132px; height: 48px; display: block; }}

  /* Slide Body */
  .slide-body {{
    flex: 1;
    display: grid;
    gap: 18px;
    padding: 14px 0 8px;
    overflow-y: auto;
    align-items: start;
  }}
  .slide-body.one-col {{ grid-template-columns: 1fr; }}
  .slide-body.two-col {{ grid-template-columns: 1.12fr 0.88fr; }}
  .col-text {{ display: flex; flex-direction: column; gap: 11px; }}
  .col-media {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}

  .stat-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .stat-pill {{
    flex: 1 1 130px;
    background: #FFF9FB;
    border: 2px solid #F4D2DD;
    border-radius: 18px;
    padding: 10px 14px;
    text-align: center;
  }}
  .stat-val {{
    font-size: 1.38rem;
    font-weight: 900;
    color: #C75678;
    line-height: 1.2;
  }}
  .stat-lbl {{
    font-size: 0.8rem;
    color: var(--ink-soft);
    margin-top: 3px;
    font-weight: 600;
  }}

  .pastel-list {{
    margin: 0;
    padding-left: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .pastel-list li {{
    background: #FFFDFB;
    border: 1.5px solid #F2E4E1;
    border-left: 6px solid #F3B6C8;
    border-radius: 14px;
    padding: 9px 14px;
    font-size: 0.96rem;
    line-height: 1.52;
  }}
  .slide.tint-mint .pastel-list li {{ border-left-color: #96D8C2; }}
  .slide.tint-lemon .pastel-list li {{ border-left-color: #F4CF73; }}
  .slide.tint-lavender .pastel-list li {{ border-left-color: #BCA9EA; }}
  .slide.tint-peach .pastel-list li {{ border-left-color: #F4B18D; }}

  .table-wrap {{ overflow-x: auto; }}
  .pastel-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.86rem;
    border-radius: 14px;
    overflow: hidden;
    border: 1.5px solid #EDD9DF;
  }}
  .pastel-table th {{
    background: #FDF0F4;
    color: var(--ink);
    font-weight: 800;
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1.5px solid #EDD9DF;
  }}
  .pastel-table td {{
    padding: 7px 10px;
    border-bottom: 1px solid #F4E9EC;
    vertical-align: top;
    line-height: 1.42;
  }}
  .pastel-table tr:last-child td {{ border-bottom: none; }}
  .pastel-table tbody tr:nth-child(even) {{ background: #FFFDF9; }}

  .figure-frame {{
    margin: 0;
    background: #FFFDF9;
    border: 2.5px solid #F1DADF;
    border-radius: 20px;
    padding: 12px 12px 10px;
    position: relative;
    box-shadow: 0 6px 16px rgba(155, 114, 118, 0.1);
    width: 100%;
    text-align: center;
  }}
  .mini-tape {{
    position: absolute;
    top: -9px;
    left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 78px;
    height: 18px;
    background: rgba(216, 241, 231, 0.9);
    border-radius: 4px;
  }}
  .figure-frame img {{
    max-width: 100%;
    max-height: 360px;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 10px;
    cursor: zoom-in;
    display: block;
    margin: 0 auto;
  }}
  .figure-frame figcaption {{
    margin-top: 8px;
    font-size: 0.8rem;
    color: var(--ink-soft);
    line-height: 1.38;
  }}
  .zoom-hint {{ color: #C26882; font-weight: 700; }}

  .gap-banner {{
    background: #FFF7DC;
    border: 1.5px dashed #E0B451;
    color: #7A5816;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 0.82rem;
    font-weight: 700;
  }}

  /* Footer */
  .slide-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding-top: 8px;
    border-top: 1.5px dashed #F1E3E6;
    font-size: 0.78rem;
    color: var(--ink-soft);
    flex-shrink: 0;
  }}
  .page-chip {{
    background: #F9EFF2;
    color: #8B4E60;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 999px;
    white-space: nowrap;
  }}

  /* Bottom nav */
  .bottombar {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    padding: 10px 18px;
    background: rgba(255, 253, 247, 0.95);
    border-top: 2px dashed #F0D9DF;
    flex-shrink: 0;
  }}
  .shortcut-hint {{ font-size: 0.8rem; color: var(--ink-soft); }}

  /* Speaker Notes Drawer */
  .notes-drawer {{
    display: none;
    background: #FFF9F2;
    border-top: 3px solid #F4CBD7;
    padding: 14px 24px;
    max-height: 28vh;
    overflow-y: auto;
    flex-shrink: 0;
  }}
  .notes-drawer.open {{ display: block; }}
  .notes-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 0.86rem;
    font-weight: 800;
    color: #8A4A5D;
  }}
  .notes-body {{
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.65;
    color: var(--ink);
  }}

  /* Overview & Zoom Modals */
  .modal-backdrop {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(74, 59, 54, 0.52);
    z-index: 100;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }}
  .modal-backdrop.open {{ display: flex; }}
  .modal-box {{
    background: #FFFDF9;
    border: 3px solid #F2D3DC;
    border-radius: 24px;
    max-width: 980px;
    width: 100%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .modal-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 20px;
    border-bottom: 2px dashed #F1DCE2;
    font-weight: 800;
  }}
  .ov-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 10px;
    padding: 16px;
    overflow-y: auto;
  }}
  .ov-item {{
    text-align: left;
    border: 2px solid #EED9E0;
    background: #FFFFFF;
    border-radius: 16px;
    padding: 10px 12px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 4px;
    color: var(--ink);
  }}
  .ov-item:hover {{ background: #FFF4F7; }}
  .ov-num {{ font-weight: 900; font-size: 0.78rem; color: #C2627E; }}
  .ov-unit {{ font-size: 0.72rem; color: var(--ink-soft); font-weight: 700; }}
  .ov-title {{ font-size: 0.84rem; font-weight: 700; line-height: 1.35; }}

  .zoom-box {{
    background: #FFFFFF;
    border-radius: 20px;
    padding: 16px;
    max-width: 92vw;
    max-height: 90vh;
    text-align: center;
    overflow: auto;
  }}
  .zoom-box img {{ max-width: 100%; max-height: 76vh; border-radius: 10px; }}
  .zoom-cap {{ margin: 8px 0 0; font-size: 0.9rem; color: var(--ink-soft); }}

  @media (max-width: 820px) {{
    .slide {{ padding: 16px 16px 12px; }}
    .slide-body.two-col {{ grid-template-columns: 1fr; }}
    .shortcut-hint {{ display: none; }}
    .progress-wrap {{ display: none; }}
  }}

  @media print {{
    @page {{ size: A4 landscape; margin: 8mm; }}
    html, body {{ height: auto; background: #FFFFFF !important; overflow: visible !important; }}
    .app-shell {{ height: auto; display: block; overflow: visible; }}
    .topbar, .bottombar, .notes-drawer, .modal-backdrop, .zoom-hint {{ display: none !important; }}
    .stage-area {{ display: block; padding: 0; overflow: visible; }}
    .deck {{ max-width: none; max-height: none; height: auto; }}
    .slide {{
      display: flex !important;
      page-break-after: always;
      break-after: page;
      height: 190mm;
      box-shadow: none;
      margin-bottom: 8mm;
    }}
    .slide:last-child {{ page-break-after: auto; break-after: auto; }}
  }}
</style>
</head>
<body>
<div class="app-shell">
  <header class="topbar">
    <div class="brand">{doc_title}</div>
    <div class="progress-wrap" aria-label="簡報進度"><div class="progress-fill" id="progressFill"></div></div>
    <div class="top-actions">
      <button class="btn" id="btnOverview" type="button">目錄 (G)</button>
      <button class="btn" id="btnNotes" type="button">講稿 (N)</button>
      <button class="btn" id="btnPrint" type="button">列印 PDF</button>
    </div>
  </header>

  <main class="stage-area">
    <div class="deck" id="deck">
      {"".join(rendered_slides)}
    </div>
  </main>

  <aside class="notes-drawer" id="notesDrawer" aria-live="polite">
    <div class="notes-head">
      <span id="notesMeta">講者口語講稿</span>
      <button class="btn" id="btnCloseNotes" type="button">收合</button>
    </div>
    <p class="notes-body" id="notesText"></p>
  </aside>

  <footer class="bottombar">
    <button class="btn" id="btnPrev" type="button">← 上一頁</button>
    <span class="page-chip" id="counterChip">1 / {total}</span>
    <button class="btn" id="btnNext" type="button">下一頁 →</button>
    <span class="shortcut-hint">快捷鍵：← / → / 空白鍵 翻頁 ｜ N 講稿 ｜ G 目錄</span>
  </footer>
</div>

<div class="modal-backdrop" id="overviewModal" role="dialog" aria-modal="true" aria-label="投影片目錄">
  <div class="modal-box">
    <div class="modal-head">
      <span>投影片總覽（共 {total} 頁）</span>
      <button class="btn" id="btnCloseOverview" type="button">關閉</button>
    </div>
    <div class="ov-grid">{"".join(overview_items)}</div>
  </div>
</div>

<div class="modal-backdrop" id="zoomModal" role="dialog" aria-modal="true" aria-label="圖表放大檢視">
  <div class="zoom-box">
    <img id="zoomImg" src="" alt="" />
    <p class="zoom-cap" id="zoomCap"></p>
    <div style="margin-top:10px;"><button class="btn" id="btnCloseZoom" type="button">關閉放大</button></div>
  </div>
</div>

<script>
(function() {{
  const slides = Array.from(document.querySelectorAll('.slide'));
  const notesData = {notes_json};
  let current = 0;

  const progressFill = document.getElementById('progressFill');
  const counterChip = document.getElementById('counterChip');
  const notesDrawer = document.getElementById('notesDrawer');
  const notesMeta = document.getElementById('notesMeta');
  const notesText = document.getElementById('notesText');
  const btnNotes = document.getElementById('btnNotes');
  const overviewModal = document.getElementById('overviewModal');
  const zoomModal = document.getElementById('zoomModal');
  const zoomImg = document.getElementById('zoomImg');
  const zoomCap = document.getElementById('zoomCap');

  function render() {{
    slides.forEach((el, i) => el.classList.toggle('active', i === current));
    const pct = slides.length > 1 ? ((current + 1) / slides.length) * 100 : 100;
    progressFill.style.width = pct.toFixed(1) + '%';
    counterChip.textContent = (current + 1) + ' / ' + slides.length;
    const item = notesData[current] || {{}};
    notesMeta.textContent = 'P.' + (current + 1) + ' 口語講稿（預估 ' + (item.minutes || 1.5) + ' 分鐘）｜' + (item.unit || '');
    notesText.textContent = item.notes || '';
  }}

  function goTo(idx) {{
    if (idx < 0) idx = 0;
    if (idx >= slides.length) idx = slides.length - 1;
    current = idx;
    render();
  }}

  function toggleNotes() {{
    const isOpen = notesDrawer.classList.toggle('open');
    btnNotes.classList.toggle('active', isOpen);
  }}

  document.getElementById('btnPrev').addEventListener('click', () => goTo(current - 1));
  document.getElementById('btnNext').addEventListener('click', () => goTo(current + 1));
  btnNotes.addEventListener('click', toggleNotes);
  document.getElementById('btnCloseNotes').addEventListener('click', toggleNotes);
  document.getElementById('btnPrint').addEventListener('click', () => window.print());

  document.getElementById('btnOverview').addEventListener('click', () => overviewModal.classList.add('open'));
  document.getElementById('btnCloseOverview').addEventListener('click', () => overviewModal.classList.remove('open'));
  overviewModal.addEventListener('click', (e) => {{
    if (e.target === overviewModal) overviewModal.classList.remove('open');
  }});
  overviewModal.querySelectorAll('[data-goto]').forEach((btn) => {{
    btn.addEventListener('click', () => {{
      goTo(Number(btn.getAttribute('data-goto')));
      overviewModal.classList.remove('open');
    }});
  }});

  document.querySelectorAll('.zoomable-img').forEach((img) => {{
    img.addEventListener('click', () => {{
      zoomImg.src = img.src;
      zoomImg.alt = img.alt;
      zoomCap.textContent = img.alt;
      zoomModal.classList.add('open');
    }});
  }});
  document.getElementById('btnCloseZoom').addEventListener('click', () => zoomModal.classList.remove('open'));
  zoomModal.addEventListener('click', (e) => {{
    if (e.target === zoomModal) zoomModal.classList.remove('open');
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') {{
      overviewModal.classList.remove('open');
      zoomModal.classList.remove('open');
      return;
    }}
    if (overviewModal.classList.contains('open') || zoomModal.classList.contains('open')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') {{
      e.preventDefault();
      goTo(current + 1);
    }} else if (e.key === 'ArrowLeft') {{
      e.preventDefault();
      goTo(current - 1);
    }} else if (e.key.toLowerCase() === 'n') {{
      toggleNotes();
    }} else if (e.key.toLowerCase() === 'g') {{
      overviewModal.classList.toggle('open');
    }}
  }});

  render();
}})();
</script>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html, encoding="utf-8")
    return output_path
