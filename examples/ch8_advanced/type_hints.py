#!/usr/bin/env python3
"""Type hints in Python."""

from typing import List, Dict, Optional

def greet(name: str) -> str:
    """Greet someone with type hints."""
    return f"Hello, {name}!"

def process_numbers(numbers: List[float]) -> Dict[str, float]:
    """Process numbers with type hints."""
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers) if numbers else 0,
        "count": len(numbers)
    }

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    """Return None if user not found."""
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

# Usage
print(greet("World"))

result = process_numbers([10.5, 20.3, 30.7])
print(f"Results: {result}")

user = get_user(1)
print(f"User: {user}")
print(f"User type: {type(user)}")