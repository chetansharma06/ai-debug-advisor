"""ErrorExplanationAgent: generates human-readable explanations of findings."""

from debug_advisor.models import Explanation
from debug_advisor.llm.base import LLMClient


class ErrorExplanationAgent:
    """Creates user-friendly explanations for each finding."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def explain(self, code: str, findings: list[Explanation]) -> Explanation:
        # TODO: integrate with LLM to generate explanation
        if not findings:
            return Explanation(
                finding_id="none",
                title="No issues found",
                body="Your code appears to be correct.",
            )
        finding = findings[0]
        return Explanation(
            finding_id=finding.finding_id,
            title=finding.message,
            body=f"There is an issue at line {finding.span.start_line}: {finding.message}",
        )