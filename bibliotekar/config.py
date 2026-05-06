"""
entity_id=config_module; type=module; state=initial

Configuration parameters, environment variables, and project rules for the autonomous library‑secretary. This module centralizes configurable values and persistent guidelines. Amendments to project rules should update ``docs/history.md`` and maintain backward compatibility via default values when possible.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Paths:
    """File system locations for raw sources, wiki, and schema.

    entity_id=paths_dataclass; type=config_entity; state=initial
    """
    base_dir: Path = Path(os.getenv("BIBLIOTEKAR_BASE", "/home/oai/share/bibliotekar_data"))
    raw_dir: Path = field(init=False)
    wiki_dir: Path = field(init=False)
    schema_file: Path = field(init=False)
    index_file: Path = field(init=False)
    log_file: Path = field(init=False)

    def __post_init__(self):  # type: ignore[override]
        object.__setattr__(self, "raw_dir", self.base_dir / "raw")
        object.__setattr__(self, "wiki_dir", self.base_dir / "wiki")
        object.__setattr__(self, "schema_file", self.base_dir / "schema.md")
        object.__setattr__(self, "index_file", self.wiki_dir / "index.md")
        object.__setattr__(self, "log_file", self.wiki_dir / "log.md")


@dataclass
class OpenRouterConfig:
    """Configuration for connecting to OpenRouter endpoints.

    entity_id=openrouter_config; type=config_entity; state=initial
    """
    api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    model: str = os.getenv("OPENROUTER_MODEL", "pplx-llama-3")
    base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


@dataclass
class ProjectRules:
    """Persistent project rules loaded from the guidelines document.

    entity_id=project_rules; type=config_entity; state=initial
    """
    rules: List[str] = field(default_factory=list)

    def load_default(self) -> None:
        """Load baseline rules derived from the Karpathy LLM‑Wiki pattern and user instructions.

        condition=no_rules_loaded → action=load_defaults → result=rules_populated
        """
        default_rules = [
            "Three‑layer architecture: raw sources (immutable), wiki (LLM‑generated markdown), schema (instructions)",
            "Operations: ingest, query, lint with persistent wiki updates",
            "Index.md for content catalog; log.md for chronological events",
            "AML‑HIP communication protocol for all agent messages",
            "LLM‑centric code maintainability prioritized over human readability",
            "Modular design: each external integration resides in a dedicated module"
        ]
        self.rules.extend(default_rules)