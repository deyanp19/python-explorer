# Chapter 04: Functions & Functional Programming

Functions organize code into reusable blocks.

## Function Basics
```python
def greet(name):
    return f"Hello, {name}!"
```

## *args and **kwargs
- `*args`: Variable positional arguments (tuple)
- `**kwargs`: Variable keyword arguments (dict)

## Scope (LEGB)
Variables follow the LEGB rule:
- **L**ocal
- **E**nclosing
- **G**lobal
- **B**uilt-in

## Lambda Functions
Anonymous functions for quick operations.
```python
square = lambda x: x ** 2
```

## Functional Programming
- `map()`: Apply function to all items
- `filter()`: Filter items based on condition
- `reduce()`: Cumulative operations
