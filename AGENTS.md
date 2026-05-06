# AGENTS.md

СУЩНОСТЬ:
entity_id=codex_instructions; type=agent_rules; state=active

КОНТЕКСТ:
task_id=repository_maintenance; agent_id=codex_or_gpt; memory_ref=[README.md, index.md, schema.md, docs/guidelines.md]

ПРИОРИТЕТЫ:
1. priority=maximum; target=GPT-5.5_maintainability; human_ergonomics=secondary
2. priority=high; target=AML-HIP_communication; requirement=explicit_entities_and_low_ambiguity
3. priority=high; target=autonomous_librarian; user_role=request_or_correction_only
4. priority=high; target=stable_module_API; backend_changes_must_not_break_agent_API

ОБЯЗАТЕЛЬНЫЙ_ПОРЯДОК_РАБОТЫ:
1. action=read; target=index.md; reason=fast_navigation
2. action=read; target=schema.md; reason=wiki_behavior_rules
3. action=read; target=docs/guidelines.md; reason=project_rules
4. action=run_tests; target=pytest; reason=baseline
5. action=modify_smallest_relevant_files; target=repo; reason=LLM_maintainability
6. action=update_index_if_file_map_changes; target=index.md; reason=navigation_consistency
7. action=update_history_if_rule_or_architecture_changes; target=docs/history.md; reason=long_term_memory
8. action=run_tests; target=pytest; reason=verification

ФАЙЛЫ_НАВИГАЦИИ:
- file=index.md; role=repository_map
- file=schema.md; role=wiki_operation_contract
- file=docs/guidelines.md; role=project_rules
- file=docs/history.md; role=change_history
- file=README.md; role=user_and_agent_onboarding

МОДУЛИ:
- module=bibliotekar/agent.py; role=orchestration
- module=bibliotekar/providers.py; role=LLM_backend_abstraction
- module=bibliotekar/wiki.py; role=wiki_storage_index_log
- module=bibliotekar/search.py; role=index_first_retrieval
- module=bibliotekar/linker.py; role=bidirectional_link_repair
- module=bibliotekar/contradictions.py; role=contradiction_ledger
- module=bibliotekar/dashboard.py; role=static_observability
- module=bibliotekar/ingest.py; role=source_text_extraction
- module=bibliotekar/concept_extractor.py; role=concept_candidates
- module=bibliotekar_ui.py; role=CLI_UI

СТАБИЛЬНЫЙ_API:
- Agent.ingest(source_path: str) -> dict
- Agent.query(question: str) -> dict
- Agent.search(query: str, top_k: int = 5) -> dict
- Agent.lint() -> dict
- Agent.maintain() -> dict
- BaseLLMProvider.summarize(text: str) -> str
- BaseLLMProvider.answer(question: str, context: str) -> str

ЗАПРЕТЫ:
- forbidden=large_monolithic_files
- forbidden=hidden_global_state
- forbidden=unlogged_architecture_changes
- forbidden=changing_public_API_without_tests
- forbidden=removing_AML_HIP_project_memory
- forbidden=hardcoding_user_private_paths

ПРОВЕРКА:
- check=pytest; expected=all_passed
- check=index_updated; expected=true_when_file_map_changes
- check=schema_preserved; expected=true
- check=provider_swap_isolated; expected=true

СОХРАНЕНИЕ:
local_memory=true; shared_memory=true; index_keys=[task_id, entity_id, module, intent]
