"""
entity_id=search_module; type=module; state=ready

Index-first wiki search.  Karpathy pattern says query starts at index.md,
then drills into relevant pages.  This module implements a small deterministic
term search over index.md entries and page contents.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Tuple


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in re.split(r"\W+", text) if len(t) >= 2]


def score_text(query_terms: Iterable[str], text: str) -> int:
    lower = text.lower()
    return sum(lower.count(term) for term in query_terms)


def search_wiki(wiki_dir: Path, query: str, top_k: int = 8) -> List[Tuple[Path, int]]:
    terms = tokenize(query)
    if not terms:
        return []
    candidates: dict[Path, int] = {}
    index_path = wiki_dir / "index.md"
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if ".md" not in line:
                continue
            score = score_text(terms, line)
            if score <= 0:
                continue
            # index lines are "- date | category/file.md | title"
            for chunk in line.split("|"):
                chunk = chunk.strip()
                if chunk.endswith(".md"):
                    path = wiki_dir / chunk
                    candidates[path] = candidates.get(path, 0) + score * 5

    # fall back / refine by scanning all markdown pages
    for path in wiki_dir.glob("**/*.md"):
        if path.name in {"index.md", "log.md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        score = score_text(terms, text)
        if score > 0:
            candidates[path] = candidates.get(path, 0) + score

    return sorted(candidates.items(), key=lambda item: item[1], reverse=True)[:top_k]


def read_context(results: List[Tuple[Path, int]], limit_chars: int = 24000) -> str:
    chunks: list[str] = []
    used = 0
    for path, score in results:
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.name
        chunk = f"\n\n--- PAGE={rel}; SCORE={score} ---\n{text}"
        if used + len(chunk) > limit_chars:
            chunk = chunk[: max(0, limit_chars - used)]
        chunks.append(chunk)
        used += len(chunk)
        if used >= limit_chars:
            break
    return "".join(chunks)
