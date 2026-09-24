"""Integration test: full pipeline with StubLLMClient."""

from debug_advisor.llm.stub_client import StubLLMClient
from debug_advisor.orchestrator import DebugAdvisor


def test_full_pipeline() -> None:
    code = "def foo(items=[]): pass"
    advisor = DebugAdvisor(StubLLMClient())
    result = advisor.run(code)
    assert len(result.findings) > 0