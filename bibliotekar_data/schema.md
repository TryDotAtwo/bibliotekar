# Bibliotekar Schema

entity_id=schema; type=operational_rules; state=ready

PRIORITIES:
- maintainability_for_GPT_5_5=max
- AML_HIP=true
- autonomy=true
- stable_module_API=true

LAYERS:
- raw_sources: immutable curated input files
- wiki: generated/maintained markdown knowledge base
- schema: rules and workflows for agent behavior

WORKFLOWS:
- ingest: read raw source, summarize, extract concepts, write source page, update concept pages, repair links, update index, append log
- query: read index, search relevant pages, synthesize answer, save query page
- lint: find orphans, detect contradiction markers, write contradiction ledger
- maintain: repair bidirectional links, run lint, build dashboard

PAGE_FORMATS:
- source_page: file, hash, summary, concepts, raw excerpt
- concept_page: concept, source backlinks
- query_page: answer, used pages
- synthesis_page: report or ledger
