#!/usr/bin/env python3
"""Script to generate all chapter content and examples."""

import os

# Chapter definitions: (chapter_name, readme_content, examples)
CHAPTERS = {
    "ch2_data_structures": {
        "readme": """# Chapter 02: Data Structures

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
"""
    },
    "ch3_control_flow": {
        "readme": """# Chapter 03: Control Flow

Control flow allows you to make decisions and repeat code blocks.

## Conditional Statements
- `if`: Execute code if condition is true
- `elif`: Execute if previous conditions were false
- `else`: Execute if no conditions were true

## Loops
- `for`: Iterate over sequences
- `while`: Repeat while condition is true

## Loop Control
- `break`: Exit loop immediately
- `continue`: Skip to next iteration
- `pass`: Placeholder that does nothing
"""
    },
    "ch4_functions": {
        "readme": """# Chapter 04: Functions & Functional Programming

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
"""
    },
    "ch5_oop": {
        "readme": """# Chapter 05: Object-Oriented Programming

Python supports full OOP with classes, inheritance, and polymorphism.

## Classes and Objects
```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says woof!"
```

## Dunder Methods
Special methods enclosed in double underscores:
- `__init__`: Constructor
- `__str__`: String representation
- `__repr__`: Official string representation
- `__len__`: Length operation
- `__add__`: Addition operator

## Inheritance
```python
class GoldenRetriever(Dog):
    def bark(self):
        return f"{self.name} says woof woof!"
```

## Polymorphism
Different classes responding differently to the same method call.

## Encapsulation
Using private attributes (by convention with underscore prefix).
"""
    },
    "ch6_exception_handling": {
        "readme": """# Chapter 06: Error & Exception Handling

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
"""
    },
    "ch7_file_io": {
        "readme": """# Chapter 07: File I/O & Context Managers

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
"""
    },
    "ch8_advanced": {
        "readme": """# Chapter 08: Advanced Pythonic Features

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
"""
    },
    "ch9_concurrency": {
        "readme": """# Chapter 09: Concurrency & Async

Python provides multiple ways to handle concurrent operations.

## Threading
For I/O-bound tasks:
```python
import threading
thread = threading.Thread(target=func)
thread.start()
```

## Multiprocessing
For CPU-bound tasks:
```python
from multiprocessing import Process
process = Process(target=func)
process.start()
```

## Async/Await
Modern async programming:
```python
async def fetch_data():
    await asyncio.sleep(1)
    return "Data"
```
"""
    },
    "ch10_stdlib": {
        "readme": """# Chapter 10: Standard Library Highlights

Python's rich standard library includes powerful modules.

## collections
- `Counter`: Count elements
- `defaultdict`: Dictionary with default values
- `namedtuple`: Tuple with named fields
- `OrderedDict`: Dictionary that remembers order

## itertools
- `chain()`: Chain iterables
- `accumulate()`: Cumulative operations
- `groupby()`: Group consecutive elements

## datetime
Working with dates and times.

## os and sys
Operating system interfaces and system parameters.
"""
    },
}

