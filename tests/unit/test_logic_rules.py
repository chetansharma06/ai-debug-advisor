"""Tests for logic rules (mutable default, off-by-one)."""

import pytest
from debug_advisor.agents.analysis.rules.logic import LogicRule


def test_mutable_default_detected() -> None:
    code = "def foo(items=[]): pass"
    findings = LogicRule().check(code)
    assert len(findings) > 0
    assert findings[0].message == "Mutable default argument detected"