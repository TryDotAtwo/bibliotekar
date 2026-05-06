"""
Tests for stability features such as fallback summarization and error handling in ingestion.
"""

from pathlib import Path

import pytest

from bibliotekar.agent import Agent
from bibliotekar.config import Paths, OpenRouterConfig
from bibliotekar import ingest as ingest_mod


def test_llm_summarize_fallback(tmp_path: Path) -> None:
    """Ensure that llm_summarize falls back to a naive summarizer when remote API calls fail."""
    # Create an agent with an invalid OpenRouter configuration to force remote failure
    class TmpPaths(Paths):
        def __init__(self, base_dir: Path) -> None:
            object.__setattr__(self, "base_dir", base_dir)
            super().__post_init__()

    paths = TmpPaths(tmp_path)
    # Provide an invalid base_url to trigger errors
    bad_openrouter = OpenRouterConfig(api_key="dummy", base_url="http://localhost:9999", model="gpt-3")
    agent = Agent(paths=paths, openrouter=bad_openrouter)
    # A sample text with multiple sentences
    text = "Sentence one. Sentence two? Sentence three! Sentence four."
    summary = agent.llm_summarize(text)
    # Expect the naive summarizer to select the first three sentences
    assert "Sentence one." in summary
    assert "Sentence two?" in summary or "Sentence three!" in summary


def test_ingest_error_handling_with_docx(monkeypatch, tmp_path: Path) -> None:
    """Verify that ingest_file handles extraction errors gracefully for DOCX files."""
    # Prepare a fake DOCX file (actually plain text) to trigger extraction failure
    docx_path = tmp_path / "bad.docx"
    docx_path.write_text("not a real docx")
    # Monkeypatch docx2txt.process to raise an exception
    def raise_error(path: str) -> str:
        raise RuntimeError("docx parsing failed")

    monkeypatch.setattr(ingest_mod.docx2txt, "process", raise_error)
    result = ingest_mod.ingest_file(docx_path)
    # Text should be empty due to fallback
    assert result["text"] == ""
    assert result["metadata"]["filename"] == "bad.docx"