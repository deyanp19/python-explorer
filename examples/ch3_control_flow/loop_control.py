#!/usr/bin/env python3
"""Using break, continue, and pass."""

print("Using break:")
for i in range(10):
    if i == 5:
        print("  Stopping at 5")
        break
    print(f"  {i}")

print("\nUsing continue:")
for i in range(5):
    if i == 2:
        print("  Skipping 2")
        continue
    print(f"  {i}")

print("\nUsing pass:")
class EmptyClass:
    pass  # Will add functionality later

def placeholder():
    pass  # Implement later

print("  Empty class and function created with pass")

# Else clause for loops
print(f"\nLoop with else:")
for i in range(3):
    print(f"  {i}")
else:
    print("  Looped through all items!")