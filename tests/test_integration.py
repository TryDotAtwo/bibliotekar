"""
Integration test for the agent across ingestion, wiki update, and query answering.
"""

from pathlib import Path

from bibliotekar.agent import Agent
from bibliotekar.config import Paths


def test_ingest_and_query_integration(tmp_path: Path) -> None:
    # Set up custom paths
    class TmpPaths(Paths):
        def __init__(self, base_dir: Path) -> None:
            object.__setattr__(self, "base_dir", base_dir)
            super().__post_init__()

    paths = TmpPaths(tmp_path)
    agent = Agent(paths=paths)
    # Prepare two sources: one text and one markdown
    # Ensure raw directory exists
    paths.raw_dir.mkdir(parents=True, exist_ok=True)
    src1 = paths.raw_dir / "info1.txt"
    src1.write_text("The 4x4 Rubik's cube is also known as the Rubik's Revenge. It requires algorithms that reduce it to a 3x3 state and fix parity errors.")
    src2 = paths.raw_dir / "info2.md"
    src2.write_text("To solve a 4x4, first solve the center pieces, then pair up edge pieces, then solve it like a 3x3. Be mindful of parity errors.")
    # Ingest both sources
    result1 = agent.ingest(str(src1))
    result2 = agent.ingest(str(src2))
    assert "summary" in result1 and result1["summary"]
    assert "summary" in result2 and result2["summary"]
    # Query about the topic
    response = agent.query("How to solve a 4x4 Rubik's cube optimally?")
    assert "answer" in response and response["answer"]
    # The answer should mention "3x3" because the sources reference solving like a 3x3
    assert "3x3" in response["answer"] or "Rubik" in response["answer"]