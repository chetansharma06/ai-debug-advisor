"""GitHub Copilot API implementation."""

import os
from typing import Sequence

from debug_advisor.llm.base import LLMClient


class CopilotClient(LLMClient):
    """Client for the GitHub Copilot API."""

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def generate(self, messages: Sequence[dict[str, str]]) -> str:
        # TODO: integrate with Copilot API
        return "Copilot response"