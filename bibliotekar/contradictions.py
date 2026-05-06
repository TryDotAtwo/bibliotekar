"""
entity_id=contradictions_module; type=module; state=ready

Structured contradiction ledger.  A full semantic contradiction detector needs
an LLM.  This module implements a deterministic ledger and a lexical detector
that flags lines containing contradiction/conflict markers.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Dict, List


MARKERS = ["contradiction", "conflict", "inconsistent", "contradicts", "disagrees"]


def scan_contradictions(wiki_dir: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in wiki_dir.glob("**/*.md"):
        if path.name == "contradictions.md":
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            low = line.lower()
            if any(marker in low for marker in MARKERS):
                rows.append({"page": str(path.relative_to(wiki_dir)), "line": str(i), "claim": line.strip()})
    return rows


def write_ledger(wiki_dir: Path, rows: List[Dict[str, str]]) -> Path:
    synth = wiki_dir / "synthesis"
    synth.mkdir(parents=True, exist_ok=True)
    out = synth / "contradictions.md"
    lines = ["# Contradiction Ledger", "", f"generated_at={dt.datetime.now().isoformat(timespec='seconds')}", ""]
    if not rows:
        lines.append("status=no_contradictions_detected")
    else:
        for row in rows:
            lines.append(f"- page={row['page']}; line={row['line']}; claim={row['claim']}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
