#!/usr/bin/env python3
"""Basic exception handling."""

# Try-except
print("Try-except example:")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  Cannot divide by zero!")

# Specific exceptions
print("\nSpecific exceptions:")
try:
    age = int("not_a_number")
except ValueError as e:
    print(f"  ValueError: {e}")

# Multiple exceptions
print("\nMultiple exceptions:")
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"  Caught: {e}")

# Finally
print("\nWith finally:")
try:
    print("  Attempting operation...")
    result = 5 / 0
except ZeroDivisionError:
    print("  Error caught!")
finally:
    print("  This always runs")