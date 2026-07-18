"""Configuration loaded from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the pipeline."""

    openai_api_key: str
    model: str = "gpt-4o-mini"
    max_revisions: int = 2
    temperature: float = 0.7


def load_settings() -> Settings:
    """Read settings from the environment, failing fast on a missing key."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return Settings(
        openai_api_key=api_key,
        model=os.getenv("MODEL", "gpt-4o-mini"),
        max_revisions=int(os.getenv("MAX_REVISIONS", "2")),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
    )
