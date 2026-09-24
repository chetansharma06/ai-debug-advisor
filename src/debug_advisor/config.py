"""Settings loaded from environment / .env files."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    """Runtime configuration."""

    llm_api_key: str | None
    llm_base_url: str
    llm_model: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            llm_api_key=os.getenv("LLM_API_KEY"),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://api.example.com/v1"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o"),
        )


def project_root() -> Path:
    """Return the repository root, independent of the current directory."""
    return Path(__file__).resolve().parents[2]