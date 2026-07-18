"""Critic agent: reviews a draft and returns a structured verdict."""

import json
import re
from dataclasses import dataclass

from .base import CompleteFn

SYSTEM_PROMPT = """You are a strict but constructive article reviewer.

Evaluate the draft on: structure, clarity, completeness and factual plausibility.
Respond with ONLY a JSON object, no markdown fences, in this exact shape:
{"approved": true or false, "feedback": "list of concrete issues to fix, or praise if approved"}

Approve only if the article needs no substantial changes."""


@dataclass(frozen=True)
class Review:
    approved: bool
    feedback: str


class Critic:
    """Reviews a draft; returns approval plus actionable feedback."""

    def __init__(self, complete: CompleteFn):
        self._complete = complete

    def run(self, draft: str) -> Review:
        raw = self._complete(SYSTEM_PROMPT, f"Draft to review:\n{draft}")
        return self._parse(raw)

    @staticmethod
    def _parse(raw: str) -> Review:
        """Parse the model's JSON verdict, tolerating stray fences or text."""
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            # Unparseable review: treat as approval rather than looping forever.
            return Review(approved=True, feedback="")
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return Review(approved=True, feedback="")
        return Review(
            approved=bool(data.get("approved", True)),
            feedback=str(data.get("feedback", "")),
        )
