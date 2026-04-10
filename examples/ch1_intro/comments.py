#!/usr/bin/env python3
"""Demonstrating Python comments and docstrings."""

# This is a single-line comment
# Comments help explain what code does

print("This will be printed")

# Another comment before the next line
print("This will also be printed")

"""
This is a module-level docstring.
It documents the entire module.
"""

def example_function():
    """
    This is a function docstring.
    
    Docstrings are triple-quoted strings that document code.
    They can span multiple lines.
    """
    pass  # This function does nothing intentionally

if __name__ == "__main__":
    print("\nDocstring of example_function:")
    print(example_function.__doc__)
