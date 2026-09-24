"""Detects fix leakage in hints (levels 1-4)."""

import re


class LeakDetector:
    """Flags hints that reveal the actual fix code."""

    FIX_PATTERNS = [
        r"change .* to .*",
        r"replace .* with .*",
        r"add .*",
        r"remove .*",
        r"fix:?\s",
        r"solution:?\s",
        r"answer:?\s",
    ]

    def check(self, hint: str) -> bool:
        """Return True if the hint appears to leak the fix."""
        lowered = hint.lower()
        return any(re.search(p, lowered) for p in self.FIX_PATTERNS)