#!/usr/bin/env python3
"""Understanding if-elif-else statements."""

age = 25

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 65:
    print("Adult")
else:
    print("Senior")

print(f"\nAge: {age}")

# Nested conditionals
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    if score >= 95:
        grade = "A+"
    else:
        grade = "A-"
else:
    grade = "B or lower"

print(f"Score: {score} -> Grade: {grade}")