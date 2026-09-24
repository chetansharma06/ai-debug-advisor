"""CodeOptimizationAgent: produces optimized versions of buggy code."""

from debug_advisor.llm.base import LLMClient


class CodeOptimizationAgent:
    """Generates an optimized/fixed version of the user's code."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def optimize(self, code: str) -> str:
        # TODO: integrate with LLM to generate optimized code
        return "# Optimized version of your code\n" + code