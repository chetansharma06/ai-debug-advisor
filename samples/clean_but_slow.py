"""Example 3: clean but slow code.

This works correctly but is inefficient.
"""


def find_duplicates(items):
    """Find duplicate items (O(n²) approach)."""
    duplicates = []
    for item in items:
        count = 0
        for other in items:
            if item == other:
                count += 1
        if count > 1 and item not in duplicates:
            duplicates.append(item)
    return duplicates


if __name__ == "__main__":
    data = [1, 2, 3, 2, 4, 5, 1, 6, 7, 8, 9, 1]
    print(find_duplicates(data))  # Expected: [1, 2]