# Development Notes

## Goal

`Bibliotekar` implements a persistent LLM-maintained wiki. The wiki is not plain RAG. New sources are compiled into durable pages, crosslinks, indexes, logs, contradictions and synthesis.

## Core invariants

1. Raw sources are immutable.
2. Wiki pages are LLM-owned.
3. Schema guides behavior.
4. Index is read before broad wiki scans.
5. Log is append-only.
6. Good answers are written back to the wiki.
7. Maintenance is explicit and testable.

## Provider invariant

Only the provider module should care whether the LLM is:

- current ChatGPT/self summarizer passed as callable,
- OpenRouter,
- future local model,
- mock test backend.

The rest of the code calls:

```python
provider.summarize(text)
provider.answer(question, context)
```

## Test policy

Add or update tests for every behavior change.

Current test command:

```bash
pytest -q
```

## Known next improvements

- Replace heuristic concept extraction with LLM JSON contract.
- Replace contradiction keyword scan with claim-level extraction.
- Add real image/video multimodal provider.
- Add FastAPI dashboard server if live UI becomes necessary.
- Add proper citations inside generated wiki pages.
