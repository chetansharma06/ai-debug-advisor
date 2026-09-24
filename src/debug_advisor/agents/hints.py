"""HintGenerationAgent: produces graded hints for findings."""

from debug_advisor.models import Finding, Hint, HintLevel
from debug_advisor.llm.base import LLMClient


class HintGenerationAgent:
    """Generates graded hints (1-5) for each finding."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def generate(self, code: str, findings: list[Finding]) -> list[Hint]:
        # TODO: integrate with LLM to generate hints
        if not findings:
            return []
        # Generate 5-level hint ladder
        hints = []
        for level in range(1, 6):
            hints.append(
                Hint(
                    finding_id=findings[0].finding_id,
                    level=level,
                    text=f"Hint level {level}: Something about line {findings[0].span.start_line}",
                )
            )
        return hints
