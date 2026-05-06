"""
entity_id=package_bibliotekar; type=python_package; state=initial

This package implements an autonomous library-secretary agent inspired by Andrej Karpathy's LLM‑Wiki pattern. It is composed of modular components that ingest heterogeneous raw sources, maintain a persistent interlinked markdown wiki, answer queries, and integrate with external services. All internal communications follow the Autistic Meta‑Language High‑Information Protocol (AML‑HIP).

Contents:
    - ingest.py: Source ingestion utilities for various file types.
    - wiki.py: Wiki storage management and page operations.
    - agent.py: Core agent orchestrating ingestion, query, lint, and external modules.
    - aml_hip.py: Message formatting and validation according to AML‑HIP.
    - notion_integration.py: Stub for Notion API interactions.
    - gcal_integration.py: Stub for Google Calendar API interactions.
    - presentation_generator.py: Generation of slide decks using markdown and Marp.
    - article_generator.py: Generation of scientific articles in LaTeX or markdown.
    - image_generator.py: Generation of images or infographics.
    - utils.py: Utility functions shared across modules.
    - config.py: Configuration definitions and persistent project rules.

Tests reside in the ``tests`` directory and ensure behavior correctness, message format compliance, and deterministic operations. Configuration files and project rules are stored in ``docs/guidelines.md`` and ``docs/history.md``.
"""

from . import aml_hip  # noqa: F401  # ensure module registration