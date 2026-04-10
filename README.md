# Python Features Explorer

A comprehensive interactive learning platform designed to explore and understand Python programming through hands-on examples and structured content.

## 📋 Overview

**Python Features Explorer** is an interactive CLI application that provides a structured, chapter-based curriculum for learning Python. It combines theoretical content with executable code examples, making it ideal for both beginners and intermediate developers looking to strengthen their Python skills.

### Key Features
- **Interactive Menu System**: Navigate through 10 chapters of Python content
- **Live Code Execution**: Run examples directly from the CLI
- **Structured Learning**: Progress from basics to advanced topics
- **Comprehensive Coverage**: Python fundamentals, OOP, concurrency, and standard library

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required

### Running the Application

```bash
cd /home/dido/projects/python/python_quick_robert_oliver/using_math
python3 main.py
```

### Usage

The application presents an interactive menu:

```
============================================================
                  PYTHON FEATURES EXPLORER
============================================================
1. Ch_1_Introduction
2. Ch_2_Data_Structures
3. Ch_3_Control_Flow
4. Ch_4_Functions
5. Ch_5_Oop
6. Ch_6_Exception_Handling
7. Ch_7_File_Io
8. Ch_8_Advanced
9. Ch_9_Concurrency
10. Ch_10_Stdlib

11. Exit
```

**How to use:**
1. Enter a number (1-10) to select a chapter
2. View the chapter content and available examples
3. Select an example to run
4. View the output and error messages
5. Repeat or choose to exit

### Example Session

```
Select a chapter (1-11)> 1

CHAPTER 1: CH_1_INTRODUCTION
Welcome to Python programming! This chapter covers the fundamentals that will set your foundation.

------------------------------------------------------------
                Available Examples
------------------------------------------------------------
1. Hello_World
2. Comments
3. Zen_Of_Python

1. Select an example to run (1-3)> 1

Running example: Hello_World
----------------------------------------

OUTPUT:
Hello, World!

Example completed with exit code: 0
```

## 📚 Project Structure

```
using_math/
├── main.py                      # Main application entry point
├── math_examples.py            # Standalone math function examples
├── generate_chapters.py        # Chapter content generator
│
├── content/                    # Documentation files
│   ├── ch1_intro/README.md    # Chapter 1: Introduction
│   ├── ch2_data_structures/README.md  # Chapter 2: Data Structures
│   ├── ch3_control_flow/README.md     # Chapter 3: Control Flow
│   ├── ch4_functions/README.md        # Chapter 4: Functions
│   ├── ch5_oop/README.md              # Chapter 5: OOP
│   ├── ch6_exception_handling/README.md # Chapter 6: Exception Handling
│   ├── ch7_file_io/README.md          # Chapter 7: File I/O
│   ├── ch8_advanced/README.md           # Chapter 8: Advanced Features
│   ├── ch9_concurrency/README.md        # Chapter 9: Concurrency
│   └── ch10_stdlib/README.md          # Chapter 10: Standard Library
│
└── examples/                   # Executable code examples
    ├── ch1_intro/
    │   ├── hello_world.py
    │   ├── zen_of_python.py
    │   └── comments.py
    ├── ch2_data_structures/
    ├── ch3_control_flow/
    ├── ch4_functions/
    ├── ch5_oop/
    ├── ch6_exception_handling/
    ├── ch7_file_io/
    ├── ch8_advanced/
    ├── ch9_concurrency/
    └── ch10_stdlib/
```

## 📖 Chapter Curriculum

### Chapter 1: Introduction
**Topics Covered:**
- What is Python?
- Basic syntax and indentation
- Comments and docstrings
- The Zen of Python

**Learning Outcomes:**
- Understand Python's design philosophy
- Write your first Python program
- Comment code effectively

### Chapter 2: Data Structures
**Topics Covered:**
- Primitive types (int, float, str, bool)
- Lists (mutable, ordered collections)
- Tuples (immutable, ordered collections)
- Sets (unordered, unique elements)
- Dictionaries (key-value pairs)
- List comprehensions

