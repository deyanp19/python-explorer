# Chapter 07: File I/O & Context Managers

Safe file handling with context managers.

## Reading Files
```python
with open("file.txt", "r") as f:
    content = f.read()
```

## Writing Files
```python
with open("file.txt", "w") as f:
    f.write("Hello, World!")
```

## Context Managers
The `with` statement ensures resources are properly cleaned up.

## Custom Context Managers
```python
from contextlib import contextmanager

@contextmanager
def file_handler(filename):
    f = open(filename, 'r')
    try:
        yield f
    finally:
        f.close()
