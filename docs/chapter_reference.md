# Chapter Reference Guide

## Quick Navigation

| Chapter | Title | Key Topics | Example Count |
|---------|-------|-----------|---------------|
| 1 | Introduction | Syntax, Comments, Python Philosophy | 3 |
| 2 | Data Structures | Lists, Tuples, Sets, Dicts | 5 |
| 3 | Control Flow | If-else, Loops | 3 |
| 4 | Functions | Parameters, Scope, Lambdas | 3 |
| 5 | OOP | Classes, Inheritance, Dunder | 3 |
| 6 | Exception Handling | Try-except, Custom exceptions | 2 |
| 7 | File I/O | Context managers | 2 |
| 8 | Advanced Features | Generators, Decorators, Type hints | 3 |
| 9 | Concurrency | Threading, Async/Await | 3 |
| 10 | Standard Library | collections, itertools | 2 |

---

## Chapter-by-Chapter Breakdown

### Chapter 1: Introduction to Python

**File:** `content/ch1_intro/README.md`

**Topics:**
- What is Python?
- Basic syntax and structure
- Comments and documentation
- The Zen of Python

**Key Concepts:**
- Python is a high-level, interpreted language
- Indentation-based syntax
- Two types of comments: `#` and docstrings
- Python's philosophy (import this)

**Example Files:**
1. `hello_world.py` - Basic "Hello, World!" program
2. `zen_of_python.py` - Displays Python's design principles
3. `comments.py` - Shows various comment styles

**Learning Outcomes:**
- Write your first Python program
- Understand Python's readability-focused design
- Use comments effectively

**Sample Code:**
```python
# Print to console
print("Hello, World!")

# The Zen of Python
import this
```

---

### Chapter 2: Data Structures

**File:** `content/ch2_data_structures/README.md`

**Topics:**
- Primitive types
- Lists and their operations
- Tuples vs Lists
- Sets (unique, unordered)
- Dictionaries (key-value pairs)
- List comprehensions

**Key Concepts:**
- **Lists**: Ordered, mutable, can contain mixed types
- **Tuples**: Ordered, immutable
- **Sets**: Unordered, unique elements
- **Dictionaries**: Unordered key-value pairs (Python 3.7+ maintains insertion order)

**Example Files:**
1. `primitive_types.py` - Basic data types (int, float, str, bool)
2. `lists.py` - List creation and methods
3. `dictionaries.py` - Dict operations
4. `tuples_sets.py` - Tuples and sets usage

**Learning Outcomes:**
- Choose appropriate data structures for your use case
- Manipulate collections efficiently
- Use comprehensions for cleaner code

**Sample Code:**
```python
# Lists
my_list = [1, 2, 3, "four", 5.0]
my_list.append(6)  # Add item
my_list.pop()      # Remove last item

# Dictionaries
my_dict = {"name": "Alice", "age": 30}
my_dict["city"] = "New York"  # Add/modify

# List comprehension
squares = [x**2 for x in range(10)]
```

---

### Chapter 3: Control Flow

**File:** `content/ch3_control_flow/README.md`

**Topics:**
- Conditional statements (if, elif, else)
- For loops
- While loops
- Loop control statements (break, continue, pass)

**Key Concepts:**
- Boolean expressions evaluate to True/False
- Indentation defines code blocks
- Loop control for precise iteration behavior

**Example Files:**
1. `if_else.py` - Conditional logic
2. `for_while.py` - Loop structures
3. `loop_control.py` - Break, continue, pass

**Learning Outcomes:**
- Implement conditional logic
- Iterate over data structures
- Control program flow effectively

**Sample Code:**
```python
# Conditional
age = 20
if age < 18:
    print("Minor")
elif age == 18:
    print("You are 18")
else:
    print("Adult")

# For loop
for i in range(5):
    print(i)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
for i in range(10):
    if i == 5:
        break  # Exit loop
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
```

---

### Chapter 4: Functions & Functional Programming