**Learning Outcomes:**
- Choose the appropriate data structure for your needs
- Manipulate collections efficiently
- Use comprehensions for cleaner code

### Chapter 3: Control Flow
**Topics Covered:**
- Conditional statements (if, elif, else)
- Loops (for, while)
- Loop control (break, continue, pass)

**Learning Outcomes:**
- Implement conditional logic
- Iterate over data structures
- Control program flow effectively

### Chapter 4: Functions & Functional Programming
**Topics Covered:**
- Function definition and parameters
- *args and **kwargs
- Variable scope (LEGB rule)
- Lambda functions
- Functional programming (map, filter, reduce)

**Learning Outcomes:**
- Write reusable, modular code
- Understand variable scope
- Use functional programming patterns

### Chapter 5: Object-Oriented Programming
**Topics Covered:**
- Classes and objects
- Dunder methods (__init__, __str__, __repr__, __len__, __add__)
- Inheritance and polymorphism
- Encapsulation (private attributes)

**Learning Outcomes:**
- Design classes and objects
- Implement inheritance hierarchies
- Use Python's magic methods effectively

### Chapter 6: Exception Handling
**Topics Covered:**
- Try-except blocks
- Multiple exception handling
- Finally clause
- Custom exceptions

**Learning Outcomes:**
- Handle errors gracefully
- Create custom exception classes
- Write robust, error-resistant code

### Chapter 7: File I/O & Context Managers
**Topics Covered:**
- Reading and writing files
- Context managers and the `with` statement
- Custom context managers

**Learning Outcomes:**
- Handle files safely and efficiently
- Create custom context managers
- Understand resource management

### Chapter 8: Advanced Pythonic Features
**Topics Covered:**
- Generators and yield
- Decorators
- Type hints

**Learning Outcomes:**
- Create memory-efficient generators
- Use decorators to enhance functions
- Add type annotations for better code clarity

### Chapter 9: Concurrency & Async
**Topics Covered:**
- Threading for I/O-bound tasks
- Multiprocessing for CPU-bound tasks
- Async/await for modern async programming

**Learning Outcomes:**
- Understand concurrent programming concepts
- Choose the right concurrency model
- Write asynchronous Python code

### Chapter 10: Standard Library Highlights
**Topics Covered:**
- collections module (Counter, defaultdict, namedtuple, OrderedDict)
- itertools module (chain, accumulate, groupby)
- datetime module
- os and sys modules

**Learning Outcomes:**
- Leverage built-in data structures
- Use itertools for efficient iteration
- Work with system and datetime operations

## 🛠️ Component Details

### `main.py` - Application Core

The main application that orchestrates the learning experience:

```python
class PythonExplorer:
    """Main application class for exploring Python features."""
```

**Key Methods:**
- `__init__()`: Initializes and loads chapter data
- `display_menu()`: Shows the main navigation menu
- `display_chapter_details()`: Displays chapter content and examples
- `run_example()`: Executes selected example scripts with output display

### `generate_chapters.py` - Content Generator

A script used to generate and manage chapter documentation. This utility:
- Creates structured content files
- Organizes example files by chapter
- Maintains consistent formatting across all documentation

### `math_examples.py` - Mathematical Operations

A standalone file demonstrating Python's `math` module capabilities:

```python
# Basic Operations
print(f"ceil(1.1) = {math.ceil(1.1)}")          # 2
print(f"floor(1.1) = {math.floor(1.1)}")      # 1

# Trigonometry
print(f"sin(math.pi/2) = {math.sin(math.pi/2)}")     # 1.0
print(f"cos(0) = {math.cos(0)}")                      # 1.0
```

**Functions Demonstrated:**
- Rounding: `ceil()`, `floor()`, `trunc()`, `round()`
- Absolute: `fabs()`
- Modulo: `fmod()`
- Trigonometry: `sin()`, `cos()`, `tan()`, `asin()`, `acos()`, `atan()`
- Conversions: `degrees()`, `radians()`
- Exponential: `pow()`, `sqrt()`, `exp()`, `log()`, `log10()`, `log2()`
- Geometry: `hypot()`
- Constants: `math.e`, `math.pi`
- Special Values: `inf`, `nan`

