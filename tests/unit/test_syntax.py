"""Tests for syntax analyzer."""

from debug_advisor.agents.analysis.syntax import SyntaxAnalyzer


def test_syntax_error_detected() -> None:
    code = "def foo(:"  # invalid syntax
    findings = SyntaxAnalyzer().find_issues(code)
    assert len(findings) == 1
    assert "Syntax error" in findings[0].message