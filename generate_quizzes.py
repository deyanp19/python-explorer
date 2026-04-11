#!/usr/bin/env python3
"""Quiz Question Generator for Python Features Explorer.

This script automatically generates quiz questions from chapter README files.
It can be used to create quizzes for any chapter to test comprehension.
"""

import os
import re
import json
import yaml
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    """Represents a quiz question."""
    chapter_number: str
    question: str
    options: List[str]
    answer: int  # 1-indexed
    explanation: str


class QuizGenerator:
    """Generate quiz questions from chapter content."""

    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize quiz generator."""
        self.config = self._load_config(config_path)
        self.questions_history: List[QuizQuestion] = []

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration."""
        default_config = {
            'quizzes': {
                'questions_per_chapter': 5,
                'passing_score': 70,
                'allow_retries': True,
                'max_attempts': 3,
            }
        }

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        self._merge_config(default_config, yaml_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

        return default_config

    def _merge_config(self, base: Dict, override: Dict) -> None:
        """Merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def generate_quiz(self, readme_path: str, chapter_number: str,
                      num_questions: Optional[int] = None) -> List[QuizQuestion]:
        """Generate quiz questions from a README file.
        
        Generates up to 11 comprehensive questions covering various aspects
        of Python programming, ensuring all quizzes have consistent question counts.
        """
        if not num_questions:
            num_questions = 11  # Fixed to always generate 11 questions

        if not os.path.exists(readme_path):
            print(f"Error: File not found: {readme_path}")
            return []

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            questions = []

            # Try to generate questions from actual content patterns
            code_questions = self._generate_code_example_questions(content, chapter_number)
            topic_questions = self._generate_topic_questions(content, chapter_number)
            concept_questions = self._generate_concept_questions(content, chapter_number)
            
            # Use content-based questions if found, otherwise use all fallback
            if code_questions or topic_questions or concept_questions:
                questions.extend(code_questions)
                questions.extend(topic_questions)
                questions.extend(concept_questions)
                
                # If we still don't have 11, supplement with fallback questions
                if len(questions) < 11:
                    fallback_questions = self._generate_fallback_questions(content, chapter_number)
                    questions.extend(fallback_questions)
            else:
                # Use only fallback questions
                questions = self._generate_fallback_questions(content, chapter_number)

            # Ensure exactly 11 questions
            questions = questions[:11]

            self.questions_history.extend(questions)
            return questions

        except Exception as e:
            print(f"Error generating quiz: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _generate_code_example_questions(self, content: str,
                                        chapter_number: str) -> List[QuizQuestion]:
        """Generate questions based on code examples in the content."""
        questions = []

        # Find Python code blocks
        code_blocks = re.findall(r'```python\s*\n(.*?)\n```', content, re.DOTALL)

        for i, block in enumerate(code_blocks[:3]):  # Limit to first 3 blocks
            # Extract key function or concept from code
            keywords = re.findall(r'\b(import|from|class|def|print)\s+(\S+)', block)

            if keywords:
                topic = ' '.join([k[1] for k in keywords[:2]])

                question = QuizQuestion(
                    chapter_number=chapter_number,
                    question=f"What module or function is imported/used in the code example?",
                    options=[
                        topic,
                        f"Random {topic}_alternate",
                        f"Related {topic}_module",
                        "Python standard library"
                    ],
                    answer=1 if topic else 4,
                    explanation=f"The example uses {topic or 'Python standard library features'}"
                )
                questions.append(question)

        return questions

    def _generate_topic_questions(self, content: str,
                                  chapter_number: str) -> List[QuizQuestion]:
        """Generate questions based on chapter topics discussed."""
        questions = []

        # Find chapter title
        title_match = re.search(r'Chapter\s+(\d+)\s*[:\s]*(.+)$', content, re.MULTILINE)

        if title_match:
            chapter_num = title_match.group(1)
            chapter_title = title_match.group(2).strip()

            # Count occurrences of key Python modules
            module_counts = {}
            for module in ['math', 'os', 'sys', 'datetime', 'collections', 'itertools', 'json', 're', 'random']:
                count = len(re.findall(rf'\b{module}\b', content, re.IGNORECASE))
                if count > 0:
                    module_counts[module] = count

            if module_counts:
                most_used = max(module_counts, key=module_counts.get)
                questions.append(QuizQuestion(
                    chapter_number=chapter_num,
                    question=f"What Python module appears most frequently in this chapter?",
                    options=[
                        most_used.capitalize(),
                        "Other module",
                        "No modules used",
                        "External libraries only"
                    ],
                    answer=1,
                    explanation=f"The '{most_used}' module is mentioned {module_counts[most_used]} times"
                ))

        return questions

    def _generate_concept_questions(self, content: str,
                                    chapter_number: str) -> List[QuizQuestion]:
        """Generate questions based on concepts explained in content."""
        questions = []

        # Find numbered lists (likely learning objectives)
        numbered_items = re.findall(r'(\d+)\.\s+(.+?)(?=\n\d+\.|\Z)', content, re.DOTALL)

        if len(numbered_items) >= 2:
            first_item = numbered_items[0][1].strip()[:80]

            questions.append(QuizQuestion(
                chapter_number=chapter_number,
                question=f"In this chapter, students will learn about:",
                options=[
                    f"Key Python feature: {first_item}",
                    "Advanced algorithms",
                    "Database management",
                    "Network programming"
                ],
            answer=1,
            explanation="The print() function outputs data to the console"
        ))
        
        # Question 9: Functions
        questions.append(QuizQuestion(
            chapter_number=chapter_number,
            question="What keyword is used to define a function?",
            options=[
                "func",
                "define",
                "function",
                "def"
            ],
            answer=4,
            explanation="The 'def' keyword defines functions in Python"
        ))
        
        # Question 10: Modules
        questions.append(QuizQuestion(
            chapter_number=chapter_number,
            question="What is a Python module?",
            options=[
                "A compiled executable",
                "A file containing Python code",
                "A database connection",
                "A network protocol"
            ],
            answer=2,
            explanation="Modules are files containing Python code that can be imported"
        ))
        
        # Question 11: Syntax
        questions.append(QuizQuestion(
            chapter_number=chapter_number,
            question="Which character starts a comment in Python?",
            options=[
                "//",
                "/*",
                "#",
                "--"
            ],
            answer=3,
            explanation="The # symbol starts a comment in Python"
        ))
        
        return questions

    def _generate_chapter_1_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 1: Getting Started."""
        questions = [
            QuizQuestion(
                chapter_number="1",
                question="What is the correct function to output text in Python?",
                options=["output()", "print()", "write()", "echo()"],
                answer=2,
                explanation="The print() function outputs text to the console in Python."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What symbol is used for single-line comments?",
                options=["//", "#", "/*", "--"],
                answer=2,
                explanation="The # symbol starts single-line comments in Python."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What is the correct file extension for Python files?",
                options=[".py", ".python", ".pt", ".pc"],
                answer=1,
                explanation="Python files use the .py extension."
            ),
            QuizQuestion(
                chapter_number="1",
                question="Which keyword imports modules in Python?",
                options=["include", "import", "using", "require"],
                answer=2,
                explanation="The import keyword is used to import modules."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What data type represents decimal numbers?",
                options=["int", "float", "str", "bool"],
                answer=2,
                explanation="The float data type represents decimal numbers."
            ),
            QuizQuestion(
                chapter_number="1",
                question="Which keyword defines a function?",
                options=["func", "define", "def", "function"],
                answer=3,
                explanation="The def keyword defines functions in Python."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What does Python use to define code blocks?",
                options=["Braces", "Indentation", "Semicolons", "Keywords"],
                answer=2,
                explanation="Python uses indentation to define code blocks."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What is Python primarily known for?",
                options=["Complex syntax", "Readability", "Speed", "Hardware control"],
                answer=2,
                explanation="Python is known for its simple and readable syntax."
            ),
            QuizQuestion(
                chapter_number="1",
                question="Which built-in function returns the type of an object?",
                options=["kind()", "type()", "category()", "class()"],
                answer=2,
                explanation="The type() function returns the data type of an object."
            ),
            QuizQuestion(
                chapter_number="1",
                question="What is the result of 10 / 3 in Python 3?",
                options=["3", "3.33", "3.0", "3.333..."],
                answer=4,
                explanation="Python 3 division returns a float result."
            ),
            QuizQuestion(
                chapter_number="1",
                question="Which statement creates a variable?",
                options=["var x = 5", "int x = 5", "x = 5", "declare x = 5"],
                answer=3,
                explanation="Python uses simple assignment: variable_name = value."
            )
        ]
        return questions
    
    def _generate_chapter_2_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 2: Data Structures."""
        questions = [
            QuizQuestion(
                chapter_number="2",
                question="Which data structure is ordered and mutable?",
                options=["list", "tuple", "set", "dict"],
                answer=1,
                explanation="Lists are ordered and mutable (can be changed)."
            ),
            QuizQuestion(
                chapter_number="2",
                question="Which data structure is ordered but immutable?",
                options=["list", "tuple", "set", "dict"],
                answer=2,
                explanation="Tuples are ordered and immutable (cannot be changed)."
            ),
            QuizQuestion(
                chapter_number="2",
                question="What syntax is used to create a dictionary?",
                options=["[]", "()", "{}", "<>"],
                answer=3,
                explanation="Curly braces {} are used to create dictionaries."
            ),
            QuizQuestion(
                chapter_number="2",
                question="How do you access an element by index in a list?",
                options=["list.key", "list[index]", "list.name", "list(0)"],
                answer=2,
                explanation="Square brackets with index: list[index] accesses elements."
            ),
            QuizQuestion(
                chapter_number="2",
                question="Which method adds an element to the end of a list?",
                options=["push()", "add()", "append()", "insert()"],
                answer=3,
                explanation="append() adds an element to the end of a list."
            ),
            QuizQuestion(
                chapter_number="2",
                question="What does set() do with duplicate values?",
                options=["Keeps all duplicates", "Removes duplicates", "Errors out", "Counts them"],
                answer=2,
                explanation="Sets automatically remove duplicate values."
            ),
            QuizQuestion(
                chapter_number="2",
                question="Which syntax creates a list comprehension?",
                options=["for x in list: x", "[x for x in list]", "list(x for x in list)", "(x for x in list)"],
                answer=2,
                explanation="List comprehensions use square brackets: [expression for item in iterable]."
            ),
            QuizQuestion(
                chapter_number="2",
                question="How do you get the number of elements in a list?",
                options=["list.size()", "list.length", "len(list)", "size(list)"],
                answer=3,
                explanation="The len() function returns the number of elements."
            ),
            QuizQuestion(
                chapter_number="2",
                question="Which data structure stores key-value pairs?",
                options=["list", "tuple", "set", "dict"],
                answer=4,
                explanation="Dictionaries store data as key-value pairs."
            ),
            QuizQuestion(
                chapter_number="2",
                question="What is the main difference between list and tuple?",
                options=["Lists are immutable", "Tuples are immutable", "Lists can only store ints", "Tuples are unordered"],
                answer=2,
                explanation="Tuples are immutable (cannot be modified after creation)."
            ),
            QuizQuestion(
                chapter_number="2",
                question="Which operator checks if an item is in a list?",
                options=["in", "contains", "has", "is"],
                answer=1,
                explanation="The in operator checks membership: item in list."
            )
        ]
        return questions
    
    def _generate_chapter_3_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 3: Control Flow."""
        questions = [
            QuizQuestion(
                chapter_number="3",
                question="Which keyword starts a conditional statement?",
                options=["when", "else", "if", "case"],
                answer=3,
                explanation="The if keyword begins conditional statements."
            ),
            QuizQuestion(
                chapter_number="3",
                question="What keyword exits a loop immediately?",
                options=["break", "continue", "exit", "stop"],
                answer=1,
                explanation="The break statement exits a loop immediately."
            ),
            QuizQuestion(
                chapter_number="3",
                question="What keyword skips to the next iteration?",
                options=["break", "continue", "skip", "next"],
                answer=2,
                explanation="The continue statement skips to the next loop iteration."
            ),
            QuizQuestion(
                chapter_number="3",
                question="Which keyword is used for iteration loops?",
                options=["while", "for", "repeat", "loop"],
                answer=2,
                explanation="The for keyword is used for iterating over sequences."
            ),
            QuizQuestion(
                chapter_number="3",
                question="What keyword starts a loop based on a condition?",
                options=["while", "for", "if", "until"],
                answer=1,
                explanation="The while loop repeats while a condition is true."
            ),
            QuizQuestion(
                chapter_number="3",
                question="Which keyword handles alternative conditions?",
                options=["else", "otherwise", "alt", "switch"],
                answer=1,
                explanation="The else keyword handles alternative conditions."
            ),
            QuizQuestion(
                chapter_number="3",
                question="What keyword handles additional conditions?",
                options=["elif", "else if", "elseif", "if else"],
                answer=1,
                explanation="The elif keyword checks additional conditions."
            ),
            QuizQuestion(
                chapter_number="3",
                question="Which statement is a placeholder that does nothing?",
                options=["null", "pass", "skip", "ignore"],
                answer=2,
                explanation="The pass statement is a placeholder that does nothing."
            ),
            QuizQuestion(
                chapter_number="3",
                question="Can you use else with for loops?",
                options=["No", "Yes, executes when loop finishes", "Yes, executes when loop breaks", "Only with while"],
                answer=2,
                explanation="Yes, else with for executes when the loop finishes normally."
            ),
            QuizQuestion(
                chapter_number="3",
                question="What is the indentation requirement in Python?",
                options=["Optional", "4 spaces minimum", "Consistent indentation required", "Any spaces work"],
                answer=3,
                explanation="Python requires consistent indentation for code blocks."
            ),
            QuizQuestion(
                chapter_number="3",
                question="How do you write a multi-way conditional?",
                options=["if-else", "if-elif-else", "switch-case", "multiple-if"],
                answer=2,
                explanation="Use if-elif-else chains for multi-way conditionals."
            )
        ]
        return questions
    
    def _generate_chapter_4_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 4: Functions."""
        questions = [
            QuizQuestion(
                chapter_number="4",
                question="Which keyword defines a function?",
                options=["func", "define", "def", "function"],
                answer=3,
                explanation="The def keyword is used to define functions."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What are *args used for?",
                options=["Keyword arguments", "Variable positional arguments", "Default arguments", "Named arguments"],
                answer=2,
                explanation="*args collects variable positional arguments into a tuple."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What are **kwargs used for?",
                options=["Positional arguments", "Variable keyword arguments", "Required arguments", "Default arguments"],
                answer=2,
                explanation="**kwargs collects variable keyword arguments into a dictionary."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What keyword creates anonymous functions?",
                options=["lambda", "anonymous", "fn", "func"],
                answer=1,
                explanation="The lambda keyword creates anonymous (unnamed) functions."
            ),
            QuizQuestion(
                chapter_number="4",
                question="Which function applies a function to all items?",
                options=["map()", "apply()", "do()", "run()"],
                answer=1,
                explanation="map() applies a function to each item in an iterable."
            ),
            QuizQuestion(
                chapter_number="4",
                question="Which function filters items based on a condition?",
                options=["filter()", "select()", "where()", "extract()"],
                answer=1,
                explanation="filter() constructs an iterator from items where the function returns true."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What does the LEGB rule refer to?",
                options=["Loop structures", "Variable scope", "Function arguments", "Module imports"],
                answer=2,
                explanation="LEGB rules the order of variable scope: Local, Enclosing, Global, Built-in."
            ),
            QuizQuestion(
                chapter_number="4",
                question="Where are local variables defined?",
                options=["Inside functions", "Outside functions", "In classes", "In modules"],
                answer=1,
                explanation="Local variables are defined inside functions."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What is the purpose of a function?",
                options=["To repeat code", "To organize reusable code", "To define variables", "To import modules"],
                answer=2,
                explanation="Functions organize code into reusable, named blocks."
            ),
            QuizQuestion(
                chapter_number="4",
                question="How do you return a value from a function?",
                options=["print()", "return", "export", "yield"],
                answer=2,
                explanation="The return statement sends a value back from a function."
            ),
            QuizQuestion(
                chapter_number="4",
                question="What happens if a function has no return statement?",
                options=["Errors", "Returns None", "Returns 0", "Returns False"],
                answer=2,
                explanation="Functions without return statements return None."
            )
        ]
        return questions
    
    def _generate_chapter_5_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 5: Object-Oriented Programming."""
        questions = [
            QuizQuestion(
                chapter_number="5",
                question="What keyword defines a class?",
                options=["class", "define", "object", "struct"],
                answer=1,
                explanation="The class keyword is used to define classes."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What is the constructor method in Python classes?",
                options=["__init__", "__construct__", "__start__", "__build__"],
                answer=1,
                explanation="__init__ is the constructor method called when creating objects."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What are methods ending with __ called?",
                options=["Private methods", "Dunder methods", "Static methods", "Class methods"],
                answer=2,
                explanation="Methods with double underscores are called dunder or magic methods."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What does inheritance allow?",
                options=["Multiple classes", "Class reuse and extension", "Function overloading", "Variable types"],
                answer=2,
                explanation="Inheritance allows creating new classes that reuse and extend existing classes."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What is the first parameter of instance methods?",
                options=["self", "this", "cls", "object"],
                answer=1,
                explanation="self refers to the instance and is the first parameter of instance methods."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What is polymorphism?",
                options=["Many constructors", "Same method, different classes", "Hidden data", "Class nesting"],
                answer=2,
                explanation="Polymorphism allows different classes to respond differently to the same method call."
            ),
            QuizQuestion(
                chapter_number="5",
                question="How do you create an instance of a class?",
                options=["class()", "new Class()", "Class()", "make Class()"],
                answer=3,
                explanation="Call the class like a function: Class_Name()"
            ),
            QuizQuestion(
                chapter_number="5",
                question="What does __str__ method do?",
                options=["Compares objects", "Returns string representation", "Initializes", "Destroys"],
                answer=2,
                explanation="__str__ returns a human-readable string representation of the object."
            ),
            QuizQuestion(
                chapter_number="5",
                question="What is encapsulation?",
                options=["Multiple classes", "Hiding implementation details", "Class inheritance", "Method overloading"],
                answer=2,
                explanation="Encapsulation hides internal details and exposes only necessary interfaces."
            ),
            QuizQuestion(
                chapter_number="5",
                question="How do you access an object attribute?",
                options=["object(attribute)", "object.attribute", "object[attribute]", "object->attribute"],
                answer=2,
                explanation="Use dot notation: object.attribute"
            ),
            QuizQuestion(
                chapter_number="5",
                question="What is the base class for all Python classes?",
                options=["Base", "Root", "object", "Parent"],
                answer=3,
                explanation="object is the base class for all Python classes."
            )
        ]
        return questions
    
    def _generate_chapter_6_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 6: Exception Handling."""
        questions = [
            QuizQuestion(
                chapter_number="6",
                question="Which block handles exceptions?",
                options=["except", "error", "catch", "handle"],
                answer=1,
                explanation="The except block handles exceptions."
            ),
            QuizQuestion(
                chapter_number="6",
                question="Which block always executes?",
                options=["finally", "always", "end", "done"],
                answer=1,
                explanation="The finally block always executes, regardless of exceptions."
            ),
            QuizQuestion(
                chapter_number="6",
                question="What happens when dividing by zero?",
                options=["Returns 0", "Returns None", "Raises ZeroDivisionError", "Returns infinity"],
                answer=3,
                explanation="Division by zero raises a ZeroDivisionError."
            ),
            QuizQuestion(
                chapter_number="6",
                question="How do you catch multiple exception types?",
                options=["Multiple except blocks", "except (Exception1, Exception2)", "catch {Exception1, Exception2}", "one except for all"],
                answer=2,
                explanation="Use except (Exception1, Exception2) to catch multiple types."
            ),
            QuizQuestion(
                chapter_number="6",
                question="What keyword raises an exception?",
                options=["throw", "raise", "error", "trigger"],
                answer=2,
                explanation="The raise keyword is used to manually raise exceptions."
            ),
            QuizQuestion(
                chapter_number="6",
                question="What is the base exception class?",
                options=["Error", "Exception", "BaseError", "StandardError"],
                answer=2,
                explanation="Exception is the base class for all built-in exceptions."
            ),
            QuizQuestion(
                chapter_number="6",
                question="Which block contains risky code?",
                options=["try", "risky", "danger", "risky"],
                answer=1,
                explanation="The try block contains code that might raise exceptions."
            ),
            QuizQuestion(
                chapter_number="6",
                question="How do you create a custom exception?",
                options=["class CustomError(Exception)", "def CustomError(Exception)", "class Exception(CustomError)", "def Exception(CustomError)"],
                answer=1,
                explanation="Custom exceptions inherit from Exception: class CustomError(Exception)."
            ),
            QuizQuestion(
                chapter_number="6",
                question="Can you have else with try-except?",
                options=["No", "Yes, executes if no exception", "Only with finally", "Yes, always"],
                answer=2,
                explanation="Yes, else executes when no exception is raised in try."
            ),
            QuizQuestion(
                chapter_number="6",
                question="What exception occurs with invalid type conversion?",
                options=["TypeError", "ValueError", "SyntaxError", "NameError"],
                answer=2,
                explanation="ValueError occurs when a function receives an argument of correct type but invalid value."
            ),
            QuizQuestion(
                chapter_number="6",
                question="What exception occurs with undefined variables?",
                options=["UndefinedError", "NameError", "VariableError", "ReferenceError"],
                answer=2,
                explanation="NameError occurs when a variable is not defined."
            )
        ]
        return questions
    
    def _generate_chapter_7_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 7: File I/O."""
        questions = [
            QuizQuestion(
                chapter_number="7",
                question="Which keyword ensures proper resource cleanup?",
                options=["try", "finally", "with", "resource"],
                answer=3,
                explanation="The with keyword ensures proper resource cleanup using context managers."
            ),
            QuizQuestion(
                chapter_number="7",
                question="Which function opens files?",
                options=["file()", "open()", "read()", "fopen()"],
                answer=2,
                explanation="The open() function is used to open files in Python."
            ),
            QuizQuestion(
                chapter_number="7",
                question="What mode opens a file for writing?",
                options=["r", "w", "a", "x"],
                answer=2,
                explanation="The w mode opens a file for writing (overwrites existing content)."
            ),
            QuizQuestion(
                chapter_number="7",
                question="What mode opens a file for reading?",
                options=["r", "w", "a", "x"],
                answer=1,
                explanation="The r mode opens a file for reading (default mode)."
            ),
            QuizQuestion(
                chapter_number="7",
                question="How do you read the entire file content?",
                options=["file.read()", "file.readline()", "file.readlines()", "file.content()"],
                answer=1,
                explanation="The read() method reads the entire file content as a string."
            ),
            QuizQuestion(
                chapter_number="7",
                question="How do you read one line from a file?",
                options=["file.read()", "file.readline()", "file.readlines()", "file.line()"],
                answer=2,
                explanation="The readline() method reads one line from the file."
            ),
            QuizQuestion(
                chapter_number="7",
                question="How do you read all lines into a list?",
                options=["file.read()", "file.readline()", "file.readlines()", "file.lines()"],
                answer=3,
                explanation="The readlines() method reads all lines into a list."
            ),
            QuizQuestion(
                chapter_number="7",
                question="Which method writes to a file?",
                options=["file.write()", "file.print()", "file.output()", "file.send()"],
                answer=1,
                explanation="The write() method writes a string to the file."
            ),
            QuizQuestion(
                chapter_number="7",
                question="What happens when opening a non-existent file in w mode?",
                options=["Error", "Creates new file", "Returns None", "Opens read-only"],
                answer=2,
                explanation="Opening in w mode creates a new file if it does not exist."
            ),
            QuizQuestion(
                chapter_number="7",
                question="What is a context manager?",
                options=["File handler", "Manages resources with with statement", "Exception handler", "Variable manager"],
                answer=2,
                explanation="A context manager manages resources using the with statement, ensuring cleanup."
            ),
            QuizQuestion(
                chapter_number="7",
                question="Which module provides contextmanager decorator?",
                options=["contextlib", "context", "manager", "withlib"],
                answer=1,
                explanation="The contextlib module provides the contextmanager decorator."
            )
        ]
        return questions
    
    def _generate_chapter_8_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 8: Advanced Python Features."""
        questions = [
            QuizQuestion(
                chapter_number="8",
                question="Which keyword creates a generator?",
                options=["generate", "yield", "return", "yield from"],
                answer=2,
                explanation="The yield keyword produces a value and pauses the function."
            ),
            QuizQuestion(
                chapter_number="8",
                question="What is the main benefit of generators?",
                options=["Faster execution", "Memory efficiency", "Parallel processing", "Type safety"],
                answer=2,
                explanation="Generators are memory efficient as they generate values on-demand."
            ),
            QuizQuestion(
                chapter_number="8",
                question="Which decorator modifies a function?",
                options=["decorator", "@decorator_name", "decorate", "@wrap"],
                answer=2,
                explanation="Decorators use @decorator_name syntax above the function."
            ),
            QuizQuestion(
                chapter_number="8",
                question="What is a decorator?",
                options=["A class method", "A function that modifies another function", "A variable marker", "A type hint"],
                answer=2,
                explanation="A decorator is a function that takes another function and extends its behavior."
            ),
            QuizQuestion(
                chapter_number="8",
                question="What is the purpose of type hints?",
                options=["Runtime type checking", "Code documentation and IDE support", "Faster execution", "Memory management"],
                answer=2,
                explanation="Type hints improve code documentation and enable better IDE autocomplete."
            ),
            QuizQuestion(
                chapter_number="8",
                question="Which operator is used for unpacking in function calls?",
                options=["*", "**", "spread", "expand"],
                answer=2,
                explanation="** is used for unpacking keyword arguments (dictionaries)."
            ),
            QuizQuestion(
                chapter_number="8",
                question="What does the * operator do for unpacking?",
                options=["Unpacks keyword args", "Unpacks positional args", "Multiplies", "Splat operator"],
                answer=2,
                explanation="* unpacks positional arguments (lists, tuples) into separate parameters."
            ),
            QuizQuestion(
                chapter_number="8",
                question="Which keyword creates a lambda function?",
                options=["lambda", "anonymous", "fn", "func"],
                answer=1,
                explanation="The lambda keyword creates small anonymous functions."
            ),
            QuizQuestion(
                chapter_number="8",
                question="What is the syntax for type hinting a function?",
                options=["def func(x: int) -> int:", "def func(x int) int:", "def func(x: int):", "def func(int x): int"],
                answer=1,
                explanation="Type hints use def func(param: type) -> return_type:"
            ),
            QuizQuestion(
                chapter_number="8",
                question="What is a generator function?",
                options=["A function returning a list", "A function using yield", "A function creating objects", "A function generating random numbers"],
                answer=2,
                explanation="A generator function uses yield to produce a sequence of values."
            ),
            QuizQuestion(
                chapter_number="8",
                question="How many times can a generator yield values?",
                options=["Once", "Multiple times", "Twice", "Never"],
                answer=2,
                explanation="Generators can yield multiple values, resuming from where they paused."
            )
        ]
        return questions
    
    def _generate_chapter_9_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 9: Concurrency."""
        questions = [
            QuizQuestion(
                chapter_number="9",
                question="Which module provides threading support?",
                options=["threading", "threads", "concurrent", "asyncio"],
                answer=1,
                explanation="The threading module provides thread-based parallelism."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which method starts a thread?",
                options=["thread.start()", "thread.run()", "start(thread)", "thread.begin()"],
                answer=1,
                explanation="The start() method begins thread execution."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which module provides multiprocessing support?",
                options=["multiprocessing", "processes", "parallel", "multiprocess"],
                answer=1,
                explanation="The multiprocessing module allows CPU-bound parallel execution."
            ),
            QuizQuestion(
                chapter_number="9",
                question="What is GIL?",
                options=["Global Internal Lock", "Global Interpreter Lock", "General Instruction List", "Global Interface Layer"],
                answer=2,
                explanation="The Global Interpreter Lock limits CPU-bound threads to one core."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which keyword defines an async function?",
                options=["async", "async def", "await", "coroutine"],
                answer=2,
                explanation="The async def syntax defines an asynchronous function."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which keyword pauses in async functions?",
                options=["pause", "wait", "await", "suspend"],
                answer=3,
                explanation="The await keyword pauses execution until the awaited coroutine completes."
            ),
            QuizQuestion(
                chapter_number="9",
                question="What is threading used for?",
                options=["CPU-bound tasks", "I/O-bound tasks", "Data processing", "Matrix math"],
                answer=2,
                explanation="Threading is best for I/O-bound tasks that wait for external resources."
            ),
            QuizQuestion(
                chapter_number="9",
                question="What is multiprocessing used for?",
                options=["I/O-bound tasks", "CPU-bound tasks", "Network requests", "File operations"],
                answer=2,
                explanation="Multiprocessing uses multiple CPU cores for CPU-bound tasks."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which module provides asyncio support?",
                options=["async", "asyncio", "async_support", "coroutine"],
                answer=2,
                explanation="The asyncio module provides async/await support."
            ),
            QuizQuestion(
                chapter_number="9",
                question="What is the advantage of async/await?",
                options=["Multi-core CPU use", "Single-threaded concurrency", "Memory reduction", "Speed increase"],
                answer=2,
                explanation="Async/await enables concurrent I/O operations in a single thread."
            ),
            QuizQuestion(
                chapter_number="9",
                question="Which library provides both threading and multiprocessing?",
                options=["concurrent.futures", "asyncio", "threading", "multiprocessing"],
                answer=1,
                explanation="concurrent.futures provides a high-level interface for both threading and multiprocessing."
            )
        ]
        return questions
    
    def _generate_chapter_10_questions(self) -> List[QuizQuestion]:
        """Generate 11 questions for Chapter 10: Standard Library."""
        questions = [
            QuizQuestion(
                chapter_number="10",
                question="Which class counts element occurrences?",
                options=["Counter", "Count", "ElementCount", "Frequency"],
                answer=1,
                explanation="Counter from collections counts hashable objects."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which class creates tuples with named fields?",
                options=["NamedTuple", "Named", "FieldTuple", "Record"],
                answer=1,
                explanation="namedtuple from collections creates tuples with named fields."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which function chains multiple iterables?",
                options=["chain()", "combine()", "merge()", "join()"],
                answer=1,
                explanation="itertools.chain() concatenates multiple iterables."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which function groups consecutive elements?",
                options=["groupby()", "group()", "batch()", "section()"],
                answer=1,
                explanation="itertools.groupby() groups consecutive elements with the same key."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which module handles date and time?",
                options=["time", "datetime", "calendar", "date"],
                answer=2,
                explanation="The datetime module handles dates and times."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which module provides system parameters?",
                options=["sys", "system", "params", "env"],
                answer=1,
                explanation="The sys module provides access to system-specific parameters."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which module provides operating system interfaces?",
                options=["os", "system", "filesystem", "platform"],
                answer=1,
                explanation="The os module provides operating system interfaces."
            ),
            QuizQuestion(
                chapter_number="10",
                question="What does os.path.join() do?",
                options=["Joins file paths", "Joins strings", "Joins lists", "Joins directories"],
                answer=1,
                explanation="os.path.join() intelligently joins path components."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which function reads environment variables?",
                options=["os.getenv()", "os.environ[KEY]", "os.get_var()", "os.get_env()"],
                answer=2,
                explanation="os.getenv() or os.environ[KEY] reads environment variables."
            ),
            QuizQuestion(
                chapter_number="10",
                question="Which module provides random number generation?",
                options=["random", "rand", "randomize", "chance"],
                answer=1,
                explanation="The random module provides random number generation functions."
            ),
            QuizQuestion(
                chapter_number="10",
                question="What does itertools.accumulate() do?",
                options=["Accumulates values cumulatively", "Accumulates lists", "Accumulates dicts", "Accumulates counters"],
                answer=1,
                explanation="itertools.accumulate() returns accumulated sums or other binary functions."
            )
        ]
        return questions
    
    def _generate_generic_questions(self, chapter_number: str) -> List[QuizQuestion]:
        """Generate generic questions for unknown chapters."""
        return [
            QuizQuestion(
                chapter_number=chapter_number,
                question=f"Which topic does chapter {chapter_number} cover?",
                options=[
                    f"Python chapter {chapter_number} topics",
                    "General Python syntax",
                    "Data structures only",
                    "Object-oriented programming"
                ],
                answer=1,
                explanation=f"Chapter {chapter_number} covers advanced Python concepts."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What is Python?",
                options=[
                    "A high-level programming language",
                    "A database system",
                    "A web browser",
                    "An operating system"
                ],
                answer=1,
                explanation="Python is a versatile, high-level programming language."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="Which data type is immutable?",
                options=["list", "dict", "tuple", "set"],
                answer=3,
                explanation="Tuples are immutable data structures."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What symbol starts a comment?",
                options=["//", "#", "/*", "--"],
                answer=2,
                explanation="The # symbol starts single-line comments in Python."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="Which keyword imports modules?",
                options=["import", "include", "using", "require"],
                answer=1,
                explanation="The import keyword imports modules in Python."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What defines a function?",
                options=["def", "func", "define", "function"],
                answer=1,
                explanation="The def keyword defines functions in Python."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="Which loop iterates over sequences?",
                options=["for", "while", "repeat", "loop"],
                answer=1,
                explanation="The for loop iterates over sequences in Python."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What handles exceptions?",
                options=["try/except", "try/catch", "handle/error", "try/finally"],
                answer=1,
                explanation="try/except blocks handle exceptions in Python."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="Which module handles file I/O?",
                options=["built-in", "fileio", "filesystem", "io"],
                answer=1,
                explanation="File I/O is handled by built-in functions like open()."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What is a Python module?",
                options=[
                    "A file containing Python code",
                    "A compiled binary",
                    "A database connection",
                    "A network protocol"
                ],
                answer=1,
                explanation="Modules are files containing Python code that can be imported."
            ),
            QuizQuestion(
                chapter_number=chapter_number,
                question="What is the main Python installation directory?",
                options=["bin", "lib", "site-packages", "scripts"],
                answer=3,
                explanation="site-packages is where third-party packages are installed."
            )
        ]

    def _generate_fallback_questions(self, content: str,
                                      chapter_number: str) -> List[QuizQuestion]:
        """Generate 11 chapter-specific questions based on chapter number.
        
        Creates questions relevant to each chapter's topic.
        """
        questions = []
        chapter_num = int(chapter_number) if chapter_number.isdigit() else 1
        
        if chapter_num == 1:
            questions = self._generate_chapter_1_questions()
        elif chapter_num == 2:
            questions = self._generate_chapter_2_questions()
        elif chapter_num == 3:
            questions = self._generate_chapter_3_questions()
        elif chapter_num == 4:
            questions = self._generate_chapter_4_questions()
        elif chapter_num == 5:
            questions = self._generate_chapter_5_questions()
        elif chapter_num == 6:
            questions = self._generate_chapter_6_questions()
        elif chapter_num == 7:
            questions = self._generate_chapter_7_questions()
        elif chapter_num == 8:
            questions = self._generate_chapter_8_questions()
        elif chapter_num == 9:
            questions = self._generate_chapter_9_questions()
        elif chapter_num == 10:
            questions = self._generate_chapter_10_questions()
        else:
            questions = self._generate_generic_questions(chapter_number)
        
        return questions[:11]

    def generate_quiz_file(self, chapter_number: str, output_file: str,
                          chapter_dir: str = None) -> bool:
        """Generate quiz questions and save to JSON file.
        
        Args:
            chapter_number: The chapter number string (e.g., '1', '10')
            output_file: The output JSON file path
            chapter_dir: Optional directory name in content folder.
                        If not provided, defaults to 'ch{chapter_number}'
        """
        readme_path = os.path.join('content', f'ch{chapter_number}', 'README.md')
        if chapter_dir:
            readme_path = os.path.join('content', chapter_dir, 'README.md')

        questions = self.generate_quiz(readme_path, chapter_number)

        if questions:
            try:
                quiz_data = {
                    'chapter_number': chapter_number,
                    'title': f'Chapter {chapter_number} Quiz',
                    'passing_score': self.config.get('quizzes', {}).get('passing_score', 70),
                    'question_count': len(questions),
                    'questions': []
                }

                for q in questions:
                    quiz_data['questions'].append({
                        'question': q.question,
                        'options': q.options,
                        'answer': q.answer,
                        'explanation': q.explanation
                    })

                with open(output_file, 'w') as f:
                    json.dump(quiz_data, f, indent=2)

                print(f"Quiz generated: {output_file}")
                return True

            except Exception as e:
                print(f"Error saving quiz file: {e}")
                return False

        return False

    def generate_all_quizzes(self, output_dir: str = 'quizzes') -> int:
        """Generate quiz files for all chapters."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        count = 0
        chapters = [d for d in os.listdir('content') if d.startswith('ch') and os.path.isdir(os.path.join('content', d))]

        for chapter_dir in sorted(chapters):
            # Extract chapter number from directory name (e.g., ch1_intro -> 1)
            chapter_num = chapter_dir.split('_')[0].replace('ch', '') if chapter_dir.startswith('ch') else '00'
            # Add leading zero for single digits (e.g., 1 -> 01)
            if len(chapter_num) == 1:
                chapter_num = f'0{chapter_num}'
            readme_path = os.path.join('content', chapter_dir, 'README.md')

            if os.path.exists(readme_path):
                output_file = os.path.join(output_dir, f'quiz_ch{chapter_num}.json')
                if self.generate_quiz_file(chapter_num, output_file, chapter_dir):
                    count += 1
                else:
                    print(f"Failed to generate quiz for {chapter_dir}")

        print(f"\nGenerated {count}/{len(chapters)} quiz files")
        return count


def interactively_create_quizzes():
    """Interactive mode to create quizzes for specific chapters."""
    generator = QuizGenerator()

    print("\nQuiz Generator for Python Features Explorer")
    print("=" * 50)
    print("Type 'list' to see available chapters")
    print("Type 'quit' to exit\n")

    while True:
        try:
            choice = input("Select chapter number or type command> ").strip()

            if choice.lower() in ['quit', 'q', 'exit', 'exit']:
                print("Exiting quiz generator.")
                break

            if choice.lower() == 'list':
                print("\nAvailable chapters:")
                for d in sorted(os.listdir('content')):
                    if d.startswith('ch') and os.path.isdir(os.path.join('content', d)):
                        readme_path = os.path.join('content', d, 'README.md')
                        if os.path.exists(readme_path):
                            print(f"  {d}")
                continue

            # Generate quiz for specified chapter
            output_file = f'quizzes/quiz_ch{choice}.json'
            if generator.generate_quiz_file(choice, output_file):
                print(f"Successfully generated quiz for chapter {choice}")
            else:
                print(f"Failed to generate quiz for chapter {choice}")

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("\nPython Features Explorer - Quiz Generator")
    print("=" * 50)

    # Generate all quizzes
    generator = QuizGenerator()
    generated = generator.generate_all_quizzes()

    if generated > 0:
        print("\n" + "=" * 50)
        print("To interactively create more quizzes, run:")
        print("  python generate_quizzes.py --interactive")
        print("=" * 50)
    else:
        print("\nNo quizzes could be generated.")
