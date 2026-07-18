"""Thin wrapper around the OpenAI chat completions API.

Keeping all API access behind one function makes agents trivial to test:
tests inject a fake ``complete`` callable instead of hitting the network.
"""

from openai import OpenAI

from .config import Settings


class LLMClient:
    """Small facade over the OpenAI SDK used by every agent."""

    def __init__(self, settings: Settings):
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.model
        self._temperature = settings.temperature

    def complete(self, system: str, user: str) -> str:
        """Send one system+user exchange and return the assistant text."""
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""
