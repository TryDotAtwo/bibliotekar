"""
entity_id=concept_extractor_module; type=module; state=initial

Utility functions for extracting concept and entity names from text.
Concept extraction is a simple heuristic that identifies candidate
concepts based on capitalization and word frequency.  The extraction
returns a sorted list of unique concept names.  Stopwords and
punctuation are ignored.  This module can be extended with more
sophisticated NLP techniques as needed.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Set

# Minimal stopword list to avoid trivial words as concepts
_STOPWORDS: Set[str] = {
    "the",
    "and",
    "a",
    "an",
    "of",
    "to",
    "in",
    "for",
    "is",
    "are",
    "on",
    "by",
    "with",
    "as",
    "that",
    "from",
    "this",
    "it",
    "at",
    "be",
    "or",
    "was",
    "but",
}


def extract_concepts(text: str) -> List[str]:
    """Extract potential concept names from a block of text.

    entity_id=extract_concepts; type=function; state=initial
    condition=text_provided → action=heuristic_extraction → result=concepts_list

    Parameters
    ----------
    text: str
        Text to analyse for concept names.

    Returns
    -------
    list[str]
        Sorted list of unique concept names identified in the text.
    """
    if not text:
        return []
    # Split on non‑word boundaries and filter tokens
    tokens = re.split(r"[^A-Za-z0-9_]+", text)
    candidates: Set[str] = set()
    for tok in tokens:
        if not tok:
            continue
        # Use uppercase initial letter or camelCase detection
        if tok[0].isupper() or (len(tok) > 1 and any(c.isupper() for c in tok[1:])):
            low = tok.lower()
            if low not in _STOPWORDS and len(tok) > 2:
                candidates.add(tok.strip())
    return sorted(candidates)