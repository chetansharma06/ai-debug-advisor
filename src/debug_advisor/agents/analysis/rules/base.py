"""Abstract base class for static-analysis rules."""

from abc import ABC, abstractmethod
from debug_advisor.models import Finding


class Rule(ABC):
    """A single static-analysis rule."""

    @property
    @abstractmethod
    def rule_id(self) -> str: ...

    @abstractmethod
    def check(self, code: str) -> list[Finding]: ...