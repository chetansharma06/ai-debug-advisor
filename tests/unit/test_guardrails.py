"""Tests for guardrails."""

import pytest
from debug_advisor.guardrails.leak_detector import LeakDetector
from debug_advisor.guardrails.output_validator import OutputValidator


@pytest.mark.parametrize("hint", [
    "change x to y",
    "replace foo with bar",
    "the fix is: x = 1",
])
def test_leak_detection(hint: str) -> None:
    detector = LeakDetector()
    assert detector.check(hint) is True


def test_no_leak() -> None:
    detector = LeakDetector()
    assert detector.check("consider checking if something is None") is False