"""
entity_id=article_generator_module; type=module; state=initial

Module for generating scientific articles from wiki content or query results. Articles are rendered in LaTeX using a simple template and saved to disk. The caller can compile the LaTeX externally or convert to PDF. Markdown generation is supported as an alternative for lightweight use cases.
"""

from pathlib import Path
from typing import Iterable, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape  # type: ignore


def create_article_latex(title: str, sections: Iterable[Tuple[str, str]], output_path: Path) -> Path:
    """Generate a LaTeX article using a basic template.

    entity_id=create_article_latex_function; type=function; state=initial
    condition=sections_provided → action=render_latex → result=tex_file

    Parameters
    ----------
    title: str
        Article title.
    sections: Iterable[Tuple[str, str]]
        Sequence of (heading, body) pairs.
    output_path: Path
        Destination .tex file path.

    Returns
    -------
    Path
        Generated LaTeX file path.
    """
    env = Environment(
        loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
        autoescape=select_autoescape(enabled_extensions=("tex",)),
    )
    template = env.get_template("article.tex.j2")
    rendered = template.render(title=title, sections=list(sections))
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def create_article_markdown(title: str, sections: Iterable[Tuple[str, str]], output_path: Path) -> Path:
    """Generate a markdown article.

    entity_id=create_article_markdown_function; type=function; state=initial
    """
    lines = [f"# {title}", ""]
    for heading, body in sections:
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(body)
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path