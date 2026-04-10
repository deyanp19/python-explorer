#!/usr/bin/env python3
"""Generators using yield."""

def count_up_to(n):
    """Generate numbers up to n."""
    i = 1
    while i <= n:
        yield i
        i += 1

print("Numbers 1 to 5:")
for num in count_up_to(5):
    print(f"  {num}")

# Memory efficient generation
print("\nLarge range (only first 5):")
large_range = count_up_to(1000000)
for i, num in enumerate(large_range):
    print(f"  {num}")
    if i == 4:
        break

# Generator expression
squares = (x**2 for x in range(10))
print(f"\nGenerator expression: {type(squares)}")
print(f"First 5 squares: {[next(squares) for _ in range(5)]}")