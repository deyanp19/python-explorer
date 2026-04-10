#!/usr/bin/env python3
"""Lambda functions and functional programming."""

# Lambda - anonymous function
square = lambda x: x**2
print(f"Lambda square of 5: {square(5)}")

sort_key = lambda person: person["age"]

# Map - apply function to all items
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print(f"\nSquares using map: {squares}")

# Filter - keep items matching condition
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")

# Practical example
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30}
]

adults = filter(lambda p: p["age"] >= 18, people)
print(f"\nAdults: {[p['name'] for p in adults]}")