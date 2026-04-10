# Chapter 06: Error & Exception Handling

Exception handling allows graceful error management.

## Try-Except Blocks
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

## Multiple Exceptions
```python
try:
    # risky code
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
```

## Finally
Always executes:
```python
try:
    # risky code
finally:
    print("This always runs")
```

## Custom Exceptions
```python
class CustomError(Exception):
    pass
```
