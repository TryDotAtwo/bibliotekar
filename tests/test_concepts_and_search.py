import os
import shutil
from pathlib import Path

import pytest

from bibliotekar.agent import Agent
from bibliotekar.config import Paths


def setup_tmp(tmp_path: Path) -> Agent:
    """Create a temporary project and return an Agent bound to it."""
    # Create base directories
    base_dir = tmp_path / "data"
    base_dir.mkdir()
    (base_dir / "raw").mkdir()
    (base_dir / "wiki").mkdir()
    # Write a sample raw file with concepts
    raw_file = base_dir / "raw" / "sample.txt"
    raw_file.write_text(
        """
        The Rubik Cube and God's Number
        Research into God’s Number for the 4x4 cube indicates unknown values.
        Concepts include Reduction Method and Yau Method.  Another name is Rubik's Revenge.
        """,
        encoding="utf-8",
    )
    paths = Paths(base_dir=base_dir)
    agent = Agent(paths=paths)
    return agent


def test_concept_extraction_and_crosslink(tmp_path):
    agent = setup_tmp(tmp_path)
    sample_raw = tmp_path / "data" / "raw" / "sample.txt"
    result = agent.ingest(str(sample_raw))
    # Ensure concepts are extracted
    concepts = result.get("concepts")
    assert concepts
    # Expect at least 'Rubik', 'God's', 'Number', 'Research', 'Reduction', 'Method', 'Yau', 'Rubik's', 'Revenge'
    assert any(c.startswith("Rubik") for c in concepts)
    # Ensure concept pages are created and contain reference to source
    for c in concepts:
        slug = c.lower().replace(" ", "-")
        concept_path = agent.wiki_manager.paths.wiki_dir / "concepts" / f"{slug}.md"
        assert concept_path.exists()
        content = concept_path.read_text(encoding="utf-8")
        assert "**Sources**" in content
        assert result["page"].endswith(".md")
        # Source slug appears in concept page
        source_slug = Path(result["page"]).stem
        assert source_slug in content


def test_search_and_maintain(tmp_path):
    agent = setup_tmp(tmp_path)
    sample_raw = tmp_path / "data" / "raw" / "sample.txt"
    agent.ingest(str(sample_raw))
    # Search for a term
    res = agent.search("Rubik God")
    assert res["results"], "Search should return at least one result"
    # Run maintenance and ensure no crash
    rep = agent.maintain()
    assert "maintenance" in rep