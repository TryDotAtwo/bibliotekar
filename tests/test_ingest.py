"""
Tests for the ingest module.
"""

from pathlib import Path
import tempfile

import bibliotekar.ingest as ingest


def test_ingest_text_file(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    content = "Hello world\nThis is a test file."
    file_path.write_text(content)
    result = ingest.ingest_file(file_path)
    assert "text" in result
    assert result["text"].startswith("Hello")
    assert "metadata" in result
    assert result["metadata"]["filename"] == "sample.txt"


def test_ingest_unsupported_file(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.xyz"
    file_path.write_text("dummy")
    try:
        ingest.ingest_file(file_path)
    except ingest.UnsupportedFileTypeError:
        return
    assert False, "UnsupportedFileTypeError expected"