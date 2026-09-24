"""Example 1: mutable default argument.

This function has a bug: the list default is shared across calls.
"""

def process_items(items=[]):
    """Process items, accumulating across calls."""
    processed = items.copy()
    processed.append("processed")
    return processed


if __name__ == "__main__":
    print(process_items(["a", "b"]))  # Expected: ['a', 'b', 'processed']
    print(process_items(["c"]))       # Expected: ['c', 'processed']
    print(process_items())            # Expected: ['processed']
    # The bug: each call shares the same default list!