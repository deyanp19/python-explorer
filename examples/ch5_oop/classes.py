#!/usr/bin/env python3
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
print(f"Species: {Dog.species}")