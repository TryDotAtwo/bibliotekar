# Project History

entity_id=history_document; type=document; state=initial

This document logs all changes to the project guidelines, configuration, and schema. Each entry must include a timestamp (ISO 8601), the author (agent identifier), and a summary of the modification.

## [2026-05-06] Initial commit

* Added baseline project guidelines derived from Karpathy's LLM‑Wiki pattern and user instructions.
* Established AML‑HIP protocol for all agent communications.
* Defined three‑layer architecture and core operations (ingest, query, lint).
* Outlined integration modules for Notion, Google Calendar, presentation generation, scientific article generation, and image/infographic generation.
* Implemented configuration classes in ``bibliotekar/config.py``.
* Created repository skeleton with modules, tests directory, and documentation.

## [2026-05-06] v9 production hardening

* Added provider abstraction as stable API for self/local/OpenRouter backends.
* Added index-first wiki search.
* Added bidirectional source↔concept crosslink repair.
* Added structured contradiction ledger.
* Added static dashboard generation.
* Added maintenance/self-healing pass.
* Added prebuilt 4x4 God's number wiki pages.
* Added pyproject entry point.
* Updated guidelines with fixed user priorities.
## [2026-05-06] GitHub-ready documentation pass

* Added README.md for human and agent onboarding.
* Added AGENTS.md for Codex/GPT maintainer instructions.
* Added docs/development.md with architecture invariants and next improvement list.
* Added docs/usage.md with CLI and Python API examples.
* Added .gitignore.
* Updated pyproject.toml with build-system, dependencies, dev extras, and CLI entry point.
* Preserved Karpathy LLM Wiki pattern: raw sources, wiki, schema, ingest, query, lint, index, log, maintenance.
