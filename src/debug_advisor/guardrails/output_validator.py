"""Validates LLM JSON output against expected schemas."""

import json


class OutputValidator:
    """Ensures LLM responses are valid JSON matching the expected schema."""

    def validate(self, text: str, schema: type) -> object:
        """Parse and validate JSON against a TypedDict / dataclass."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("LLM output is not valid JSON")
        # TODO: add jsonschema validation
        return data