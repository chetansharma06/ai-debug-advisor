"""Core data models shared across the debugging pipeline."""

from dataclasses import dataclass, field
from typing import Literal


HintLevel = Literal[1, 2, 3, 4, 5]


@dataclass(slots=True)
class Span:
    """A source-code span (inclusive line numbers, 1-based)."""

    start_line: int
    end_line: int | None = None

    def contains(self, line: int) -> bool:
        end = self.end_line if self.end_line is not None else self.start_line
        return self.start_line <= line <= end


@dataclass(slots=True)
class Finding:
    """A single issue detected in the user's code."""

    finding_id: str
    message: str
    span: Span
    severity: str = "medium"
    rule_id: str | None = None


@dataclass(slots=True)
class Explanation:
    """A human-readable explanation of one finding."""

    finding_id: str
    title: str
    body: str
    example: str | None = None


@dataclass(slots=True)
class Hint:
    """One step in the graded hint ladder."""

    finding_id: str
    level: HintLevel
    text: str


@dataclass(slots=True)
class SessionFinding:
    """Finding plus its current hint level for a session."""

    finding: Finding
    level: HintLevel = 1
    hint: Hint | None = None


@dataclass(slots=True)
class PipelineResult:
    """Full output of one advisor run."""

    findings: list[Finding] = field(default_factory=list)
    explanation: Explanation | None = None
    hints: list[Hint] = field(default_factory=list)
    optimized_code: str | None = None