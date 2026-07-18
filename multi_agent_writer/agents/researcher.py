"""Researcher agent: turns a topic into an outline with key points."""

from .base import CompleteFn

SYSTEM_PROMPT = """You are a research assistant preparing material for an article writer.

Given a topic, produce:
1. A one-sentence angle for the article.
2. An outline of 4-6 sections with short titles.
3. Under each section, 2-4 concrete key points or facts to cover.

Be specific and factual. Do not write the article itself.
Answer in the same language as the topic."""


class Researcher:
    """Produces an outline and key points for a given topic."""

    def __init__(self, complete: CompleteFn):
        self._complete = complete

    def run(self, topic: str) -> str:
        return self._complete(SYSTEM_PROMPT, f"Topic: {topic}")