**File:** `content/ch4_functions/README.md`

**Topics:**
- Function definition and calling
- Parameters and return values
- *args and **kwargs
- Variable scope (LEGB rule)
- Lambda functions
- Map, filter, and reduce

**Key Concepts:**
- Functions organize code into reusable blocks
- *args collects positional arguments into a tuple
- **kwargs collects keyword arguments into a dict
- LEGB: Local, Enclosing, Global, Built-in
- Lambdas are anonymous functions
- Functional programming applies functions to collections

**Example Files:**
1. `function_basics.py` - Basic function definition
2. `args_kwargs.py` - Variable arguments
3. `lambda_map_filter.py` - Functional programming

**Learning Outcomes:**
- Write reusable, modular code
- Understand variable scope
- Use functional programming patterns

**Sample Code:**
```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# *args and **kwargs
def print_args(*args, **kwargs):
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

# Variable scope
x = "global"
def inner():
    x = "local"
    print(x)  # Prints "local"

# Lambda
square = lambda x: x ** 2

# Map and filter
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

from functools import reduce
sum_all = reduce(lambda x, y: x + y, numbers)
```

---

### Chapter 5: Object-Oriented Programming

**File:** `content/ch5_oop/README.md`

**Topics:**
- Classes and objects
- Constructor (__init__)
- Instance methods and self
- Dunder methods (magic methods)
- Inheritance and polymorphism
- Encapsulation

**Key Concepts:**
- Classes define blueprints for objects
- __init__ initializes new instances
- Dunder methods customize object behavior
- Inheritance allows code reuse
- Polymorphism: different objects respond differently to the same method

**Dunder Methods Covered:**
- `__init__()`: Constructor
- `__str__()`: User-friendly string representation
- `__repr__()`: Official string representation
- `__len__()`: Length operation
- `__add__()`: Addition operator

**Example Files:**
1. `classes.py` - Basic class definition
2. `inheritance.py` - Class inheritance
3. `dunder_methods.py` - Magic methods

**Learning Outcomes:**
- Design classes and objects
- Implement inheritance hierarchies
- Use Python's magic methods effectively

**Sample Code:**
```python
# Basic class
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says woof!"

# Inheritance
class GoldenRetriever(Dog):
    def bark(self):
        return f"{self.name} says woof woof!"

# Dunder methods
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
    
    def __str__(self):
        return f"{self.title} ({self.pages} pages)"
    
    def __len__(self):
        return self.pages
    
    def __add__(self, other):
        return Book(f"{self.title} + {other.title}", 
                   self.pages + other.pages)
```

---

### Chapter 6: Error & Exception Handling

**File:** `content/ch6_exception_handling/README.md`

**Topics:**
- Try-except blocks
- Multiple exception handling
- Finally clause
- Custom exceptions

**Key Concepts:**
- Exceptions interrupt normal program flow
- Catch exceptions to handle errors gracefully
- Finally clause always executes
- Custom exceptions extend Exception class

**Example Files:**
1. `try_except.py` - Basic error handling
2. `custom_exceptions.py` - Define and raise custom exceptions

**Learning Outcomes:**
- Handle errors gracefully
- Create custom exception classes
- Write robust, error-resistant code

**Sample Code:**
```python
# Basic try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Multiple exceptions
try:
    value = int(input("Enter number: "))
except ValueError:
    print("Invalid number!")

# Finally always executes
try:
    file = open("data.txt", "r")
    data = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("Attempt completed")

# Custom exceptions
class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
```

---

### Chapter 7: File I/O & Context Managers

**File:** `content/ch7_file_io/README.md`

**Topics:**
- Reading files
- Writing files
- Context managers and `with` statement
- Custom context managers

**Key Concepts:**
- `with` ensures resources are properly cleaned up
- File modes: 'r' (read), 'w' (write), 'a' (append)
- Context managers can be created using classes or decorators

