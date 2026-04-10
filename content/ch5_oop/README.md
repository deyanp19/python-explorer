# Chapter 05: Object-Oriented Programming

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
