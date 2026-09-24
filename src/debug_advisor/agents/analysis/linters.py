"""Adapter for Ruff and Pyflakes linters."""

from debug_advisor.models import Finding, Span


class LinterAdapter:
    """Runs Ruff and Pyflakes on source code, returning unified Findings."""

    def find_issues(self, code: str) -> list[Finding]:
        # TODO: integrate with ruff.api and pyflakes.checker
        return []