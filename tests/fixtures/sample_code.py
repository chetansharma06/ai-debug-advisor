"""Test fixtures for sample code."""


def add(a, b):
    return a + b


def buggy_add(a, b=None):
    if b is None:
        b = 0
    return a + b