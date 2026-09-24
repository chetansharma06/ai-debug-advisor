"""LLMClient protocol shared by all backends."""

from typing import Protocol, Sequence


class LLMClient(Protocol):
    """Minimal interface for an LLM backend."""

    def generate(self, messages: Sequence[dict[str, str]]) -> str:
        """Generate a response from the model."""
        ...