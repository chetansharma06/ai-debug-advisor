"""Loading versioned Jinja2 prompt templates."""

from pathlib import Path

from jinja2 import Environment


class PromptLoader:
    """Loads prompts from the prompts/ directory."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[2]
        self.env = Environment()

    def render(self, name: str, **context: object) -> str:
        template = self.env.from_string(
            (self.root / "prompts" / name).read_text(encoding="utf-8")
        )
        return template.render(**context)