#!/usr/bin/env python3
"""Enhanced Quiz Question Generator with larger pools and randomized selection."""

import os
import json
import random
from pathlib import Path
from typing import List, Dict


class EnhancedQuizGenerator:
    """Generate enhanced quiz questions with larger pools and randomized selection."""

    def __init__(self):
        self.chapter_pools = self._create_question_pools()

    def _create_question_pools(self) -> Dict[int, List[Dict]]:
        return {
            1: self._generate_chapter_1_questions(),
            2: self._generate_chapter_2_questions(),
            3: self._generate_chapter_3_questions(),
            4: self._generate_chapter_4_questions(),
            5: self._generate_chapter_5_questions(),
            6: self._generate_chapter_6_questions(),
            7: self._generate_chapter_7_questions(),
            8: self._generate_chapter_8_questions(),
            9: self._generate_chapter_9_questions(),
            10: self._generate_chapter_10_questions(),
        }

    def _generate_chapter_1_questions(self) -> List[Dict]:
        """Generate questions for Chapter 1: Getting Started with Python."""
        return [
            {'question': 'What is the correct function to output text?', 'options': ['output()', 'print()', 'write()', 'echo()'], 'answer': 2, 'explanation': 'print() outputs text to console.', 'difficulty': 'easy'},
            {'question': 'What symbol is used for single-line comments?', 'options': ['//', '#', '/*', '--'], 'answer': 2, 'explanation': '# starts single-line comments.', 'difficulty': 'easy'},
            {'question': 'What is the correct file extension for Python files?', 'options': ['.py', '.python', '.pt', '.pc'], 'answer': 1, 'explanation': 'Python files use .py extension.', 'difficulty': 'easy'},
            {'question': 'Which keyword imports modules?', 'options': ['include', 'import', 'using', 'require'], 'answer': 2, 'explanation': 'import keyword imports modules.', 'difficulty': 'easy'},
            {'question': 'What data type represents decimal numbers?', 'options': ['int', 'float', 'str', 'bool'], 'answer': 2, 'explanation': 'float represents decimal numbers.', 'difficulty': 'easy'},
            {'question': 'Which keyword defines a function?', 'options': ['func', 'define', 'def', 'function'], 'answer': 3, 'explanation': 'def keyword defines functions.', 'difficulty': 'easy'},
            {'question': 'What does Python use to define code blocks?', 'options': ['Braces', 'Indentation', 'Semicolons', 'Keywords'], 'answer': 2, 'explanation': 'Python uses indentation for blocks.', 'difficulty': 'easy'},
            {'question': 'What is Python primarily known for?', 'options': ['Complex syntax', 'Readability', 'Speed', 'Hardware control'], 'answer': 2, 'explanation': 'Python is known for readability.', 'difficulty': 'easy'},
            {'question': 'Which built-in function returns the type of an object?', 'options': ['kind()', 'type()', 'category()', 'class()'], 'answer': 2, 'explanation': 'type() returns the data type.', 'difficulty': 'easy'},
            {'question': 'What is the result of 10 / 3 in Python 3?', 'options': ['3', '3.33', '3.0', '3.333...'], 'answer': 4, 'explanation': 'Python 3 division returns a float.', 'difficulty': 'easy'},
            {'question': 'Which statement creates a variable?', 'options': ['var x=5', 'int x=5', 'x=5', 'declare x=5'], 'answer': 3, 'explanation': 'Python uses simple assignment: x = 5.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_2_questions(self) -> List[Dict]:
        """Generate questions for Chapter 2: Data Structures."""
        return [
            {'question': 'Which is ordered and mutable?', 'options': ['list', 'tuple', 'set', 'dict'], 'answer': 1, 'explanation': 'Lists are ordered and mutable.', 'difficulty': 'easy'},
            {'question': 'Which is ordered but immutable?', 'options': ['list', 'tuple', 'set', 'dict'], 'answer': 2, 'explanation': 'Tuples are ordered and immutable.', 'difficulty': 'easy'},
            {'question': 'Syntax for dictionary?', 'options': ['[]', '()', '{}', '<>'], 'answer': 3, 'explanation': 'Curly braces create dictionaries.', 'difficulty': 'easy'},
            {'question': 'Access element by index?', 'options': ['list.key', 'list[index]', 'list.name', 'list(0)'], 'answer': 2, 'explanation': 'Use list[index] for index access.', 'difficulty': 'easy'},
            {'question': 'Add element to end of list?', 'options': ['push()', 'add()', 'append()', 'insert()'], 'answer': 3, 'explanation': 'append() adds to end.', 'difficulty': 'easy'},
            {'question': 'What does set() do with duplicates?', 'options': ['Keeps duplicates', 'Removes duplicates', 'Error', 'Counts them'], 'answer': 2, 'explanation': 'Sets remove duplicates.', 'difficulty': 'easy'},
            {'question': 'List comprehension syntax?', 'options': ['for x in list: x', '[x for x in list]', 'list(x for x)', '(x for x in list)'], 'answer': 2, 'explanation': 'List comprehensions use square brackets.', 'difficulty': 'easy'},
            {'question': 'Get number of elements?', 'options': ['list.size()', 'list.length', 'len(list)', 'size(list)'], 'answer': 3, 'explanation': 'len() returns element count.', 'difficulty': 'easy'},
            {'question': 'Which stores key-value pairs?', 'options': ['list', 'tuple', 'set', 'dict'], 'answer': 4, 'explanation': 'Dictionaries store key-value pairs.', 'difficulty': 'easy'},
            {'question': 'Difference between list and tuple?', 'options': ['Lists immutable', 'Tuples immutable', 'Lists only ints', 'Tuples unordered'], 'answer': 2, 'explanation': 'Tuples are immutable.', 'difficulty': 'easy'},
            {'question': 'Check if item in list?', 'options': ['in', 'contains', 'has', 'is'], 'answer': 1, 'explanation': 'in operator checks membership.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_3_questions(self) -> List[Dict]:
        """Generate questions for Chapter 3: Control Flow."""
        return [
            {'question': 'Which keyword starts conditional statement?', 'options': ['when', 'else', 'if', 'case'], 'answer': 3, 'explanation': 'if keyword begins conditionals.', 'difficulty': 'easy'},
            {'question': 'What keyword exits loop immediately?', 'options': ['break', 'continue', 'exit', 'stop'], 'answer': 1, 'explanation': 'break exits loop immediately.', 'difficulty': 'easy'},
            {'question': 'What keyword skips to next iteration?', 'options': ['break', 'continue', 'skip', 'next'], 'answer': 2, 'explanation': 'continue skips to next iteration.', 'difficulty': 'easy'},
            {'question': 'Which keyword is used for iteration loops?', 'options': ['while', 'for', 'repeat', 'loop'], 'answer': 2, 'explanation': 'for keyword iterates over sequences.', 'difficulty': 'easy'},
            {'question': 'What keyword starts loop based on condition?', 'options': ['while', 'for', 'if', 'until'], 'answer': 1, 'explanation': 'while loop repeats while condition is true.', 'difficulty': 'easy'},
            {'question': 'Which keyword handles alternative conditions?', 'options': ['else', 'otherwise', 'alt', 'switch'], 'answer': 1, 'explanation': 'else handles alternative conditions.', 'difficulty': 'easy'},
            {'question': 'What keyword handles additional conditions?', 'options': ['elif', 'else if', 'elseif', 'if else'], 'answer': 1, 'explanation': 'elif checks additional conditions.', 'difficulty': 'easy'},
            {'question': 'Which statement is placeholder that does nothing?', 'options': ['null', 'pass', 'skip', 'ignore'], 'answer': 2, 'explanation': 'pass is placeholder that does nothing.', 'difficulty': 'easy'},
            {'question': 'Can you use else with for loops?', 'options': ['No', 'Yes, when loop finishes', 'Yes, when loop breaks', 'Only with while'], 'answer': 2, 'explanation': 'else executes when loop finishes normally.', 'difficulty': 'easy'},
            {'question': 'What is indentation requirement?', 'options': ['Optional', '4 spaces minimum', 'Consistent required', 'Any spaces'], 'answer': 3, 'explanation': 'Python requires consistent indentation.', 'difficulty': 'easy'},
            {'question': 'How to write multi-way conditional?', 'options': ['if-else', 'if-elif-else', 'switch-case', 'multiple-if'], 'answer': 2, 'explanation': 'Use if-elif-else chains.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_4_questions(self) -> List[Dict]:
        """Generate questions for Chapter 4: Functions."""
        return [
            {'question': 'Which keyword defines a function?', 'options': ['func', 'define', 'def', 'function'], 'answer': 3, 'explanation': 'def keyword defines functions.', 'difficulty': 'easy'},
            {'question': 'What are *args used for?', 'options': ['Keyword args', 'Variable positional args', 'Default args', 'Named args'], 'answer': 2, 'explanation': '*args collects variable positional args.', 'difficulty': 'easy'},
            {'question': 'What are **kwargs used for?', 'options': ['Positional args', 'Variable keyword args', 'Required args', 'Default args'], 'answer': 2, 'explanation': '**kwargs collects variable keyword args.', 'difficulty': 'easy'},
            {'question': 'What keyword creates anonymous functions?', 'options': ['lambda', 'anonymous', 'fn', 'func'], 'answer': 1, 'explanation': 'lambda creates anonymous functions.', 'difficulty': 'easy'},
            {'question': 'Which function applies function to all items?', 'options': ['map()', 'apply()', 'do()', 'run()'], 'answer': 1, 'explanation': 'map() applies function to each item.', 'difficulty': 'easy'},
            {'question': 'Which function filters items based on condition?', 'options': ['filter()', 'select()', 'where()', 'extract()'], 'answer': 1, 'explanation': 'filter() filters items based on condition.', 'difficulty': 'easy'},
            {'question': 'What does LEGB rule refer to?', 'options': ['Loop structures', 'Variable scope', 'Function arguments', 'Module imports'], 'answer': 2, 'explanation': 'LEGB is variable scope: Local, Enclosing, Global, Built-in.', 'difficulty': 'easy'},
            {'question': 'Where are local variables defined?', 'options': ['Inside functions', 'Outside functions', 'In classes', 'In modules'], 'answer': 1, 'explanation': 'Local variables are inside functions.', 'difficulty': 'easy'},
            {'question': 'What is the purpose of a function?', 'options': ['To repeat code', 'To organize reusable code', 'To define variables', 'To import modules'], 'answer': 2, 'explanation': 'Functions organize reusable code blocks.', 'difficulty': 'easy'},
            {'question': 'How do you return a value from a function?', 'options': ['print()', 'return', 'export', 'yield'], 'answer': 2, 'explanation': 'return sends value back from function.', 'difficulty': 'easy'},
            {'question': 'What happens if a function has no return statement?', 'options': ['Error', 'Returns None', 'Returns 0', 'Returns False'], 'answer': 2, 'explanation': 'Functions without return return None.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_5_questions(self) -> List[Dict]:
        """Generate questions for Chapter 5: Object-Oriented Programming."""
        return [
            {'question': 'What keyword defines a class?', 'options': ['class', 'define', 'object', 'struct'], 'answer': 1, 'explanation': 'class keyword defines classes.', 'difficulty': 'easy'},
            {'question': 'What is the constructor method in Python classes?', 'options': ['__init__', '__construct__', '__start__', '__build__'], 'answer': 1, 'explanation': '__init__ is the constructor.', 'difficulty': 'easy'},
            {'question': 'What are methods ending with __ called?', 'options': ['Private methods', 'Dunder methods', 'Static methods', 'Class methods'], 'answer': 2, 'explanation': 'Methods with __ are dunder/magic methods.', 'difficulty': 'easy'},
            {'question': 'What does inheritance allow?', 'options': ['Multiple classes', 'Class reuse and extension', 'Function overloading', 'Variable types'], 'answer': 2, 'explanation': 'Inheritance allows reuse and extension.', 'difficulty': 'easy'},
            {'question': 'What is the first parameter of instance methods?', 'options': ['self', 'this', 'cls', 'object'], 'answer': 1, 'explanation': 'self refers to the instance.', 'difficulty': 'easy'},
            {'question': 'What is polymorphism?', 'options': ['Many constructors', 'Same method different classes', 'Hidden data', 'Class nesting'], 'answer': 2, 'explanation': 'Polymorphism: different classes same method.', 'difficulty': 'easy'},
            {'question': 'How do you create an instance of a class?', 'options': ['class()', 'new Class()', 'Class()', 'make Class()'], 'answer': 3, 'explanation': 'Call class like function: Class_Name().', 'difficulty': 'easy'},
            {'question': 'What does __str__ do?', 'options': ['Compare objects', 'Return string representation', 'Initialize', 'Destroy'], 'answer': 2, 'explanation': '__str__ returns human-readable string.', 'difficulty': 'easy'},
            {'question': 'What is encapsulation?', 'options': ['Multiple classes', 'Hide implementation details', 'Class inheritance', 'Method overloading'], 'answer': 2, 'explanation': 'Encapsulation hides internal details.', 'difficulty': 'easy'},
            {'question': 'How do you access an object attribute?', 'options': ['object(attribute)', 'object.attribute', 'object[attribute]', 'object->attribute'], 'answer': 2, 'explanation': 'Use dot notation: object.attribute.', 'difficulty': 'easy'},
            {'question': 'What is the base class for all Python classes?', 'options': ['Base', 'Root', 'object', 'Parent'], 'answer': 3, 'explanation': 'object is base class.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_6_questions(self) -> List[Dict]:
        """Generate questions for Chapter 6: Exception Handling."""
        return [
            {'question': 'Which block handles exceptions?', 'options': ['except', 'error', 'catch', 'handle'], 'answer': 1, 'explanation': 'except block handles exceptions.', 'difficulty': 'easy'},
            {'question': 'Which block always executes?', 'options': ['finally', 'always', 'end', 'done'], 'answer': 1, 'explanation': 'finally always executes.', 'difficulty': 'easy'},
            {'question': 'What happens when dividing by zero?', 'options': ['Returns 0', 'Returns None', 'Raises ZeroDivisionError', 'Returns infinity'], 'answer': 3, 'explanation': 'Division by zero raises ZeroDivisionError.', 'difficulty': 'easy'},
            {'question': 'How do you catch multiple exception types?', 'options': ['Multiple except', 'except (Exception1, Exception2)', 'catch {Exception1, Exception2}', 'one except for all'], 'answer': 2, 'explanation': 'Use except (Exception1, Exception2).', 'difficulty': 'easy'},
            {'question': 'What keyword raises an exception?', 'options': ['throw', 'raise', 'error', 'trigger'], 'answer': 2, 'explanation': 'raise keyword raises exceptions.', 'difficulty': 'easy'},
            {'question': 'What is the base exception class?', 'options': ['Error', 'Exception', 'BaseError', 'StandardError'], 'answer': 2, 'explanation': 'Exception is base class.', 'difficulty': 'easy'},
            {'question': 'Which block contains risky code?', 'options': ['try', 'risky', 'danger', 'risky'], 'answer': 1, 'explanation': 'try block contains risky code.', 'difficulty': 'easy'},
            {'question': 'How do you create a custom exception?', 'options': ['class CustomError(Exception)', 'def CustomError(Exception)', 'class Exception(CustomError)', 'def Exception(CustomError)'], 'answer': 1, 'explanation': 'class CustomError(Exception) creates custom exception.', 'difficulty': 'easy'},
            {'question': 'Can you have else with try-except?', 'options': ['No', 'Yes, if no exception', 'Only with finally', 'Yes, always'], 'answer': 2, 'explanation': 'else executes when no exception.', 'difficulty': 'easy'},
            {'question': 'What exception occurs with invalid type conversion?', 'options': ['TypeError', 'ValueError', 'SyntaxError', 'NameError'], 'answer': 2, 'explanation': 'ValueError for correct type, invalid value.', 'difficulty': 'easy'},
            {'question': 'What exception occurs with undefined variables?', 'options': ['UndefinedError', 'NameError', 'VariableError', 'ReferenceError'], 'answer': 2, 'explanation': 'NameError for undefined variables.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_7_questions(self) -> List[Dict]:
        """Generate questions for Chapter 7: File I/O."""
        return [
            {'question': 'Which keyword ensures proper resource cleanup?', 'options': ['try', 'finally', 'with', 'resource'], 'answer': 3, 'explanation': 'with keyword ensures proper cleanup.', 'difficulty': 'easy'},
            {'question': 'Which function opens files?', 'options': ['file()', 'open()', 'read()', 'fopen()'], 'answer': 2, 'explanation': 'open() opens files.', 'difficulty': 'easy'},
            {'question': 'What mode opens a file for writing?', 'options': ['r', 'w', 'a', 'x'], 'answer': 2, 'explanation': 'w mode opens for writing.', 'difficulty': 'easy'},
            {'question': 'What mode opens a file for reading?', 'options': ['r', 'w', 'a', 'x'], 'answer': 1, 'explanation': 'r mode opens for reading.', 'difficulty': 'easy'},
            {'question': 'How do you read the entire file content?', 'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.content()'], 'answer': 1, 'explanation': 'read() reads entire file as string.', 'difficulty': 'easy'},
            {'question': 'How do you read one line from a file?', 'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.line()'], 'answer': 2, 'explanation': 'readline() reads one line.', 'difficulty': 'easy'},
            {'question': 'How do you read all lines into a list?', 'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.lines()'], 'answer': 3, 'explanation': 'readlines() reads all lines into list.', 'difficulty': 'easy'},
            {'question': 'Which method writes to a file?', 'options': ['file.write()', 'file.print()', 'file.output()', 'file.send()'], 'answer': 1, 'explanation': 'write() writes to file.', 'difficulty': 'easy'},
            {'question': 'What happens when opening a non-existent file in w mode?', 'options': ['Error', 'Creates file', 'Returns None', 'Opens read-only'], 'answer': 2, 'explanation': 'w mode creates file if not exists.', 'difficulty': 'easy'},
            {'question': 'What is a context manager?', 'options': ['Manages resources with with statement', 'File handler', 'Exception handler', 'Variable manager'], 'answer': 1, 'explanation': 'Context manager manages resources with with.', 'difficulty': 'easy'},
            {'question': 'Which module provides contextmanager decorator?', 'options': ['contextlib', 'context', 'manager', 'withlib'], 'answer': 1, 'explanation': 'contextlib provides contextmanager.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_8_questions(self) -> List[Dict]:
        """Generate questions for Chapter 8: Advanced Python Features."""
        return [
            {'question': 'Which keyword creates a generator?', 'options': ['generate', 'yield', 'return', 'yield from'], 'answer': 2, 'explanation': 'yield keyword yields values.', 'difficulty': 'easy'},
            {'question': 'What is the main benefit of generators?', 'options': ['Memory efficiency', 'Speed', 'Parallel processing', 'Type safety'], 'answer': 1, 'explanation': 'Generators are memory efficient.', 'difficulty': 'easy'},
            {'question': 'Which decorator modifies a function?', 'options': ['decorator', '@decorator_name', 'decorate', '@wrap'], 'answer': 2, 'explanation': 'Use @decorator_name syntax.', 'difficulty': 'easy'},
            {'question': 'What is a decorator?', 'options': ['Function modifying function', 'Class method', 'Variable marker', 'Type hint'], 'answer': 1, 'explanation': 'Decorator modifies function behavior.', 'difficulty': 'easy'},
            {'question': 'What is the purpose of type hints?', 'options': ['Code documentation and IDE', 'Runtime checking', 'Faster execution', 'Memory management'], 'answer': 1, 'explanation': 'Type hints improve documentation and IDE support.', 'difficulty': 'easy'},
            {'question': 'Which operator is used for unpacking in function calls?', 'options': ['*', '**', 'spread', 'expand'], 'answer': 2, 'explanation': '** unpacks keyword arguments.', 'difficulty': 'easy'},
            {'question': 'What does * do for unpacking?', 'options': ['Unpack positional args', 'Unpack keyword args', 'Multiply', 'Splat'], 'answer': 1, 'explanation': '* unpacks positional arguments.', 'difficulty': 'easy'},
            {'question': 'Which keyword creates a lambda function?', 'options': ['lambda', 'anonymous', 'fn', 'func'], 'answer': 1, 'explanation': 'lambda creates anonymous functions.', 'difficulty': 'easy'},
            {'question': 'What is the syntax for type hinting a function?', 'options': ['def func(x: int) -> int:', 'def func(x int) int:', 'def func(x: int):', 'def func(int x): int'], 'answer': 1, 'explanation': 'Use def func(param: type) -> return_type.', 'difficulty': 'easy'},
            {'question': 'What is a generator function?', 'options': ['Function using yield', 'Function returning list', 'Function creating objects', 'Function generating random'], 'answer': 1, 'explanation': 'Generator function uses yield.', 'difficulty': 'easy'},
            {'question': 'How many times can a generator yield values?', 'options': ['Multiple times', 'Once', 'Twice', 'Never'], 'answer': 1, 'explanation': 'Generators can yield multiple values.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_9_questions(self) -> List[Dict]:
        """Generate questions for Chapter 9: Concurrency."""
        return [
            {'question': 'Which module provides threading support?', 'options': ['threading', 'threads', 'concurrent', 'asyncio'], 'answer': 1, 'explanation': 'threading module provides threads.', 'difficulty': 'easy'},
            {'question': 'Which method starts a thread?', 'options': ['thread.start()', 'thread.run()', 'start(thread)', 'thread.begin()'], 'answer': 1, 'explanation': 'start() begins thread execution.', 'difficulty': 'easy'},
            {'question': 'Which module provides multiprocessing support?', 'options': ['multiprocessing', 'processes', 'parallel', 'multiprocess'], 'answer': 1, 'explanation': 'multiprocessing module for CPU parallel.', 'difficulty': 'easy'},
            {'question': 'What is GIL?', 'options': ['Global Interpreter Lock', 'Global Internal Lock', 'General Instruction List', 'Global Interface Layer'], 'answer': 1, 'explanation': 'GIL is mutex for thread safety.', 'difficulty': 'easy'},
            {'question': 'Which keyword defines an async function?', 'options': ['async', 'async def', 'await', 'coroutine'], 'answer': 2, 'explanation': 'async def defines async function.', 'difficulty': 'easy'},
            {'question': 'Which keyword pauses in async functions?', 'options': ['pause', 'wait', 'await', 'suspend'], 'answer': 3, 'explanation': 'await pauses until coroutine completes.', 'difficulty': 'easy'},
            {'question': 'What is threading used for?', 'options': ['I/O-bound tasks', 'CPU-bound tasks', 'Data processing', 'Matrix math'], 'answer': 1, 'explanation': 'Threading is for I/O-bound tasks.', 'difficulty': 'easy'},
            {'question': 'What is multiprocessing used for?', 'options': ['CPU-bound tasks', 'I/O-bound tasks', 'Network requests', 'File operations'], 'answer': 1, 'explanation': 'Multiprocessing for CPU-bound tasks.', 'difficulty': 'easy'},
            {'question': 'Which module provides asyncio support?', 'options': ['async', 'asyncio', 'async_support', 'coroutine'], 'answer': 2, 'explanation': 'asyncio module provides async/await.', 'difficulty': 'easy'},
            {'question': 'What is the advantage of async/await?', 'options': ['Single-threaded concurrency', 'Multi-core use', 'Memory reduction', 'Speed increase'], 'answer': 1, 'explanation': 'Async/await enables single-threaded concurrency.', 'difficulty': 'easy'},
            {'question': 'What does asyncio.run() do?', 'options': ['Run asyncio program', 'Run coroutine', 'Run task', 'Start event loop'], 'answer': 1, 'explanation': 'asyncio.run runs asyncio main function.', 'difficulty': 'easy'},
        ]

    def _generate_chapter_10_questions(self) -> List[Dict]:
        """Generate questions for Chapter 10: Standard Library."""
        return [
            {'question': 'Which class counts element occurrences?', 'options': ['Counter', 'Count', 'ElementCount', 'Frequency'], 'answer': 1, 'explanation': 'Counter counts hashable objects.', 'difficulty': 'easy'},
            {'question': 'Which class creates tuples with named fields?', 'options': ['NamedTuple', 'Named', 'FieldTuple', 'Record'], 'answer': 1, 'explanation': 'namedtuple creates tuples with named fields.', 'difficulty': 'easy'},
            {'question': 'Which function chains multiple iterables?', 'options': ['chain()', 'combine()', 'merge()', 'join()'], 'answer': 1, 'explanation': 'itertools.chain() concatenates iterables.', 'difficulty': 'easy'},
            {'question': 'Which function groups consecutive elements?', 'options': ['groupby()', 'group()', 'batch()', 'section()'], 'answer': 1, 'explanation': 'itertools.groupby() groups consecutive elements.', 'difficulty': 'easy'},
            {'question': 'Which module handles date and time?', 'options': ['time', 'datetime', 'calendar', 'date'], 'answer': 2, 'explanation': 'datetime module handles dates and times.', 'difficulty': 'easy'},
            {'question': 'Which module provides system parameters?', 'options': ['sys', 'system', 'params', 'env'], 'answer': 1, 'explanation': 'sys module provides system parameters.', 'difficulty': 'easy'},
            {'question': 'Which module provides OS interfaces?', 'options': ['os', 'system', 'filesystem', 'platform'], 'answer': 1, 'explanation': 'os module provides OS interfaces.', 'difficulty': 'easy'},
            {'question': 'What does os.path.join() do?', 'options': ['Joins file paths', 'Joins strings', 'Joins lists', 'Joins directories'], 'answer': 1, 'explanation': 'os.path.join() intelligently joins paths.', 'difficulty': 'easy'},
            {'question': 'Which function reads environment variables?', 'options': ['os.getenv()', 'os.environ[KEY]', 'os.get_var()', 'os.get_env()'], 'answer': 2, 'explanation': 'os.getenv() or os.environ[KEY] reads env vars.', 'difficulty': 'easy'},
            {'question': 'Which module provides random number generation?', 'options': ['random', 'rand', 'randomize', 'chance'], 'answer': 1, 'explanation': 'random module provides random numbers.', 'difficulty': 'easy'},
            {'question': 'What does itertools.accumulate() do?', 'options': ['Accumulates values cumulatively', 'Accumulates lists', 'Accumulates dicts', 'Accumulates counters'], 'answer': 1, 'explanation': 'accumulate() returns accumulated sums or other binary functions.', 'difficulty': 'easy'},
        ]

    def generate_quiz(self, chapter_num: int, num_questions: int = 11) -> List[Dict]:
        """Randomly select questions from the chapter's pool."""
        if chapter_num not in self.chapter_pools:
            return []
        pool = self.chapter_pools[chapter_num]
        if num_questions > len(pool):
            num_questions = len(pool)
        return random.sample(pool, num_questions)

    def save_quiz(self, chapter_num: int, output_file: str) -> bool:
        """Generate and save quiz to JSON file."""
        questions = self.generate_quiz(chapter_num)
        if not questions:
            return False
        quiz_data = {
            'chapter_number': str(chapter_num).zfill(2),
            'title': f'Chapter {chapter_num} Quiz',
            'question_count': len(questions),
            'questions': []
        }
        for q in questions:
            quiz_data['questions'].append({
                'question': q['question'],
                'options': q['options'],
                'answer': q['answer'],
                'explanation': q['explanation'],
                'difficulty': q.get('difficulty', 'medium')
            })
        with open(output_file, 'w') as f:
            json.dump(quiz_data, f, indent=2)
        return True


if __name__ == "__main__":
    generator = EnhancedQuizGenerator()
    output_dir = Path('quizzes')
    output_dir.mkdir(exist_ok=True)
    for chapter_num in range(1, 11):
        output_file = output_dir / f'quiz_ch{str(chapter_num).zfill(2)}.json'
        if generator.save_quiz(chapter_num, str(output_file)):
            print(f"Generated quiz for chapter {chapter_num}")
        else:
            print(f"Failed for chapter {chapter_num}")
