"""Tests for hint generation."""

from debug_advisor.agents.hints import HintGenerationAgent
from debug_advisor.llm.stub_client import StubLLMClient
from debug_advisor.models import Finding, Span


def test_hint_generation() -> None:
    agent = HintGenerationAgent(StubLLMClient())
    finding = Finding(
        finding_id="test",
        message="Test finding",
        span=Span(start_line=10),
    )
    hints = agent.generate("pass", [finding])
    assert len(hints) == 5
    assert [h.level for h in hints] == [1, 2, 3, 4, 5]
