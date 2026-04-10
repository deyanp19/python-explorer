#!/usr/bin/env python3
"""Demonstrating tuples and sets."""

# Tuple - immutable
coordinates = (10.5, 20.3)
print(f"Tuple: {coordinates}")
print(f"Type: {type(coordinates).__name__}")

try:
    coordinates[0] = 5
except TypeError as e:
    print(f"\nCannot modify: {e}")

# Set - unordered, unique elements
fruits = {"apple", "banana", "apple", "cherry"}
print(f"\nSet (removes duplicates): {fruits}")

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(f"\nset1: {set1}")
print(f"set2: {set2}")
print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")