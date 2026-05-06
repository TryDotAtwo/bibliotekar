# Bibliotekar

`Bibliotekar` is an autonomous LLM-centric librarian-secretary implementing Andrej Karpathy's **LLM Wiki** pattern.

Primary invariant: the repository is optimized for future maintenance by GPT-5.5 / Codex-like agents. Human ergonomics are secondary. Module boundaries, filenames, index files, and schema files exist to make future automated development fast and low-ambiguity.

## Status

- Working prototype: yes.
- Tests: `19 passed` in the current package.
- Included UI: CLI plus generated static dashboard.
- Included example wiki: God’s Number for the 4×4×4 Rubik’s Cube.
- Included LLM backends: self/mock summarizer, OpenRouter provider, combined fallback provider.
- Intended next maintainer: Codex/GPT-style code agent.

## Karpathy LLM Wiki mapping

| Karpathy element | Implementation |
|---|---|
| Raw sources | `bibliotekar_data/raw/` |
| Generated wiki | `bibliotekar_data/wiki/` |
| Schema/rules | `schema.md`, `AGENTS.md`, `docs/guidelines.md` |
| Ingest | `Agent.ingest()` |
| Query | `Agent.query()` |
| Lint | `Agent.lint()` |
| Maintain | `Agent.maintain()` |
| Index | `bibliotekar_data/wiki/index.md` |
| Log | `bibliotekar_data/wiki/log.md` |
| Crosslinks | `bibliotekar/linker.py`, concept backlinks |
| Contradictions | `bibliotekar/contradictions.py`, `wiki/synthesis/contradictions.md` |
| Search | `bibliotekar/search.py` |
| Dashboard | `bibliotekar/dashboard.py`, `bibliotekar_data/dashboard.html` |

## Repository map

Read `index.md` first. `index.md` is the fast navigation file for LLM/Codex maintainers.

Main files:

- `AGENTS.md` — mandatory instructions for Codex / agent maintainers.
- `schema.md` — operational schema for wiki behavior.
- `bibliotekar/agent.py` — main orchestrator.
- `bibliotekar/providers.py` — one stable API for self/OpenRouter/local-compatible LLM providers.
- `bibliotekar/wiki.py` — page creation, index, log, concept backlinks.
- `bibliotekar/search.py` — index-first wiki search.
- `bibliotekar/linker.py` — bidirectional link repair.
- `bibliotekar/contradictions.py` — contradiction ledger.
- `bibliotekar/dashboard.py` — static dashboard generation.
- `bibliotekar_ui.py` — CLI UI.
- `tests/` — test suite.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -e .
pip install pytest
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest
```

## Test

```bash
pytest -q
```

Expected result in this package:

```text
19 passed
```

## Run CLI

```bash
python bibliotekar_ui.py --base_dir ./bibliotekar_data
```

Menu capabilities:

- ingest file
- ask question
- search wiki
- list pages
- view page
- view index
- view log
- maintain wiki

## OpenRouter configuration

OpenRouter is optional. Without an API key, `SelfProvider` / fallback mode works.

```bash
export OPENROUTER_API_KEY="sk-or-..."
export OPENROUTER_MODEL="google/gemini-2.0-flash-exp:free"
```

Windows PowerShell:

```powershell
$env:OPENROUTER_API_KEY="sk-or-..."
$env:OPENROUTER_MODEL="google/gemini-2.0-flash-exp:free"
```

Provider API remains stable:

```python
provider.summarize(text) -> str
provider.answer(question, context) -> str
```

Changing local/OpenRouter/self backend should not require changes outside `bibliotekar/providers.py` or provider configuration.

## Example wiki

The package includes `bibliotekar_data/wiki/` with a prebuilt God’s Number 4×4 wiki.

Important pages:

- `bibliotekar_data/wiki/queries/query-god-s-number-4×4.md`
- `bibliotekar_data/wiki/concepts/god-s-number-4×4.md`
- `bibliotekar_data/wiki/synthesis/contradictions.md`
- `bibliotekar_data/wiki/index.md`
- `bibliotekar_data/wiki/log.md`

## Development rules

All agent messages and project records should follow AML-HIP style where practical:

```text
СУЩНОСТЬ:
entity_id=<id>; type=<type>; state=<state>

КОНТЕКСТ:
task_id=<id>; agent_id=<id>; memory_ref=[...]

ДЕЙСТВИЕ:
1. action=<type>; target=<entity_id>; params={...}
```

## Current limitations

- Concept extraction is heuristic, not semantic-perfect.
- Image/video understanding requires a real multimodal LLM provider.
- OpenRouter `/summarize` endpoint compatibility may require adapting provider payloads to the actual selected model/API.
- Dashboard is static HTML, not a live web server.
- This is ready for daily testing and iterative development, not a mature production SaaS.

## GitHub push

If GitHub CLI is configured:

```bash
git init
git add .
git commit -m "Initial Bibliotekar LLM Wiki implementation"
gh repo create bibliotekar --private --source=. --remote=origin --push
```

If remote already exists:

```bash
git remote add origin git@github.com:<OWNER>/bibliotekar.git
git branch -M main
git push -u origin main
```
