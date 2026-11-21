"""3-tier Wiki retrieval aligned with AGENTS.md."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple


def retrieve_wiki_context(
    repo_root: Path, topic: str, max_files: int = 15
) -> Tuple[str, List[str], List[str]]:
    """
    Implements the 3-tier retrieval strategy from AGENTS.md:
      1. Keyword/tag scan across wiki/ frontmatter & text.
      2. Read wiki/index.md and category _index.md files.
      3. Load top matched pages (capped at max_files) and list raw/assets/ images.
    """
    wiki_dir = repo_root / "wiki"
    assets_dir = repo_root / "raw" / "assets"

    tokens = [
        t.lower()
        for t in re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]{2,}", topic)
        if len(t) >= 2
    ]

    # Tier 1 & 2: score all markdown files in wiki/
    scored: List[Tuple[int, Path]] = []
    for md in sorted(wiki_dir.rglob("*.md")):
        if md.name == "log.md":
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        low = text.lower()
        score = sum(low.count(tok) for tok in tokens) if tokens else 1
        # Always boost index/overview slightly if small repo
        if md.name in ("index.md", "overview.md", "_index.md"):
            score += 1
        scored.append((score, md))

    scored.sort(key=lambda x: (-x[0], str(x[1])))
    selected = [p for _, p in scored[:max_files]]

    chunks: List[str] = []
    used_rel: List[str] = []
    for p in selected:
        rel = str(p.relative_to(repo_root))
        used_rel.append(rel)
        content = p.read_text(encoding="utf-8", errors="ignore")
        chunks.append(f"=== FILE: {rel} ===\n{content}")

    assets: List[str] = []
    if assets_dir.exists():
        for img in sorted(assets_dir.rglob("*")):
            if img.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
                assets.append(str(img.relative_to(repo_root)))

    context_pack = "\n\n".join(chunks)
    return context_pack, assets, used_rel
