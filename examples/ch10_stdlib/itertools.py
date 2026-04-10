#!/usr/bin/env python3
"""itertools module examples."""

from itertools import chain, accumulate, groupby

# Chain - combine iterables
lists = [[1, 2, 3], [4, 5], [6]]
combined = list(chain.from_iterable(lists))
print("Chain example:")
print(f"  {combined}")

# Accumulate - cumulative operations
numbers = [1, 2, 3, 4, 5]
cumulative = list(accumulate(numbers))
print(f"\nAccumulate (sum):   {cumulative}")
cumulative_mult = list(accumulate(numbers, lambda x, y: x*y))
print(f"Accumulate (multiply): {cumulative_mult}")

# GroupBy - group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
groups = {k: list(g) for k, g in groupby(data, key=lambda x: x[0])}
print(f"\nGroupBy example:")
for key, group in groups.items():
    print(f"  {key}: {group}")