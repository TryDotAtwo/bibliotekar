"""
entity_id=providers_module; type=module; state=ready

LLM provider abstraction. Public API is stable:
    summarize(text) -> str
    answer(question, context) -> str

Provider replacement rule:
    local/self/OpenRouter/custom changes only provider construction.
    Agent API remains unchanged.
"""
from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

import requests

from .config import OpenRouterConfig


class BaseLLMProvider(ABC):
    """Stable LLM provider interface."""

    @abstractmethod
    def summarize(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def answer(self, question: str, context: str) -> str:
        raise NotImplementedError


class SelfProvider(BaseLLMProvider):
    """Provider used by tests and by ChatGPT-backed harnesses.

    A caller can inject a callable that acts as the LLM.  When no callable is
    supplied, the provider uses deterministic local fallbacks so the project
    remains testable without network access.
    """

    def __init__(self, summarizer: Optional[Callable[[str], str]] = None) -> None:
        self.summarizer = summarizer

    def summarize(self, text: str) -> str:
        if self.summarizer is not None:
            try:
                out = self.summarizer(text)
                if out:
                    return out
            except Exception:
                logging.exception("SelfProvider.summarizer failed")
        return _first_sentences(text, 3, 1000)

    def answer(self, question: str, context: str) -> str:
        if self.summarizer is not None:
            try:
                out = self.summarizer(f"Question:\n{question}\n\nContext:\n{context}")
                if out:
                    return out
            except Exception:
                logging.exception("SelfProvider.answer summarizer failed")
        # Deterministic fallback keeps enough context for tests and debugging.
        return context[:4000]


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider with retries and fallback-safe empty responses."""

    def __init__(self, config: OpenRouterConfig, retries: int = 3) -> None:
        self.config = config
        self.retries = retries

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.config.base_url}{endpoint}"
        for attempt in range(1, self.retries + 1):
            try:
                resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                if resp.status_code == 200:
                    return resp.json()
                logging.warning("openrouter_status=%s attempt=%s endpoint=%s", resp.status_code, attempt, endpoint)
            except Exception:
                logging.exception("openrouter_exception attempt=%s endpoint=%s", attempt, endpoint)
            time.sleep(2 ** (attempt - 1))
        return None

    def summarize(self, text: str) -> str:
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "Summarize the user text as a concise wiki note with explicit claims."},
                {"role": "user", "content": text[:12000]},
            ],
            "max_tokens": 700,
        }
        data = self._post("/chat/completions", payload)
        return _choice_text(data)

    def answer(self, question: str, context: str) -> str:
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "Answer using only the provided wiki context. Cite page names when possible."},
                {"role": "user", "content": f"QUESTION:\n{question}\n\nWIKI_CONTEXT:\n{context[:24000]}"},
            ],
            "max_tokens": 1200,
        }
        data = self._post("/chat/completions", payload)
        return _choice_text(data)


class CombinedProvider(BaseLLMProvider):
    """OpenRouter-first provider with deterministic self fallback."""

    def __init__(self, openrouter: OpenRouterConfig, summarizer: Optional[Callable[[str], str]] = None) -> None:
        self.self_provider = SelfProvider(summarizer)
        self.openrouter_provider = OpenRouterProvider(openrouter) if openrouter.api_key else None

    def summarize(self, text: str) -> str:
        if self.openrouter_provider is not None:
            out = self.openrouter_provider.summarize(text)
            if out:
                return out
        return self.self_provider.summarize(text)

    def answer(self, question: str, context: str) -> str:
        if self.openrouter_provider is not None:
            out = self.openrouter_provider.answer(question, context)
            if out:
                return out
        return self.self_provider.answer(question, context)


def _choice_text(data: Optional[Dict[str, Any]]) -> str:
    if not data:
        return ""
    choices = data.get("choices") or []
    if not choices:
        return ""
    msg = choices[0].get("message") or {}
    return (msg.get("content") or "").strip()


def _first_sentences(text: str, n: int, limit: int) -> str:
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    out = " ".join(sentences[:n]) if sentences and sentences[0] else text[:limit]
    return out[:limit] + ("…" if len(out) > limit else "")
