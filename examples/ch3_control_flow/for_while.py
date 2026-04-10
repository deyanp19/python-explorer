#!/usr/bin/env python3
"""Using for and while loops."""

# For loop with range
print("Counting with for loop:")
for i in range(5):
    print(f"  {i}")

# For loop with list
fruits = ["apple", "banana", "cherry"]
print(f"\nFruits:")
for i, fruit in enumerate(fruits, 1):
    print(f"  {i}. {fruit}")

# While loop
print(f"\nWhile loop counting down:")
countdown = 5
while countdown > 0:
    print(f"  {countdown}")
    countdown -= 1
print("Blast off!")

# Iterating over string
print(f"\nCharacters in 'Python':")
for char in "Python":
    print(f"  {char}")