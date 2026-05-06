"""
Tests for the wiki manager.
"""

from pathlib import Path
import tempfile

from bibliotekar.wiki import WikiManager


def test_create_page(tmp_path: Path) -> None:
    # Use custom paths pointing to tmp directory
    class TmpPaths:
        def __init__(self, base: Path) -> None:
            self.base_dir = base
            self.raw_dir = base / "raw"
            self.wiki_dir = base / "wiki"
            self.schema_file = base / "schema.md"
            self.index_file = self.wiki_dir / "index.md"
            self.log_file = self.wiki_dir / "log.md"

    paths = TmpPaths(tmp_path)
    manager = WikiManager(paths)
    page = manager.create_page("entities", "Test Entity", "Content here")
    assert page.exists()
    index_lines = manager.paths.index_file.read_text().splitlines()
    assert any("Test Entity" in line for line in index_lines)
    log_text = manager.paths.log_file.read_text()
    assert "create | entities" in log_text