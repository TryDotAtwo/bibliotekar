# Usage

## CLI

```bash
python bibliotekar_ui.py --base_dir ./bibliotekar_data
```

## Python API

```python
from bibliotekar.agent import Agent
from bibliotekar.config import Paths

agent = Agent(paths=Paths(base_dir="bibliotekar_data"))
agent.ingest("some_source.md")
result = agent.query("What changed?")
print(result["answer"])
```

## Custom self-provider

```python
def self_summarizer(text: str) -> str:
    return text[:1000]

agent = Agent(paths=Paths(base_dir="bibliotekar_data"), summarizer=self_summarizer)
```

## OpenRouter

```bash
export OPENROUTER_API_KEY="sk-or-..."
export OPENROUTER_MODEL="google/gemini-2.0-flash-exp:free"
```

```python
from bibliotekar.agent import Agent
agent = Agent()
```
