"""Deterministic fake LLM for tests and offline mode."""

from typing import Sequence

from debug_advisor.llm.base import LLMClient


class StubLLMClient(LLMClient):
    """Returns a deterministic, configurable response."""

    def __init__(self, response: str = "This is a deterministic test response.") -> None:
        self.response = response

    def generate(self, messages: Sequence[dict[str, str]]) -> str:
        return self.response