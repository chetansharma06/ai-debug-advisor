"""Per-session hint-level tracking."""

from dataclasses import dataclass

from debug_advisor.models import Finding, Hint, HintLevel, SessionFinding


@dataclass(slots=True)
class SessionState:
    """Tracks the current hint level for each finding in the session"""

    findings: dict[str, SessionFinding]

    def __init__(self) -> None:
        self.findings = {}

    def register(self, finding: Finding) -> SessionFinding:
        existing = self.findings.get(finding.finding_id)
        if existing is not None:
            return existing
        session_finding = SessionFinding(finding=finding)
        self.findings[finding.finding_id] = session_finding
        return session_finding

    def advance(self, finding_id: str) -> Hint:
        """Advance one finding to the next hint level and return the new hint."""
        session_finding = self.findings[finding_id]
        next_level: HintLevel = min(session_finding.level + 1, 5)  # type: ignore[assignment]
        session_finding.level = next_level
        assert session_finding.hint is not None
        session_finding.hint.level = next_level
        return session_finding.hint

    def current_level(self, finding_id: str) -> HintLevel:
        return self.findings[finding_id].level