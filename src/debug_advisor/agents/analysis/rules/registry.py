"""Registry that collects all Rule subclasses and runs them."""

from debug_advisor.agents.analysis.rules.base import Rule
from debug_advisor.agents.analysis.rules.logic import LogicRule
from debug_advisor.agents.analysis.rules.structural import StructuralRule
from debug_advisor.agents.analysis.rules.style import StyleRule
from debug_advisor.models import Finding


class RulesRegistry:
    """Holds instantiated rules and runs them on code."""

    def __init__(self) -> None:
        self._rules: list[Rule] = [
            LogicRule(),
            StructuralRule(),
            StyleRule(),
        ]

    def find_issues(self, code: str) -> list[Finding]:
        findings: list[Finding] = []
        for rule in self._rules:
            findings.extend(rule.check(code))
        return findings


RULES_REGISTRY = RulesRegistry()