"""Pipeline tests using a scripted fake LLM — no network, no API key."""

from multi_agent_writer.agents.critic import Critic
from multi_agent_writer.pipeline import run_pipeline


class FakeLLM:
    """Returns canned responses keyed by the agent's system prompt."""

    def __init__(self, critic_verdicts: list[str]):
        self._critic_verdicts = critic_verdicts
        self._critic_calls = 0
        self.calls: list[str] = []

    def complete(self, system: str, user: str) -> str:
        if "research assistant" in system:
            self.calls.append("researcher")
            return "Outline: intro, body, conclusion"
        if "revising" in system:
            self.calls.append("writer-revise")
            return "Revised draft"
        if "strict but constructive" in system:
            self.calls.append("critic")
            verdict = self._critic_verdicts[min(self._critic_calls, len(self._critic_verdicts) - 1)]
            self._critic_calls += 1
            return verdict
        if "copy editor" in system:
            self.calls.append("editor")
            return "# Polished\n\n" + user
        self.calls.append("writer-draft")
        return "First draft"


APPROVE = '{"approved": true, "feedback": "great"}'
REJECT = '{"approved": false, "feedback": "fix the intro"}'


def test_approved_first_try_runs_each_agent_once():
    llm = FakeLLM([APPROVE])
    result = run_pipeline("test topic", llm.complete, max_revisions=2)

    assert llm.calls == ["researcher", "writer-draft", "critic", "editor"]
    assert result.revisions == 0
    assert result.article.startswith("# Polished")


def test_rejected_then_approved_triggers_one_revision():
    llm = FakeLLM([REJECT, APPROVE])
    result = run_pipeline("test topic", llm.complete, max_revisions=2)

    assert result.revisions == 1
    assert "writer-revise" in llm.calls
    assert llm.calls.count("critic") == 2


def test_revision_limit_is_respected():
    llm = FakeLLM([REJECT])  # critic always rejects
    result = run_pipeline("test topic", llm.complete, max_revisions=2)

    assert result.revisions == 2
    assert llm.calls.count("writer-revise") == 2
    # Editor still runs: best effort beats no article.
    assert result.article.startswith("# Polished")


def test_critic_parses_json_wrapped_in_fences():
    review = Critic._parse('```json\n{"approved": false, "feedback": "too short"}\n```')
    assert review.approved is False
    assert review.feedback == "too short"


def test_critic_treats_garbage_as_approval():
    review = Critic._parse("I really liked it!")
    assert review.approved is True
