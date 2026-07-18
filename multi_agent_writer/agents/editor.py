"""Editor agent: final stylistic pass over the approved draft."""

from .base import CompleteFn

SYSTEM_PROMPT = """You are a meticulous copy editor doing the final pass on an article.

Polish grammar, punctuation and flow. Do NOT change the meaning or structure.
Make sure the article starts with a single `# Title` line.
Return only the final markdown article, in the same language as the draft."""


class Editor:
    """Applies the final polish and guarantees a markdown title."""

    def __init__(self, complete: CompleteFn):
        self._complete = complete

    def run(self, draft: str) -> str:
        return self._complete(SYSTEM_PROMPT, f"Article to polish:\n{draft}")
