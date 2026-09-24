"""Structural rules (unused imports, dead code, etc.)."""

import ast
from debug_advisor.agents.analysis.rules.base import Rule
from debug_advisor.models import Finding, Span


class StructuralRule(Rule):
    """Detects structural issues like dead code or unreachable statements."""

    @property
    def rule_id(self) -> str:
        return "structural"

    def check(self, code: str) -> list[Finding]:
        findings: list[Finding] = []
        # TODO: implement unused import detection, dead code, etc.
        return findings