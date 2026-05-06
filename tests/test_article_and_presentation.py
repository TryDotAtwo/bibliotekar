"""
Tests for article and presentation generation modules.

These tests verify that LaTeX and markdown articles are generated correctly,
and that PowerPoint presentations are created with the expected number of slides.
"""

from pathlib import Path

import pytest
from pptx import Presentation  # type: ignore

from bibliotekar.article_generator import create_article_latex, create_article_markdown
from bibliotekar.presentation_generator import create_presentation


def test_create_article_markdown_and_latex(tmp_path: Path) -> None:
    title = "Test Article"
    sections = [("Section One", "This is the first section."), ("Section Two", "Another section.")]
    md_path = tmp_path / "article.md"
    tex_path = tmp_path / "article.tex"
    # Generate Markdown and LaTeX articles
    md_result = create_article_markdown(title, sections, md_path)
    tex_result = create_article_latex(title, sections, tex_path)
    # Verify files exist and contain the title
    assert md_result.exists()
    assert tex_result.exists()
    assert title in md_result.read_text(encoding="utf-8")
    assert title in tex_result.read_text(encoding="utf-8")


def test_create_presentation(tmp_path: Path) -> None:
    title = "Demo Presentation"
    sections = [("Slide 1", "Content of slide one."), ("Slide 2", "Content of slide two.")]
    pptx_path = tmp_path / "demo.pptx"
    create_presentation(title, sections, pptx_path)
    assert pptx_path.exists()
    # Load presentation and check number of slides
    pres = Presentation(str(pptx_path))
    # Should have 1 title slide + len(sections) slides
    assert len(pres.slides) == 1 + len(sections)