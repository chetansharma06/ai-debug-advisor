"""Style / convention rules (naming, formatting, etc.)."""

from debug_advisor.agents.analysis.rules.base import Rule
from debug_advisor.models import Finding


class StyleRule(Rule):
    """Detects style violations (naming, formatting, etc.)."""

    @property
    def rule_id(self) -> str:
        return "style"

    def check(self, code: str) -> list[Finding]:
        # TODO: integrate with Ruff style checks
        return []