"""Writer agent: turns research notes into a draft, and revises after review."""

from .base import CompleteFn

SYSTEM_PROMPT = """You are a professional article writer.

Write a well-structured markdown article based on the research notes you are given.
Rules:
- Use markdown headers for sections.
- Clear, engaging prose; no filler phrases.
- 600-900 words.
- Answer in the same language as the research notes."""

REVISE_PROMPT = """You are a professional article writer revising your own draft.

You are given your previous draft and reviewer feedback.
Rewrite the article addressing every point of the feedback.
Keep the same language, markdown structure and 600-900 word length."""


class Writer:
    """Writes the first draft and revises it based on critic feedback."""

    def __init__(self, complete: CompleteFn):
        self._complete = complete

    def draft(self, topic: str, research: str) -> str:
        user = f"Topic: {topic}\n\nResearch notes:\n{research}"
        return self._complete(SYSTEM_PROMPT, user)

    def revise(self, draft: str, feedback: str) -> str:
        user = f"Previous draft:\n{draft}\n\nReviewer feedback:\n{feedback}"
        return self._complete(REVISE_PROMPT, user)
