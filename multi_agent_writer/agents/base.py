"""Shared typing for agents.

Every agent receives a ``complete(system, user) -> str`` callable instead of
a concrete client, so the pipeline can be tested without network access.
"""

from typing import Callable

CompleteFn = Callable[[str, str], str]
