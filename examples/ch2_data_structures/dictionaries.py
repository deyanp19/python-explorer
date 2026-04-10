#!/usr/bin/env python3
"""Working with dictionaries and dict comprehensions."""

# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
print(f"Person: {person}")

# Accessing values
print(f"\nName: {person.get('name')}")
print(f"Age: {person['age']}")

# Updating
person["age"] = 31
person["email"] = "alice@example.com"
print(f"\nUpdated: {person}")

# Iterating
print(f"\nKey-Value pairs:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Dict comprehension
squares = {x: x**2 for x in range(5)}
print(f"\nDict comprehension: {squares}")