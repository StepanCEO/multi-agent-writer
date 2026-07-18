"""Pipeline orchestration: researcher -> writer <-> critic -> editor."""

import logging
from dataclasses import dataclass, field

from .agents import Critic, Editor, Researcher, Writer
from .agents.base import CompleteFn

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Final article plus a trace of what happened along the way."""

    article: str
    research: str
    revisions: int
    reviews: list[str] = field(default_factory=list)


def run_pipeline(topic: str, complete: CompleteFn, max_revisions: int = 2) -> PipelineResult:
    """Run the full multi-agent pipeline for a topic.

    The writer drafts, the critic reviews; if the critic rejects, the writer
    revises — up to ``max_revisions`` times. The editor always does the final
    pass, even if the critic never approved (best effort beats no article).
    """
    researcher = Researcher(complete)
    writer = Writer(complete)
    critic = Critic(complete)
    editor = Editor(complete)

    logger.info("Researcher: gathering key points for %r", topic)
    research = researcher.run(topic)

    logger.info("Writer: drafting")
    draft = writer.draft(topic, research)

    reviews: list[str] = []
    revisions = 0
    for attempt in range(max_revisions + 1):
        logger.info("Critic: reviewing draft (attempt %d)", attempt + 1)
        review = critic.run(draft)
        reviews.append(review.feedback)
        if review.approved:
            logger.info("Critic: approved")
            break
        if revisions >= max_revisions:
            logger.info("Critic: rejected, but revision limit reached")
            break
        revisions += 1
        logger.info("Writer: revising (revision %d of %d)", revisions, max_revisions)
        draft = writer.revise(draft, review.feedback)

    logger.info("Editor: final polish")
    article = editor.run(draft)

    return PipelineResult(
        article=article,
        research=research,
        revisions=revisions,
        reviews=reviews,
    )
