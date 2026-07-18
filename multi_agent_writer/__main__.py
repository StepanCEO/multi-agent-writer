"""CLI entry point: ``python -m multi_agent_writer "your topic"``."""

import argparse
import logging
import re
import sys
from pathlib import Path

from openai import OpenAIError

from .config import load_settings
from .llm import LLMClient
from .pipeline import run_pipeline


def _slugify(text: str) -> str:
    slug = re.sub(r"[^\w]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    return slug[:60] or "article"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="multi_agent_writer",
        description="Write an article on a topic using a researcher/writer/critic/editor agent pipeline.",
    )
    parser.add_argument("topic", help="Article topic, e.g. \"Why RAG beats fine-tuning for FAQs\"")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="Output .md path (default: output/<topic-slug>.md)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress logs")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(message)s",
    )

    try:
        settings = load_settings()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    client = LLMClient(settings)
    try:
        result = run_pipeline(args.topic, client.complete, max_revisions=settings.max_revisions)
    except OpenAIError as exc:
        print(f"OpenAI API error: {exc}", file=sys.stderr)
        return 1

    out_path = args.output or Path("output") / f"{_slugify(args.topic)}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.article, encoding="utf-8")

    print(f"\nDone: {out_path} (revisions: {result.revisions})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
