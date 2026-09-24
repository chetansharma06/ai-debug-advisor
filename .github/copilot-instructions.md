# Copilot Instructions

## Python package: debug_advisor
- Python 3.11+, use type hints everywhere
- Use `dataclass(slots=True)` for models
- Use `Literal` for constrained string enums
- Ruff for linting/formatting (line length 88)
- pytest for testing
- All LLM interactions go through `LLMClient` protocol in `llm/base.py`
- Hint levels 1-4 must NOT leak the fix (use `LeakDetector`)