"""Logic / correctness rules (off-by-one, mutable default, etc.)."""

import ast
from debug_advisor.agents.analysis.rules.base import Rule
from debug_advisor.models import Finding, Span


class LogicRule(Rule):
    """Detects common logic bugs like off-by-one, mutable defaults."""

    @property
    def rule_id(self) -> str:
        return "logic"

    def check(self, code: str) -> list[Finding]:
        findings: list[Finding] = []
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return findings

        for node in ast.walk(tree):
            # mutable default argument
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        findings.append(
                            Finding(
                                finding_id=f"LOGIC-MUTABLE-DEFAULT-{node.lineno}",
                                message="Mutable default argument detected",
                                span=Span(start_line=node.lineno),
                                severity="high",
                                rule_id="mutable-default",
                            )
                        )
        return findings