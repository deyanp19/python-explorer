#!/usr/bin/env python3
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
    print(f"{animal} says: {animal.speak()}")