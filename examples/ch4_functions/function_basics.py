#!/usr/bin/env python3
"""Function basics and scope."""

def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet("World"))

# Default parameters
def introduce(name, age=25):
    return f"{name} is {age} years old"

print(f"\nWith default age: {introduce('Bob')}")
print(f"With specified age: {introduce('Bob', 30)}")

# Return multiple values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

stats = get_stats([10, 20, 30, 40, 50])
print(f"\nMin: {stats[0]}, Max: {stats[1]}, Sum: {stats[2]}")

# Scope demonstration
x = "global"

def scope_test():
    x = "local"
    print(f"Inside function: {x}")

scope_test()
print(f"Outside: {x}")