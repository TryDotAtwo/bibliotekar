"""
entity_id=agent_module; type=module; state=ready

Autonomous library-secretary. Implements Karpathy LLM-Wiki pattern:
raw sources are immutable, wiki is persistent/compiled, schema guides behavior.
Operations: ingest, query, lint, maintain, search, dashboard.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .config import OpenRouterConfig, Paths
from .concept_extractor import extract_concepts
from .contradictions import scan_contradictions, write_ledger
from .dashboard import build_dashboard
from .ingest import UnsupportedFileTypeError, ingest_file
from .linker import repair_bidirectional_links
from .providers import CombinedProvider
from .search import read_context, search_wiki
from .utils import slugify
from .wiki import WikiManager


@dataclass
class Agent:
    """Autonomous library-secretary.

    entity_id=agent_class; type=class; state=ready
    condition=agent_initialized → action=instantiate_provider_and_wiki → result=agent_ready
    """

    paths: Paths = field(default_factory=Paths)
    openrouter: OpenRouterConfig = field(default_factory=OpenRouterConfig)
    wiki_manager: Optional[WikiManager] = None
    summarizer: Optional[Callable[[str], str]] = None
    provider: CombinedProvider = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.wiki_manager = self.wiki_manager or WikiManager(self.paths)
        self.provider = CombinedProvider(self.openrouter, self.summarizer)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create schema.md if missing."""
        if not self.paths.schema_file.exists():
            self.paths.schema_file.write_text(
                "# Bibliotekar Schema\n\n"
                "priority=LLM-maintainability\n"
                "communication=AML-HIP\n"
                "architecture=raw_sources|wiki|schema\n"
                "workflow_ingest=read_source→summarize→extract_concepts→create_source_page→update_concept_pages→crosslink→log\n"
                "workflow_query=read_index→search_pages→read_relevant_pages→answer→save_query_page\n"
                "workflow_lint=orphan_scan→contradiction_scan→write_reports\n",
                encoding="utf-8",
            )

    def ingest(self, source_path: str) -> Dict[str, Any]:
        """Ingest a raw source and update source/concept wiki pages."""
        path = Path(source_path)
        try:
            data = ingest_file(path)
        except UnsupportedFileTypeError as exc:
            logging.exception("unsupported_file_type")
            return {"error": str(exc)}

        text: str = data["text"]
        metadata = data["metadata"]
        summary = self.llm_summarize(text)
        concepts = extract_concepts(text + "\n" + summary)
        title = f"Source: {metadata['filename']}"
        source_slug = slugify(title)

        concept_lines: List[str] = []
        for concept in concepts[:30]:
            c_slug = slugify(concept)
            concept_lines.append(f"- [{concept}](../concepts/{c_slug}.md)")
            self.wiki_manager.update_concept_page(concept, source_slug)  # type: ignore[union-attr]

        raw_excerpt = text[:3000]
        content = (
            f"**File:** {metadata['filename']}\n\n"
            f"**Hash:** {metadata['hash']}\n\n"
            f"**Summary**\n{summary}\n\n"
            f"**Concepts**\n" + ("\n".join(concept_lines) if concept_lines else "- none") + "\n\n"
            f"**Raw excerpt**\n\n{raw_excerpt}\n"
        )
        page_path = self.wiki_manager.create_page("sources", title, content)  # type: ignore[union-attr]
        repair = repair_bidirectional_links(self.paths.wiki_dir)
        return {"page": str(page_path), "summary": summary, "concepts": concepts, "repair": repair}

    def search(self, query: str, top_k: int = 8) -> Dict[str, Any]:
        """Index-first search over wiki pages."""
        results = search_wiki(self.paths.wiki_dir, query, top_k=top_k)
        return {"results": [(str(path), score) for path, score in results]}

    def query(self, question: str) -> Dict[str, Any]:
        """Answer a question using index-first retrieval, then save answer in wiki."""
        results = search_wiki(self.paths.wiki_dir, question, top_k=8)
        context = read_context(results)
        if not context:
            context = self._read_index_and_log()
        answer = self.llm_answer(question, context)
        title = f"Query: {question[:70]}"
        citations = "\n".join(f"- {Path(str(path)).name}; score={score}" for path, score in results)
        content = f"{answer}\n\n**Used pages**\n{citations if citations else '- none'}\n"
        page_path = self.wiki_manager.create_page("queries", title, content)  # type: ignore[union-attr]
        return {"answer": answer, "page": str(page_path), "used_pages": citations}

    def lint(self) -> Dict[str, Any]:
        """Health-check wiki: orphans, contradictions, stale-looking pages."""
        pages = self.wiki_manager.list_pages()  # type: ignore[union-attr]
        issues: List[str] = []
        text_all = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in pages)
        for p in pages:
            slug = p.stem
            if text_all.count(slug) <= 1 and p.parent.name != "sources":
                issues.append(f"orphan_page={p.relative_to(self.paths.wiki_dir)}")

        contradictions = scan_contradictions(self.paths.wiki_dir)
        ledger = write_ledger(self.paths.wiki_dir, contradictions)
        if issues:
            self.wiki_manager.create_page("synthesis", "Lint Report", "\n".join(f"- {x}" for x in issues))  # type: ignore[union-attr]
        self.wiki_manager._append_log_entry("lint", "synthesis", f"issues={len(issues)} contradictions={len(contradictions)}")  # type: ignore[union-attr]
        return {"issues": issues, "contradictions": contradictions, "ledger": str(ledger)}

    def maintain(self) -> Dict[str, Any]:
        """Self-healing pass: repair backlinks and run lint."""
        links = repair_bidirectional_links(self.paths.wiki_dir)
        lint = self.lint()
        dashboard = build_dashboard(self.paths.base_dir)
        return {"maintenance": links.get("added", []), "links": links, "lint": lint, "dashboard": str(dashboard)}

    def build_dashboard(self) -> Path:
        """Build static dashboard.html for observing wiki state."""
        return build_dashboard(self.paths.base_dir)

    def llm_summarize(self, text: str) -> str:
        """Provider-backed summarization."""
        try:
            out = self.provider.summarize(text)
            if out:
                return out
        except Exception:
            logging.exception("llm_summarize_failed")
        return text[:1000]

    def llm_answer(self, question: str, context: str) -> str:
        """Provider-backed question answering."""
        # Deterministic no-network path keeps exact context for tests and maintenance.
        if self.summarizer is None and not self.openrouter.api_key:
            return context[:4000]
        try:
            out = self.provider.answer(question, context)
            if out:
                return out
        except Exception:
            logging.exception("llm_answer_failed")
        return context[:4000]

    def _read_index_and_log(self) -> str:
        parts = []
        for path in [self.paths.index_file, self.paths.log_file]:
            if path.exists():
                parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        return "\n\n".join(parts)
