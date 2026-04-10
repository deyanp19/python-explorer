#!/usr/bin/env python3
"""collections module examples."""

from collections import Counter, defaultdict, namedtuple, OrderedDict

# Counter
fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(fruits)
print("Counter example:")
print(f"  Fruits: {dict(counts)}")
print(f"  Most common: {counts.most_common(2)}")

# defaultdict
words = ["apple", "banana", "apple", "cherry"]
letter_counts = defaultdict(int)
for word in words:
    letter_counts[len(word)] += 1

print("\ndefaultdict example:")
print(f"  Word lengths: {dict(letter_counts)}")

# NamedTuple
Person = namedtuple("Person", ["name", "age"])
alice = Person("Alice", 30)
print(f"\nNamedTuple: {alice}")
print(f"  Name: {alice.name}, Age: {alice.age}")

# OrderedDict
od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3
print(f"\nOrderedDict (remembers insertion order):")
print(f"  {dict(od)}")