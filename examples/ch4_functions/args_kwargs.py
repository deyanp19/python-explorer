#!/usr/bin/env python3
"""Using *args and **kwargs."""

def print_all(*args):
    """Accept variable positional arguments."""
    print("Positional args:", args)
    for i, arg in enumerate(args):
        print(f"  {i}: {arg}")

print_all(1, 2, 3, 4, 5)

def describe_person(**kwargs):
    """Accept variable keyword arguments."""
    print("Keyword args:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

describe_person(name="Alice", age=30, city="NYC", job="Engineer")

def combine_args_kwargs(*args, **kwargs):
    """Mix both types."""
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

combine_args_kwargs(1, 2, name="Test", value=100)