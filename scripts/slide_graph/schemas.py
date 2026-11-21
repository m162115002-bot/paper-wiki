"""Pydantic schemas and LangGraph shared state for Slide Graph v3 (Auto Ingest + Figure Crop + Map-Reduce Slides)."""
from __future__ import annotations

from typing import Annotated, Any, Dict, List, Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


# ---------- Stage 0a: PDF Ingest & Figure Extraction Schemas ----------
class FigureCropSpec(BaseModel):
    page_number: int = Field(..., description="圖表所在的 PDF 頁碼（從 1 開始）")
    filename: str = Field(..., description="全小寫 ASCII 檔名，例如 fig12-1-pain-model.png")
    caption: str = Field(..., description="繁體中文圖說與原文頁碼")
    ymin: int = Field(..., ge=0, le=1000, description="圖表上邊界（0–1000 正規化座標）")
    xmin: int = Field(..., ge=0, le=1000, description="圖表左邊界（0–1000 正規化座標）")
    ymax: int = Field(..., ge=0, le=1000, description="圖表下邊界（0–1000 正規化座標）")
    xmax: int = Field(..., ge=0, le=1000, description="圖表右邊界（0–1000 正規化座標）")


class ConceptDraft(BaseModel):
    slug: str = Field(..., description="全小寫 ASCII slug，例如 operant-pain-management")
    title: str = Field(..., description="繁體中文標題")
    english_term: str = Field(..., description="英文專有名詞")
    category: str = Field(..., description="英文分類標籤")
    one_line_summary: str = Field(..., description="一句話繁體中文摘要")
    body_markdown: str = Field(..., description="構念頁正文 Markdown（不含 YAML Frontmatter）")


class MethodDraft(BaseModel):
    slug: str = Field(..., description="全小寫 ASCII slug，例如 tens-therapy")
    title: str = Field(..., description="繁體中文標題")
    english_term: str = Field(..., description="英文全名與縮寫")
    method_type: str = Field(default="scale", description="scale / statistical_model / paradigm / biomarker / intervention")
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
    sample_size: str = Field(..., description="樣本數 N 或 N/A（綜論）")
    population: str
    design: str = Field(..., description="研究設計，如 RCT / cross_sectional / textbook_chapter_review")
    measures: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    executive_summary: str = Field(..., description="4–6 句繁體中文核心摘要")
    paper_body_markdown: str = Field(..., description="完整單篇文獻頁正文 Markdown（不含 YAML Frontmatter）")
    figures: List[FigureCropSpec] = Field(
        default_factory=list,
        description="PDF 內值得擷取的關鍵統計圖表、流程圖或模型圖（最多 8 張，給出精準 0–1000 裁切座標）",
    )
    new_concepts: List[ConceptDraft] = Field(default_factory=list)
    new_methods: List[MethodDraft] = Field(default_factory=list)


# ---------- Stage 1: Outline Schemas ----------
class SlideOutlineItem(BaseModel):
    slide_no: int = Field(..., description="投影片頁碼（從 1 開始）")
    unit_id: str = Field(..., description="所屬單元代碼，例如 unit_1")
    tentative_title: str = Field(..., description="暫定結論式標題")
    key_focus: str = Field(..., description="本頁核心重點摘要")
    planned_asset: Optional[str] = Field(
        default=None, description="預計使用之 raw/assets/ 相對路徑（若無則為 null）"
    )
    est_minutes: float = Field(default=1.5, description="預估口報分鐘數")
    is_key_slide: bool = Field(default=False, description="是否為含重要統計數據、爭議或需人工複核的重點頁")


class UnitOutline(BaseModel):
    unit_id: str = Field(..., description="單元代碼，如 unit_1")
    unit_name: str = Field(..., description="單元中文名稱")
    slides: List[SlideOutlineItem] = Field(default_factory=list)


class OutlineSchema(BaseModel):
    deck_title: str
    deck_subtitle: str
    total_slides: int
    total_est_minutes: float
    units: List[UnitOutline]
    wiki_gaps: List[str] = Field(default_factory=list)


# ---------- Stage 2: Slide Content Schemas ----------
class TableBlock(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class StatBadge(BaseModel):
    value: str = Field(..., description="數據數值，例如 > 80%")
    label: str = Field(..., description="數據說明文字")


class SlideSpec(BaseModel):
    slide_no: int
    unit_id: str
    unit_badge: str
    action_title: str = Field(..., description="結論式標題（Action Title）")
    subtitle: Optional[str] = None
    bullets: List[str] = Field(default_factory=list, description="精簡版面要點（建議 3–5 點）")
    table: Optional[TableBlock] = None
    highlight_stats: List[StatBadge] = Field(default_factory=list)
    asset_path: Optional[str] = Field(default=None, description="raw/assets/ 圖片相對路徑")
    asset_caption: Optional[str] = None
    sticker: str = Field(
        default="brain",
        description="日式可愛粉彩 SVG 貼紙名稱（brain/bandaid/sleep_cloud/bell/neuron/capsule/ice/heart_chat/sunflower/faces_scale）",
    )
    theme_tint: Literal["pink", "mint", "lemon", "lavender", "peach"] = "pink"
    speaker_notes: str = Field(..., description="可直接照念的繁體中文口語講稿")
    apa_citation: str = Field(..., description="頁尾 APA 7th 出處")
    est_minutes: float = 1.5
    wiki_gap_note: Optional[str] = None
    is_key_slide: bool = False
    flag_reason: Optional[str] = None


class UnitSlidesOutput(BaseModel):
    unit_id: str
    slides: List[SlideSpec]


class AutoCheckResult(BaseModel):
    passed: bool
    issues: List[str] = Field(default_factory=list)
    failed_unit_ids: List[str] = Field(default_factory=list)
    flagged_slide_nos: List[int] = Field(default_factory=list)


def merge_unit_slides(
    existing: Dict[str, List[Dict[str, Any]]],
    incoming: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, List[Dict[str, Any]]]:
    merged = dict(existing or {})
    for k, v in (incoming or {}).items():
        merged[k] = v
    return merged


class GraphState(TypedDict, total=False):
    # User inputs
    repo_root: str
    pdf_path: Optional[str]          # 指定單一 PDF；若未指定且 auto_ingest=True 則掃描所有新 PDF
    auto_ingest: bool
    force_extract_figures: bool      # 若該 PDF 已匯入但尚無圖表，可補擷取圖表
    topic: str
    presenter: str
    course: str
    date: str
    style: str
    target_minutes: int
    target_slides: int
    slug: str

    # Stage 0a: Ingest & Figure Extraction
    ingested_files: List[str]
    extracted_figures: List[str]

    # Stage 0b: Retrieval
    context_pack: str
    available_assets: List[str]
    wiki_files_used: List[str]

    # Stage 1: Outline
    outline: Dict[str, Any]
    outline_retries: int
    outline_feedback: str
    outline_check: Dict[str, Any]

    # Stage 2: Map-Reduce Per-Unit Slides
    unit_slides: Annotated[Dict[str, List[Dict[str, Any]]], merge_unit_slides]
    unit_retries: Dict[str, int]
    failed_unit_ids: List[str]
    flagged_slide_nos: List[int]
    content_feedback: str
    content_check: Dict[str, Any]
    merged_slides: List[Dict[str, Any]]

    # Stage 3: HTML Build & Verification
    html_output_path: str
    html_retries: int
    html_feedback: str
    html_check: Dict[str, Any]
    final_action: str
