"""
Integration test for researching the 4x4 Rubik's cube God's number using the agent.

This test verifies that a custom summarizer can be injected into the agent and
that ingesting a source about God's number produces a wiki entry and answer
with relevant bounds. The custom summarizer simulates ChatGPT summarization.
"""

from pathlib import Path

from bibliotekar.agent import Agent
from bibliotekar.config import Paths


def test_gods_number_research(tmp_path: Path) -> None:
    class TmpPaths(Paths):
        def __init__(self, base_dir: Path) -> None:
            object.__setattr__(self, "base_dir", base_dir)
            super().__post_init__()

    # Define a manual summarizer simulating ChatGPT summarization of God's number research
    def manual_summarizer(text: str) -> str:
        return (
            "God's number for the 4×4 cube (Rubik's Revenge) remains unknown. "
            "Current research places it between 35 and 55 moves in the outer block turn metric, "
            "between 32 and 53 moves in the single slice turn metric, and between 29 and 53 moves in the block turn metric. "
            "Recent conjectures suggest an optimal quarter‑turn metric of 48 moves and a half‑turn metric of 41 moves."
        )

    paths = TmpPaths(tmp_path)
    agent = Agent(paths=paths, summarizer=manual_summarizer)
    # Create raw directory and a source file summarising research on God's number
    paths.raw_dir.mkdir(parents=True, exist_ok=True)
    file_path = paths.raw_dir / "gods_number_4x4.txt"
    file_path.write_text(
        "Research on the 4×4 Rubik's cube God's number is ongoing. It remains unknown but bounds exist: "
        "outer block turn metric 35–55, single slice turn metric 32–53, block turn metric 29–53. "
        "Conjectures from 2025 suggest quarter‑turn metric 48 and half‑turn metric 41."
    )
    # Ingest the file
    result = agent.ingest(str(file_path))
    assert "summary" in result and "35" in result["summary"]
    # Query the wiki about God's number
    response = agent.query("What is the God’s number for the 4×4 cube?")
    answer = response.get("answer", "").lower()
    # Check that the answer includes some of the bounds
    assert "35" in answer or "55" in answer
    assert "unknown" in answer or "remains" in answer or "conjectures" in answer