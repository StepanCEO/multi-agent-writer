"""Agent roles: researcher, writer, critic, editor."""

from .base import CompleteFn
from .critic import Critic, Review
from .editor import Editor
from .researcher import Researcher
from .writer import Writer

__all__ = ["CompleteFn", "Researcher", "Writer", "Critic", "Review", "Editor"]
