"""Per-session hint-level tracking and code-hash result caching."""

import hashlib
from dataclasses import dataclass

from debug_advisor.models import Finding, Hint, HintLevel, SessionFinding


def code_hash(code: str) -> str:
    """Return a stable SHA-256 hash for a code snippet (used for caching)."""
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class SessionState:
    """Tracks the current hint level for each finding in the session."""

    findings: dict[str, SessionFinding]

    def __init__(self) -> None:
        self.findings = {}
        # Cache of full PipelineResult keyed by code hash so unchanged code
        # does not re-trigger the analysis pipeline.
        self._result_cache: dict[str, object] = {}

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

    # ------------------------------------------------------------------
    # Code-hash result cache
    # ------------------------------------------------------------------

    def cache_result(self, code: str, result: object) -> None:
        """Store a PipelineResult keyed by the code snippet's hash."""
        self._result_cache[code_hash(code)] = result

    def get_cached_result(self, code: str) -> object | None:
        """Return a cached PipelineResult for this code, or None if absent."""
        return self._result_cache.get(code_hash(code))

    def invalidate(self, code: str | None = None) -> None:
        """Drop cached results. If ``code`` is None, drop everything."""
        if code is None:
            self._result_cache.clear()
        else:
            self._result_cache.pop(code_hash(code), None)