**Example Files:**
1. `file_operations.py` - Basic file reading and writing
2. `context_manager.py` - Custom context manager implementation

**Learning Outcomes:**
- Handle files safely and efficiently
- Create custom context managers
- Understand resource management

**Sample Code:**
```python
# Reading files
with open("file.txt", "r") as f:
    content = f.read()

# Writing files
with open("file.txt", "w") as f:
    f.write("Hello, World!")

# Custom context manager
from contextlib import contextmanager

@contextmanager
def file_manager(filename):
    f = open(filename, 'r')
    try:
        yield f
    finally:
        f.close()

# Usage
with file_manager("data.txt") as file:
    data = file.read()

# Context manager class
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        print(f"Elapsed: {self.end - self.start:.2f}s")

with Timer():
    # Code to time
    pass
```

---

### Chapter 8: Advanced Pythonic Features

**File:** `content/ch8_advanced/README.md`

**Topics:**
- Generators and `yield`
- Decorators
- Type hints

**Key Concepts:**
- Generators use lazy evaluation for memory efficiency
- Decorators modify function behavior
- Type hints improve code clarity and tool support

**Example Files:**
1. `generators.py` - Generator functions and expressions
2. `decorators.py` - Function decorators
3. `type_hints.py` - Type annotations

**Learning Outcomes:**
- Create memory-efficient generators
- Use decorators to enhance functions
- Add type annotations for better code clarity

**Sample Code:**
```python
# Generators
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

# Generator expression
squares = (x**2 for x in range(10))

# Decorators
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@my_decorator
def greet():
    print("Hello!")

# Type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

from typing import List, Dict

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

---

### Chapter 9: Concurrency & Async

**File:** `content/ch9_concurrency/README.md`

**Topics:**
- Threading for I/O-bound tasks
- Multiprocessing for CPU-bound tasks
- Async/await modern concurrency

**Key Concepts:**
- Threading shares memory, suitable for I/O
- Multiprocessing uses separate processes for CPU
- Async/await enables cooperative multitasking
- Events are asynchronous equivalents of threading Events

**Example Files:**
1. `threading.py` - Basic threading usage
2. `threading_example.py` - Thread synchronization
3. `asyncio_example.py` - Async programming

**Learning Outcomes:**
- Understand concurrent programming concepts
- Choose the right concurrency model
- Write asynchronous Python code

**Sample Code:**
```python
# Threading
import threading

def worker():
    print("Thread running")

thread = threading.Thread(target=worker)
thread.start()

# Multiprocessing
from multiprocessing import Process

def process_func():
    print("Processing")

process = Process(target=process_func)
process.start()

# Async/Await
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "Data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

---

### Chapter 10: Standard Library Highlights

**File:** `content/ch10_stdlib/README.md`

**Topics:**
- collections module
- itertools module
- datetime module
- os and sys modules

**Key Concepts:**
- `collections`: Enhanced data structures (Counter, defaultdict, etc.)
- `itertools`: Efficient iteration tools
- `datetime`: Date and time manipulation
- `os`: Operating system interfaces
- `sys`: System-specific parameters

**Example Files:**
1. `collections.py` - Counter, defaultdict, named tuple
2. `itertools.py` - Chain, accumulate, groupby

**Learning Outcomes:**
- Leverage built-in data structures
- Use itertools for efficient iteration
- Work with system and datetime operations

**Sample Code:**
```python
from collections import Counter, defaultdict, namedtuple
from itertools import chain, accumulate, groupby

# Counter
words = ['apple', 'banana', 'apple', 'cherry']
counter = Counter(words)
print(counter['apple'])  # 2

# Default dict
dd = defaultdict(int)
dd['key'] += 1  # No KeyError

# Named tuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# Chain
combined = chain([1, 2], [3, 4])
print(list(combined))  # [1, 2, 3, 4]

# Accumulate
squares = accumulate([1, 2, 3, 4])
print(list(squares))  # [1, 3, 6, 10]

# Group by
data = [('a', 1), ('a', 2), ('b', 3)]
grouped = {k: list(v) for k, v in groupby(data, key=lambda x: x[0])}
```

