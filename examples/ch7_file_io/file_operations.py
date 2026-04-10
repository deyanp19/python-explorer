#!/usr/bin/env python3
"""Basic file I/O operations."""
import os

filename = "example.txt"

# Writing to file
with open(filename, "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

print(f"File '{filename}' created and written.")

# Reading file
with open(filename, "r") as f:
    content = f.read()

print(f"\nFile content:\n{content}")

# Reading line by line
print("Reading line by line:")
with open(filename, "r") as f:
    for i, line in enumerate(f, 1):
        print(f"  Line {i}: {line.strip()}")

# Cleanup
os.remove(filename)
print(f"\nCleaned up {filename}")