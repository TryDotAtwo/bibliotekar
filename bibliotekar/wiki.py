"""
entity_id=wiki_module; type=module; state=initial

Management of the wiki layer. Provides functions to create pages, update the index, append log entries, and manage cross‑references. Each page is stored as a markdown file under the wiki directory; categories correspond to subdirectories (e.g. ``entities/``, ``concepts/``, ``sources/``, ``queries/``, ``synthesis/``). The index and log files are maintained automatically.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Optional

from .config import Paths
from .utils import ensure_dirs, slugify

# For typing within update_concept_page
from typing import Set


class WikiManager:
    """High‑level API for writing and maintaining wiki pages.

    entity_id=wiki_manager; type=class; state=initial
    condition=paths_provided → action=ensure_directories → result=manager_ready
    """

    def __init__(self, paths: Optional[Paths] = None) -> None:
        self.paths = paths or Paths()
        ensure_dirs([
            self.paths.raw_dir,
            self.paths.wiki_dir,
            self.paths.wiki_dir / "entities",
            self.paths.wiki_dir / "concepts",
            self.paths.wiki_dir / "sources",
            self.paths.wiki_dir / "queries",
            self.paths.wiki_dir / "synthesis",
            self.paths.wiki_dir / ".drafts",
        ])

    def create_page(self, category: str, title: str, content: str) -> Path:
        """Create or overwrite a wiki page.

        Pages are stored at ``wiki/{category}/{slug}.md``. This function updates the index and log accordingly.

        entity_id=create_page_method; type=method; state=initial

        Parameters
        ----------
        category: str
            One of 'entities', 'concepts', 'sources', 'queries', 'synthesis'.
        title: str
            Human‑readable page title (used for heading and slug).
        content: str
            Markdown content to write to the page.

        Returns
        -------
        Path
            Filesystem path to the created page.
        """
        if category not in {"entities", "concepts", "sources", "queries", "synthesis"}:
            raise ValueError(f"Invalid category {category}")
        slug = slugify(title)
        file_path = self.paths.wiki_dir / category / f"{slug}.md"
        # Compose page with heading
        page_text = f"# {title}\n\n{content}\n"
        file_path.write_text(page_text, encoding="utf-8")
        self._append_index_entry(category, title, slug)
        self._append_log_entry("create", category, title)
        return file_path

    # Concept page helper
    def update_concept_page(self, concept: str, source_slug: str) -> Path:
        """Create or update a concept page with a new source reference.

        entity_id=update_concept_page; type=method; state=initial
        condition=concept_provided → action=create_or_update_page → result=concept_page_path

        Parameters
        ----------
        concept: str
            The concept name.
        source_slug: str
            Slug of the source page referencing this concept.

        Returns
        -------
        Path
            Path to the concept page.
        """
        # Slugify concept for filename
        slug = slugify(concept)
        file_path = self.paths.wiki_dir / "concepts" / f"{slug}.md"
        # Link to source page relative path
        source_link = f"../sources/{source_slug}.md"
        if file_path.exists():
            # Update existing page: append source if not listed
            content = file_path.read_text(encoding="utf-8")
            # Find Sources section
            lines = content.splitlines()
            new_lines: list[str] = []
            in_sources = False
            sources_found: Set[str] = set()
            for line in lines:
                if line.strip().lower().startswith("**sources**"):
                    in_sources = True
                    new_lines.append(line)
                    continue
                if in_sources and line.startswith("-"):
                    # parse existing link to capture slug
                    parts = line.split("(")
                    if len(parts) > 1:
                        link_part = parts[1].split(")")[0]
                        sources_found.add(link_part)
                    new_lines.append(line)
                    continue
                new_lines.append(line)
            # If the new source link not recorded, append bullet
            if source_link not in sources_found:
                # Insert into sources section
                inserted = False
                updated_lines: list[str] = []
                for line in new_lines:
                    updated_lines.append(line)
                    if line.strip().lower().startswith("**sources**"):
                        updated_lines.append(f"- [{source_slug}]({source_link})")
                        inserted = True
                if not inserted:
                    # Sources section missing; append at end
                    updated_lines.append("**Sources**")
                    updated_lines.append(f"- [{source_slug}]({source_link})")
                file_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
        else:
            # Create new concept page with header and sources section
            content = []
            content.append(f"# {concept}\n")
            content.append(f"**Concept:** {concept}\n")
            content.append("**Sources**")
            content.append(f"- [{source_slug}]({source_link})")
            file_path.write_text("\n".join(content) + "\n", encoding="utf-8")
            # Add index and log entries
            self._append_index_entry("concepts", concept, slug)
            self._append_log_entry("create", "concepts", concept)
        return file_path

    def update_page(self, category: str, title: str, content: str) -> Path:
        """Overwrite an existing page and update log but not index (index contains summary only)."""
        return self.create_page(category, title, content)

    def _append_index_entry(self, category: str, title: str, slug: str) -> None:
        """Append a new entry to index.md with one‑line summary placeholder."""
        index_path = self.paths.index_file
        if not index_path.exists():
            index_path.write_text("# Index\n\n", encoding="utf-8")
        date_str = _dt.date.today().isoformat()
        line = f"- {date_str} | {category}/{slug}.md | {title}\n"
        with index_path.open("a", encoding="utf-8") as f:
            f.write(line)

    def _append_log_entry(self, action: str, category: str, title: str) -> None:
        """Append a log entry with timestamp."""
        log_path = self.paths.log_file
        if not log_path.exists():
            log_path.write_text("# Log\n\n", encoding="utf-8")
        timestamp = _dt.datetime.now().isoformat(timespec="seconds")
        line = f"## [{timestamp}] {action} | {category} | {title}\n"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line)

    def list_pages(self, category: Optional[str] = None) -> list[Path]:
        """Return a list of page paths, optionally filtered by category."""
        base = self.paths.wiki_dir
        if category:
            target = base / category
            return list(target.glob("*.md"))
        pages: list[Path] = []
        for cat in ["entities", "concepts", "sources", "queries", "synthesis"]:
            pages.extend((base / cat).glob("*.md"))
        return pages