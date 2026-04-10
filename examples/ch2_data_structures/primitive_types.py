#!/usr/bin/env python3
"""Demonstrating Python primitive types."""

# Integer
number = 42
print(f"Integer: {number} (type: {type(number).__name__})")

# Float
price = 19.99
print(f"Float: {price} (type: {type(price).__name__})")

# String
name = "Python"
print(f"String: {name} (type: {type(name).__name__})")

# Boolean
is_python_cool = True
print(f"Boolean: {is_python_cool} (type: {type(is_python_cool).__name__})")

# Mixed list
mixed = [1, 2.5, "hello", True]
print(f"\nMixed list: {mixed}")
print(f"Length: {len(mixed)}")