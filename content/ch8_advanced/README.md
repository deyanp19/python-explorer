# Chapter 08: Advanced Pythonic Features

Advanced features that make Python powerfull.

## Generators
Lazy evaluation using `yield`:
```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
```

## Decorators
Functions that modify other functions:
```python
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper
```

## Type Hinting
Add type annotations for better code clarity:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
