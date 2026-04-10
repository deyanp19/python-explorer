#!/usr/bin/env python3
"""Custom context manager using contextlib."""
from contextlib import contextmanager
import os

class FileManager:
    """Manual context manager."""
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# Manual context manager
print("Manual context manager:")
with FileManager("test.txt", "w") as f:
    f.write("Test content")
print("File automatically closed")

# Using contextmanager decorator
@contextmanager
def managed_file(filename):
    f = open(filename, "w")
    try:
        yield f
    finally:
        f.close()

print("\nUsing contextmanager decorator:")
with managed_file("test.txt") as f:
    f.write("Managed content")
print("File automatically closed")

# Cleanup
os.remove("test.txt")