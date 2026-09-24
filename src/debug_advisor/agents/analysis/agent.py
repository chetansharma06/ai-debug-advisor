"""CodeAnalysisAgent: runs syntax, lint, and rule-based analysis."""

from debug_advisor.agents.analysis.linters import LinterAdapter
from debug_advisor.agents.analysis.metrics import MetricsAgent
from debug_advisor.agents.analysis.rules.registry import RULES_REGISTRY
from debug_advisor.agents.analysis.syntax import SyntaxAnalyzer
from debug_advisor.models import Finding


class CodeAnalysisAgent:
    """Coordinates all static analysis backends."""

    def __init__(self) -> None:
        self.syntax = SyntaxAnalyzer()
        self.linters = LinterAdapter()
        self.metrics = MetricsAgent()
        self.rules = RULES_REGISTRY

    def analyze(self, code: str) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self.syntax.find_issues(code))
        findings.extend(self.linters.find_issues(code))
        findings.extend(self.rules.find_issues(code))
        findings.extend(self.metrics.find_issues(code))
        return findings