**datetime Module:**
```python
from datetime import datetime, timedelta

now = datetime.now()
tomorrow = now + timedelta(days=1)
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
parsed = datetime.strptime("2024-01-01", "%Y-%m-%d")
```

**OS and System:**
```python
import os, sys

# OS operations
files = os.listdir('.')
os.mkdir('new_directory')
os.remove('file.txt')

# System info
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"Command-line args: {sys.argv}")
```

---

## Quick Reference: Module Index

### `math` Module
- Constants: `e`, `pi`, `inf`, `nan`
- Rounding: `ceil`, `floor`, `trunc`, `fabs`
- Trigonometry: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Conversions: `degrees`, `radians`
- Exponential: `pow`, `sqrt`, `exp`, `log`, `log10`, `log2`
- Special: `hypot`, `isinf`, `isnan`, `isfinite`

### Built-in Functions
- `len()`: Length of container
- `sum()`: Sum of elements
- `min()`, `max()`: Minimum and maximum
- `sorted()`: Return sorted list
- `enumerate()`: Iterate with index
- `zip()`: Combine iterables
- `range()`: Sequence generator

### collections Module
- `Counter`: Count elements
- `defaultdict`: Dict with default value
- `namedtuple`: Tuple subclass with named fields
- `OrderedDict`: OrderedDict maintains insertion order (Python 3.7+)
- `deque`: Doubly-ended queue
- `ChainMap`: Combine dictionaries

### itertools Module
- `chain()`: Chain iterables
- `accumulate()`: Cumulative results
- `groupby()`: Group consecutive elements
- `product()`, `permutations()`, `combinations()`: Combinatorial functions
- `islice()`: Slice iterators
- `cycle()`, `repeat()`, `chain.from_iterable()`: Infinite iterators

---

## Learning Path Recommendations

### Beginner Path (Chapters 1-5)
1. Start with Chapter 1: Understand Python basics
2. Chapter 2: Master data structures early
3. Chapter 3: Learn control flow patterns
4. Chapter 4: Functions are the building blocks
5. Chapter 5: OOP for structured programs

### Intermediate Path (Chapters 6-8)
1. Chapter 6: Error handling makes code robust
2. Chapter 7: File I/O is practical and common
3. Chapter 8: Advanced features elevate your code

### Advanced Path (Chapters 9-10)
1. Chapter 9: Concurrency for performance
2. Chapter 10: Standard library expertise

### By Use Case

**Web Development:** Chapters 4, 5, 7, 8  
**Data Science:** Chapters 2, 4, 10  
**System Tools:** Chapters 7, 8, 10  
**High Performance:** Chapters 8, 9, 10  

---

## Example Code Summary

| Chapter | Examples | Key Learnings |
|---------|----------|---------------|
| 1 | hello_world, zen_of_python, comments | Python basics and philosophy |
| 2 | primitive_types, lists, dictionaries, tuples_sets | Data organization |
| 3 | if_else, for_while, loop_control | Program flow |
| 4 | function_basics, args_kwargs, lambda_map_filter | Code reuse |
| 5 | classes, inheritance, dunder_methods | Object design |
| 6 | try_except, custom_exceptions | Error management |
| 7 | file_operations, context_manager | Resource handling |
| 8 | decorators, generators, type_hints | Advanced patterns |
| 9 | threading, threading_example, asyncio_example | Concurrency |
| 10 | collections, itertools | Standard library |

---

## Additional Resources

- **Official Python Docs**: https://docs.python.org/3/
- **Python Software Foundation**: https://www.python.org/psf/
- **Real Python Tutorials**: https://realpython.com/
- **Python Challenge**: https://www.pythonchallenge.com/

---

*This chapter reference provides quick access to all 10 chapters covered in the Python Features Explorer.*