## 🧪 Testing & Running Examples

### Running Individual Examples

You can run any example script directly:

```bash
python3 examples/ch1_intro/hello_world.py
python3 examples/ch5_oop/classes.py
python3 examples/ch7_file_io/file_operations.py
```

### Running All Examples

You can create a simple script to run all examples:

```python
#!/usr/bin/env python3
"""Run all examples in the project."""

import subprocess
import os
from pathlib import Path

examples_dir = Path("examples")

for chapter_dir in examples_dir.iterdir():
    if chapter_dir.is_dir():
        print(f"\n{'='*50}")
        print(f"Running examples from {chapter_dir.name}")
        print(f"{'='*50}")
        
        for example_file in chapter_dir.glob("*.py"):
            print(f"\n→ {example_file.stem}")
            print("-" * 40)
            
            try:
                result = subprocess.run(
                    ["python3", str(example_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"Errors: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print("ERROR: Example timed out")
            except Exception as e:
                print(f"ERROR: {e}")
```

## 🔧 Extending the Project

### Adding a New Chapter

1. **Create content directory:**
   ```bash
   mkdir content/ch11_new_topic
   ```

2. **Create README.md:**
   ```markdown
   # Chapter 11: New Topic
   
   Description of what this chapter covers.
   ```

3. **Create examples directory:**
   ```bash
   mkdir examples/ch11_new_topic
   ```

4. **Add example scripts:**
   ```python
   # examples/ch11_new_topic/example_one.py
   print("Example code running...")
   ```

5. **Restart the application** to see the new chapter appear

### Creating Custom Examples

Follow the pattern used in existing examples:
- Keep files focused on a single concept
- Include clear print statements showing output
- Handle potential errors gracefully
- Add comments explaining the code

## 📊 Example Code Organization

### Content Files (README.md)
Each chapter's README.md follows a consistent structure:
- Chapter title and number
- Brief introduction
- Code snippets demonstrating concepts
- Key points and takeaways

### Example Files
All example files in the `examples/` directory are:
- Self-contained and executable
- Annotated with comments
- Designed to demonstrate specific concepts
- Named to clearly indicate their purpose

## 🐍 Python Version Compatibility

This project is designed for **Python 3.6+** and supports:
- Type hints (3.5+)
- f-strings (3.6+)
- Async/await syntax (3.5+)
- Modern best practices

## 📝 Best Practices Demonstrated

Throughout this project, you'll learn:
- Writing clean, readable code
- Proper error handling
- Using context managers for resource management
- Object-oriented design principles
- Functional programming patterns
- Efficient data structure usage
- Concurrency best practices

## 🤝 Contributing

To contribute to this project:

1. **Follow existing patterns** - Match the style of current examples
2. **Keep examples focused** - One concept per file
3. **Add clear comments** - Explain what the code does
4. **Test your examples** - Ensure they run without errors
5. **Update documentation** - Revise README files for new content

## 📄 License

This project is educational material for learning Python. Feel free to use and modify for learning purposes.

## 🎯 Learning Path Recommendations

### For Complete Beginners:
1. Chapter 1 (Introduction)
2. Chapter 2 (Data Structures)
3. Chapter 3 (Control Flow)
4. Chapter 4 (Functions)
5. Chapter 5 (OOP)

### For Intermediate Developers:
1. Chapter 6 (Exception Handling)
2. Chapter 7 (File I/O)
3. Chapter 8 (Advanced Features)
4. Chapter 9 (Concurrency)
5. Chapter 10 (Standard Library)

### For Quick Reference:
- Chapter 2 (Data Structures)
- Chapter 4 (Functions)
- Chapter 10 (Standard Library)

## 📞 Feedback & Support

This is an educational tool designed for learning. If you find errors, have suggestions for improvement, or want to contribute new examples, please create an issue or pull request.

---

**Happy Python coding! 🐍**

*This project demonstrates core Python concepts through practical, executable examples. Each chapter builds upon the previous one, creating a comprehensive learning experience from basics to advanced topics.*
# python-explorer
