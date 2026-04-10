# Chapter 02: Data Structures

Python provides several built-in data structures for organizing and storing data.

## Primitive Types
- **int**: Integer numbers
- **float**: Floating-point numbers
- **str**: Strings (immutable sequences of characters)
- **bool**: Boolean values (True/False)

## Collections

### Lists
Lists are ordered, mutable collections that can contain mixed types.
```python
my_list = [1, 2, 3, "four", 5.0]
```

### Tuples
Tuples are ordered, immutable collections.
```python
my_tuple = (1, 2, 3)
```

### Sets
Sets are unordered collections of unique elements.
```python
my_set = {1, 2, 3, 1, 2}  # Result: {1, 2, 3}
```

### Dictionaries
Dictionaries are unordered collections of key-value pairs.
```python
my_dict = {"name": "Alice", "age": 30}
```

### List Comprehensions
A compact way to create lists.
```python
squares = [x**2 for x in range(10)]
```