examples = {
    "ch2_data_structures": [
        ("primitive_types.py", '''#!/usr/bin/env python3
"""Demonstrating Python primitive types."""

# Integer
number = 42
print(f"Integer: {number} (type: {type(number).__name__})")

# Float
price = 19.99
print(f"Float: {price} (type: {type(price).__name__})")

# String
name = "Python"
print(f"String: {name} (type: {type(name).__name__})")

# Boolean
is_python_cool = True
print(f"Boolean: {is_python_cool} (type: {type(is_python_cool).__name__})")

# Mixed list
mixed = [1, 2.5, "hello", True]
print(f"\\nMixed list: {mixed}")
print(f"Length: {len(mixed)}")'''),
        ("lists.py", '''#!/usr/bin/env python3
"""Working with Python lists."""

# Creating a list
numbers = [1, 2, 3, 4, 5]
print(f"Original: {numbers}")

# Accessing elements
print(f"First element: {numbers[0]}")
print(f"Last element: {numbers[-1]}")

# List operations
numbers.append(6)
print(f"\\nAfter append(6): {numbers}")

numbers.insert(0, 0)
print(f"After insert(0, 0): {numbers}")

# Slicing
print(f"\\nFirst 3: {numbers[:3]}")
print(f"Last 3: {numbers[-3:]}")

# List comprehension
squares = [x**2 for x in range(5)]
print(f"\\nSquares (0-4): {squares}")

# Mutable - can change
numbers[0] = 100
print(f"\\nAfter numbers[0] = 100: {numbers}")'''),
        ("tuples_sets.py", '''#!/usr/bin/env python3
"""Demonstrating tuples and sets."""

# Tuple - immutable
coordinates = (10.5, 20.3)
print(f"Tuple: {coordinates}")
print(f"Type: {type(coordinates).__name__}")

try:
    coordinates[0] = 5
except TypeError as e:
    print(f"\\nCannot modify: {e}")

# Set - unordered, unique elements
fruits = {"apple", "banana", "apple", "cherry"}
print(f"\\nSet (removes duplicates): {fruits}")

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(f"\\nset1: {set1}")
print(f"set2: {set2}")
print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")'''),
        ("dictionaries.py", '''#!/usr/bin/env python3
"""Working with dictionaries and dict comprehensions."""

# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
print(f"Person: {person}")

# Accessing values
print(f"\\nName: {person.get('name')}")
print(f"Age: {person['age']}")

# Updating
person["age"] = 31
person["email"] = "alice@example.com"
print(f"\\nUpdated: {person}")

# Iterating
print(f"\\nKey-Value pairs:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Dict comprehension
squares = {x: x**2 for x in range(5)}
print(f"\\nDict comprehension: {squares}")'''),
    ],
    "ch3_control_flow": [
        ("if_else.py", '''#!/usr/bin/env python3
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

print(f"\\nAge: {age}")

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

print(f"Score: {score} -> Grade: {grade}")'''),
        ("for_while.py", '''#!/usr/bin/env python3
"""Using for and while loops."""

# For loop with range
print("Counting with for loop:")
for i in range(5):
    print(f"  {i}")

# For loop with list
fruits = ["apple", "banana", "cherry"]
print(f"\\nFruits:")
for i, fruit in enumerate(fruits, 1):
    print(f"  {i}. {fruit}")

# While loop
print(f"\\nWhile loop counting down:")
countdown = 5
while countdown > 0:
    print(f"  {countdown}")
    countdown -= 1
print("Blast off!")

# Iterating over string
print(f"\\nCharacters in 'Python':")
for char in "Python":
    print(f"  {char}")'''),
        ("loop_control.py", '''#!/usr/bin/env python3
"""Using break, continue, and pass."""

print("Using break:")
for i in range(10):
    if i == 5:
        print("  Stopping at 5")
        break
    print(f"  {i}")

print("\\nUsing continue:")
for i in range(5):
    if i == 2:
        print("  Skipping 2")
        continue
    print(f"  {i}")

print("\\nUsing pass:")
class EmptyClass:
    pass  # Will add functionality later

def placeholder():
    pass  # Implement later

print("  Empty class and function created with pass")

# Else clause for loops
print(f"\\nLoop with else:")
for i in range(3):
    print(f"  {i}")
else:
    print("  Looped through all items!")'''),
    ],
    "ch4_functions": [
        ("function_basics.py", '''#!/usr/bin/env python3
"""Function basics and scope."""

def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet("World"))

# Default parameters
def introduce(name, age=25):
    return f"{name} is {age} years old"

print(f"\\nWith default age: {introduce('Bob')}")
print(f"With specified age: {introduce('Bob', 30)}")

# Return multiple values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

stats = get_stats([10, 20, 30, 40, 50])
print(f"\\nMin: {stats[0]}, Max: {stats[1]}, Sum: {stats[2]}")

# Scope demonstration
x = "global"

def scope_test():
    x = "local"
    print(f"Inside function: {x}")

scope_test()
print(f"Outside: {x}")'''),
        ("args_kwargs.py", '''#!/usr/bin/env python3
"""Using *args and **kwargs."""

def print_all(*args):
    """Accept variable positional arguments."""
    print("Positional args:", args)
    for i, arg in enumerate(args):
        print(f"  {i}: {arg}")

print_all(1, 2, 3, 4, 5)

def describe_person(**kwargs):
    """Accept variable keyword arguments."""
    print("Keyword args:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

describe_person(name="Alice", age=30, city="NYC", job="Engineer")

def combine_args_kwargs(*args, **kwargs):
    """Mix both types."""
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

combine_args_kwargs(1, 2, name="Test", value=100)'''),
        ("lambda_map_filter.py", '''#!/usr/bin/env python3
"""Lambda functions and functional programming."""

# Lambda - anonymous function
square = lambda x: x**2
print(f"Lambda square of 5: {square(5)}")

sort_key = lambda person: person["age"]

# Map - apply function to all items
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print(f"\\nSquares using map: {squares}")

# Filter - keep items matching condition
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")

# Practical example
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30}
]

adults = filter(lambda p: p["age"] >= 18, people)
print(f"\\nAdults: {[p['name'] for p in adults]}")'''),
    ],
    "ch5_oop": [
        ("classes.py", '''#!/usr/bin/env python3
"""Classes and objects basics."""

class Dog:
    """A simple Dog class."""
    
    species = "Canis familiaris"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says woof!"
    
    def __str__(self):
        return f"{self.name} ({self.age} years old)"

# Creating instances
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1)
print(f"{dog1.name} says: {dog1.bark()}")
print(f"{dog2.name} says: {dog2.bark()}")
print(f"Species: {Dog.species}")'''),
        ("inheritance.py", '''#!/usr/bin/env python3
"""Inheritance and polymorphism."""

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass
    
    def __str__(self):
        return self.name

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

class Robot(Animal):
    def speak(self):
        return f"{self.name} beeps!"

# Polymorphism example
animals = [Dog("Buddy"), Cat("Whiskers"), Robot("R2D2")]

for animal in animals:
    print(f"{animal} says: {animal.speak()}")'''),
        ("dunder_methods.py", '''#!/usr/bin/env python3
"""Common dunder (double underscore) methods."""

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        return self.pages
    
    def __bool__(self):
        return self.pages > 0
    
    def __add__(self, other):
        return Book(
            "Combined",
            f"{self.author} & {other.author}",
            self.pages + other.pages
        )

# Examples
book1 = Book("Python", "Guido", 300)
book2 = Book("Java", "James", 450)

print(f"str(): {str(book1)}")
print(f"repr(): {repr(book1)}")
print(f"len(): {len(book1)}")
print(f"bool(): {bool(book1)}")
print(f"+ operator: {book1 + book2} ({len(book1 + book2)} pages)")'''),
    ],
    "ch6_exception_handling": [
        ("try_except.py", '''#!/usr/bin/env python3
"""Basic exception handling."""

# Try-except
print("Try-except example:")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  Cannot divide by zero!")

# Specific exceptions
print("\\nSpecific exceptions:")
try:
    age = int("not_a_number")
except ValueError as e:
    print(f"  ValueError: {e}")

# Multiple exceptions
print("\\nMultiple exceptions:")
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"  Caught: {e}")

# Finally
print("\\nWith finally:")
try:
    print("  Attempting operation...")
    result = 5 / 0
except ZeroDivisionError:
    print("  Error caught!")
finally:
    print("  This always runs")'''),
        ("custom_exceptions.py", '''#!/usr/bin/env python3
"""Custom exceptions."""

class InvalidAgeError(Exception):
    """Raised when age is invalid."""
    pass

class NegativeValueError(Exception):
    """Raised for negative values."""
    pass

def set_age(age):
    if age < 0:
        raise NegativeValueError("Age cannot be negative")
    elif age > 150:
        raise InvalidAgeError("Age seems unrealistic")
    else:
        print(f"Age set to: {age}")

try:
    set_age(-5)
except NegativeValueError as e:
    print(f"Caught: {e}")

try:
    set_age(200)
except InvalidAgeError as e:
    print(f"Caught: {e}")

set_age(25)'''),
    ],
    "ch7_file_io": [
        ("file_operations.py", '''#!/usr/bin/env python3
"""Basic file I/O operations."""
import os

filename = "example.txt"

# Writing to file
with open(filename, "w") as f:
    f.write("Line 1\\n")
    f.write("Line 2\\n")
    f.write("Line 3\\n")

print(f"File '{filename}' created and written.")

# Reading file
with open(filename, "r") as f:
    content = f.read()

print(f"\\nFile content:\\n{content}")

# Reading line by line
print("Reading line by line:")
with open(filename, "r") as f:
    for i, line in enumerate(f, 1):
        print(f"  Line {i}: {line.strip()}")

# Cleanup
os.remove(filename)
print(f"\\nCleaned up {filename}")'''),
        ("context_manager.py", '''#!/usr/bin/env python3
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

print("\\nUsing contextmanager decorator:")
with managed_file("test.txt") as f:
    f.write("Managed content")
print("File automatically closed")

# Cleanup
os.remove("test.txt")'''),
    ],
    "ch8_advanced": [
        ("generators.py", '''#!/usr/bin/env python3
"""Generators using yield."""

def count_up_to(n):
    """Generate numbers up to n."""
    i = 1
    while i <= n:
        yield i
        i += 1

print("Numbers 1 to 5:")
for num in count_up_to(5):
    print(f"  {num}")

# Memory efficient generation
print("\\nLarge range (only first 5):")
large_range = count_up_to(1000000)
for i, num in enumerate(large_range):
    print(f"  {num}")
    if i == 4:
        break

# Generator expression
squares = (x**2 for x in range(10))
print(f"\\nGenerator expression: {type(squares)}")
print(f"First 5 squares: {[next(squares) for _ in range(5)]}")'''),
        ("decorators.py", '''#!/usr/bin/env python3
"""Decorators and closures."""

def my_decorator(func):
    """Example decorator."""
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))

# Decorator with arguments
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def shout(text):
    print(text.upper())

shout("hello")

# Real-world: Timing decorator
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()'''),
        ("type_hints.py", '''#!/usr/bin/env python3
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
print(f"User type: {type(user)}")'''),
    ],
    "ch9_concurrency": [
        ("threading.py", '''#!/usr/bin/env python3
"""Threading for I/O-bound tasks."""

import threading
import time

def worker_thread(name, delay):
    """Worker function for threading."""
    for i in range(3):
        print(f"{name}: {i}")
        time.sleep(delay)

# Create and start threads
thread1 = threading.Thread(target=worker_thread, args=("Thread-1", 1))
thread2 = threading.Thread(target=worker_thread, args=("Thread-2", 0.5))

start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(f"\\nCompleted in {time.time()-start:.2f}s")'''),
        ("asyncio_example.py", '''#!/usr/bin/env python3
"""Async/await for concurrent I/O."""

import asyncio

async def fetch_data(name, delay):
    """Simulate fetching data."""
    print(f"{name}: Starting...")
    await asyncio.sleep(delay)
    print(f"{name}: Done!")
    return f"Data from {name}"

async def main():
    """Run concurrent tasks."""
    tasks = [
        fetch_data("Task 1", 2),
        fetch_data("Task 2", 1),
        fetch_data("Task 3", 1.5)
    ]
    
    start = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks)
    end = asyncio.get_event_loop().time()
    
    print(f"\\nResults: {results}")
    print(f"Total time: {end-start:.2f}s")

# Use event loop directly to avoid circular import
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.close()'''),
        ("threading_example.py", '''#!/usr/bin/env python3
"""Threading for concurrent I/O-bound tasks."""

import threading
import time

def worker_thread(name, delay):
    """Worker function for threading."""
    for i in range(3):
        print(f"{name}: {i}")
        time.sleep(delay)

# Create and start threads
thread1 = threading.Thread(target=worker_thread, args=("Thread-1", 1))
thread2 = threading.Thread(target=worker_thread, args=("Thread-2", 0.5))

start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(f"\\nCompleted in {time.time()-start:.2f}s'''),
    ],
    "ch10_stdlib": [
        ("collections.py", '''#!/usr/bin/env python3
"""collections module examples."""

from collections import Counter, defaultdict, namedtuple, OrderedDict

# Counter
fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(fruits)
print("Counter example:")
print(f"  Fruits: {dict(counts)}")
print(f"  Most common: {counts.most_common(2)}")

# defaultdict
words = ["apple", "banana", "apple", "cherry"]
letter_counts = defaultdict(int)
for word in words:
    letter_counts[len(word)] += 1

print("\\ndefaultdict example:")
print(f"  Word lengths: {dict(letter_counts)}")

# NamedTuple
Person = namedtuple("Person", ["name", "age"])
alice = Person("Alice", 30)
print(f"\\nNamedTuple: {alice}")
print(f"  Name: {alice.name}, Age: {alice.age}")

# OrderedDict
od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3
print(f"\\nOrderedDict (remembers insertion order):")
print(f"  {dict(od)}")'''),
        ("itertools.py", '''#!/usr/bin/env python3
"""itertools module examples."""

from itertools import chain, accumulate, groupby

# Chain - combine iterables
lists = [[1, 2, 3], [4, 5], [6]]
combined = list(chain.from_iterable(lists))
print("Chain example:")
print(f"  {combined}")

# Accumulate - cumulative operations
numbers = [1, 2, 3, 4, 5]
cumulative = list(accumulate(numbers))
print(f"\\nAccumulate (sum):   {cumulative}")
cumulative_mult = list(accumulate(numbers, lambda x, y: x*y))
print(f"Accumulate (multiply): {cumulative_mult}")

# GroupBy - group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
groups = {k: list(g) for k, g in groupby(data, key=lambda x: x[0])}
print(f"\\nGroupBy example:")
for key, group in groups.items():
    print(f"  {key}: {group}")'''),
    ],
}

def create_chapters():
    """Create all chapter directories, README files, and examples."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    for chapter_dir, readme_content in CHAPTERS.items():
        content_path = os.path.join(base_path, "content", chapter_dir)
        examples_path = os.path.join(base_path, "examples", chapter_dir)
        
        os.makedirs(content_path, exist_ok=True)
        os.makedirs(examples_path, exist_ok=True)
        
        readme_file = os.path.join(content_path, "README.md")
        with open(readme_file, "w") as f:
            f.write(readme_content["readme"])
        print(f"Created: {readme_file}")
        
        for example_file in examples.get(chapter_dir, []):
            filename, code = example_file
            example_path = os.path.join(examples_path, filename)
            with open(example_path, "w") as f:
                f.write(code)
            print(f"Created: {example_path}")
    
    print(f"\\nCreated {len(CHAPTERS)} chapters!")

if __name__ == "__main__":
    create_chapters()
