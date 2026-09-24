"""Cyclomatic complexity and other metrics via radon."""

from debug_advisor.models import Finding, Span


class MetricsAgent:
    """Flags functions/classes exceeding complexity thresholds."""

    def find_issues(self, code: str) -> list[Finding]:
        # TODO: integrate with radon.complexity.cc_visit
        return []