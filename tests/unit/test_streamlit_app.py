"""Tests for the Streamlit-based analysis wrapper."""

from streamlit_app import analyze_code


def test_analyze_code_returns_findings() -> None:
    code = "def foo(items=[]):\n    return items\n"
    result = analyze_code(code)
    assert len(result.findings) > 0
