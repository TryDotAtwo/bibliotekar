# Project Guidelines

entity_id=guidelines_document; type=document; state=ready

## Fixed Priority Rules

- priority_1=GPT-5.5-maintainability; human_convenience=irrelevant
- communication_protocol=AML-HIP-only
- autonomy=library-secretary owns wiki maintenance; user asks/requests/edits; program may ask clarification when necessary
- module_api=stable; provider_change_only_in_provider_layer; local/self/OpenRouter backends share summarize/answer interface
- file_style=small_files; descriptive_names; index_first_navigation

## Karpathy LLM-Wiki Pattern

- raw_sources=immutable; location=raw/
- wiki=LLM-generated markdown; location=wiki/
- schema=operational rules and conventions; location=schema.md
- ingest=source→summary→concepts→source_page→concept_pages→bidirectional_links→index→log
- query=index_first_search→relevant_pages→answer→query_page
- lint=orphan_scan→contradiction_scan→ledger→lint_report
- maintain=repair_crosslinks→lint→dashboard
- dashboard=static_observation_UI; file=dashboard.html

## Page Types

- sources: one page per raw source; contains metadata, hash, summary, concepts, raw excerpt
- concepts: one page per concept/entity; contains backlinks to sources
- queries: saved answers that become wiki artifacts
- synthesis: lint reports, contradiction ledger, high-level summaries

## Testing Rules

- every core module has tests
- tests cover unit, integration, stability, search, crosslinks, provider fallback, dashboard-related maintenance
- no network required for tests
