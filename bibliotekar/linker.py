"""
entity_id=linker_module; type=module; state=ready

Bidirectional wiki crosslink repair.  Source pages link to concept pages.
Concept pages link back to source pages.  The module can scan existing pages
and generate missing reciprocal references.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .utils import slugify


CONCEPT_LINK_RE = re.compile(r"\[[^\]]+\]\(\.\./concepts/([^)]+)\)")


def source_to_concept_slugs(source_text: str) -> List[str]:
    slugs = []
    for match in CONCEPT_LINK_RE.finditer(source_text):
        slug = match.group(1).replace(".md", "")
        if slug not in slugs:
            slugs.append(slug)
    return slugs


def repair_bidirectional_links(wiki_dir: Path) -> Dict[str, List[str]]:
    report: Dict[str, List[str]] = {"added": [], "checked": []}
    sources_dir = wiki_dir / "sources"
    concepts_dir = wiki_dir / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    for source_path in sources_dir.glob("*.md"):
        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
        source_slug = source_path.stem
        report["checked"].append(source_slug)
        for concept_slug in source_to_concept_slugs(source_text):
            concept_path = concepts_dir / f"{concept_slug}.md"
            source_link = f"../sources/{source_slug}.md"
            if not concept_path.exists():
                concept_title = concept_slug.replace("-", " ").title()
                concept_path.write_text(
                    f"# {concept_title}\n\n**Concept:** {concept_title}\n\n**Sources**\n- [{source_slug}]({source_link})\n",
                    encoding="utf-8",
                )
                report["added"].append(f"{concept_slug}->{source_slug}")
                continue
            text = concept_path.read_text(encoding="utf-8", errors="ignore")
            if source_link not in text:
                if "**Sources**" not in text:
                    text += "\n\n**Sources**\n"
                text += f"- [{source_slug}]({source_link})\n"
                concept_path.write_text(text, encoding="utf-8")
                report["added"].append(f"{concept_slug}->{source_slug}")
    return report
