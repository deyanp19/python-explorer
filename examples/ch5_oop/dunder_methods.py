#!/usr/bin/env python3
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
print(f"+ operator: {book1 + book2} ({len(book1 + book2)} pages)")