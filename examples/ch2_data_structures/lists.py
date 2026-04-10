#!/usr/bin/env python3
"""Working with Python lists."""

# Creating a list
numbers = [1, 2, 3, 4, 5]
print(f"Original: {numbers}")

# Accessing elements
print(f"First element: {numbers[0]}")
print(f"Last element: {numbers[-1]}")

# List operations
numbers.append(6)
print(f"\nAfter append(6): {numbers}")

numbers.insert(0, 0)
print(f"After insert(0, 0): {numbers}")

# Slicing
print(f"\nFirst 3: {numbers[:3]}")
print(f"Last 3: {numbers[-3:]}")

# List comprehension
squares = [x**2 for x in range(5)]
print(f"\nSquares (0-4): {squares}")

# Mutable - can change
numbers[0] = 100
print(f"\nAfter numbers[0] = 100: {numbers}")