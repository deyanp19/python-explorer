#!/usr/bin/env python3
"""Custom exceptions."""

class InvalidAgeError(Exception):
    """Raised when age is invalid."""
    pass

class NegativeValueError(Exception):
    """Raised for negative values."""
    pass

def set_age(age):
    if age < 0:
        raise NegativeValueError("Age cannot be negative")
    elif age > 150:
        raise InvalidAgeError("Age seems unrealistic")
    else:
        print(f"Age set to: {age}")

try:
    set_age(-5)
except NegativeValueError as e:
    print(f"Caught: {e}")

try:
    set_age(200)
except InvalidAgeError as e:
    print(f"Caught: {e}")

set_age(25)