"""
Tests for the Agent class.
"""

from pathlib import Path

from bibliotekar.agent import Agent


def test_agent_ingest_and_query(tmp_path: Path) -> None:
    # Setup custom paths for the agent
    from bibliotekar.config import Paths

    class TmpPaths(Paths):
        def __init__(self, base_dir: Path) -> None:
            object.__setattr__(self, "base_dir", base_dir)
            super().__post_init__()

    paths = TmpPaths(tmp_path)
    agent = Agent(paths=paths)
    # Create a simple text file
    source_file = tmp_path / "raw.txt"
    source_file.write_text("Test data for ingestion.")
    result = agent.ingest(str(source_file))
    assert "summary" in result
    assert "page" in result
    # Query should create a new page
    response = agent.query("What is in the wiki?")
    assert "answer" in response
    assert "page" in response