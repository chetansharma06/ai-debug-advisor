"""Syntax error detection using the standard library AST."""

import ast
from debug_advisor.models import Finding, Span


class SyntaxAnalyzer:
    """Detects Python syntax errors and reports precise spans."""

    def find_issues(self, code: str) -> list[Finding]:
        findings: list[Finding] = []
        try:
            ast.parse(code)
        except SyntaxError as exc:
            start = max(exc.lineno or 1, 1)
            findings.append(
                Finding(
                    finding_id=f"SYNTAX-{start}",
                    message=f"Syntax error: {exc.msg}",
                    span=Span(start_line=start),
                    severity="high",
                    rule_id="syntax-error",
                )
            )
        return findings