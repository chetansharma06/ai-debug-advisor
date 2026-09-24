"""Example 2: off-by-one error.

This loop misses the last element.
"""

def find_max(values):
    """Find the maximum value."""
    if not values:
        return None
    max_val = values[0]
    for i in range(len(values) - 1):  # BUG: skips last element
        if values[i] > max_val:
            max_val = values[i]
    return max_val


if __name__ == "__main__":
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(find_max(nums))  # Expected: 9, but returns 5 (missing the 9!)