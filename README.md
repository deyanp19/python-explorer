# Python Features Explorer

<div align="center">

**A comprehensive interactive learning system for Python**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

[Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Configuration](#configuration)

</div>

**Python Features Explorer** is an interactive command-line application designed to help you learn Python through guided exploration. Navigate through comprehensive chapters, execute working examples, track your progress, and test your knowledge with quizzes.

---

## ✨ What's New in Version 2.0.0

🎯 **Major Updates**
- 🔍 **Smart Search** - Find chapters by keywords instantly
- 💾 **Progress Tracking** - Remember where you left off, even after closing
- 📊 **Statistics Dashboard** - Monitor your learning journey
- ⭐ **Favorites System** - Bookmark important chapters for quick access
- 🌚 **Theme Support** - Light/dark/automatic themes for comfortable viewing
- 📚 **Quiz System** - Test your understanding with interactive quizzes
- ⚙️ **Configurable Settings** - Custom behavior via `config.yaml`
- 📝 **Logging & Error Handling** - Better debugging and reliability

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install colorama PyYAML

# Run the application
python main.py
```

**Features you'll discover immediately:**
- Search for chapters by typing keywords
- View your progress and statistics
- Mark chapters as favorites
- Take quizzes after completing examples
- All your progress saved automatically

See the [Quick Start Guide](QUICK_START.md) for detailed setup instructions.

---

## 🎓 Learning Path

The application is organized into **10 comprehensive chapters** covering essential Python concepts:

| # | Topic | Progress |
|---|-------|----------|
| 1 | **Introduction to Python** | 📖 Basic concepts, setup, environment |
| 2 | **Data Types & Variables** | 📖 Variables, types, strings |
| 3 | **Control Flow** | ♾️ Conditions, loops, flow control |
| 4 | **Functions** | 📚 Function definitions, parameters, scope |
| 5 | **Modules & Packages** | 📦 Module system, packages, imports |
| 6 | **Error Handling** | ⚠️ Exceptions, try-except, debugging |
| 7 | **Working with Files** | 📁 File I/O, CSV, JSON handling |
| 8 | **Collections & Iterators** | 📊 Lists, dicts, sets, comprehensions |
| 9 | **Classes & OOP** | 🏗️ Object-oriented programming, inheritance |
| 10 | **Advanced Python** | ⚡ Decorators, generators, async |

Each chapter includes:
- Clear learning objectives
- Detailed explanations
- Working examples you can run
- Quiz questions (when enabled)
- Progress tracking

---

## 🔥 Key Features

### 🔍 Intelligent Search
Find specific content instantly:
```
Search chapters (press Enter to see all)> os
```
Searches chapter titles, descriptions, and examples.

### 💾 Smart Progress Tracking
- Automatically save your state between sessions
- Track which examples you've completed
- Remember quiz scores and ratings
- Total time spent tracking

### 🎨 Theme Support
Choose your preferred appearance:
- **Light mode** - Bright, clear text
- **Dark mode** - Easier on eyes for long sessions  
- **Auto-detect** - Matches your system theme

### 📊 Progress Dashboard
Type `stats` at the main menu to see:
- Total chapters completed
- Progress percentage
- Favorited chapters
- Examples rated
- Session time tracked

### ⭐ Favorites System
Mark important chapters for quick access:
1. Press `fav` to enable
2. Favorite chapters appear at the top of the menu
3. Quick access to challenging material

### 📚 Interactive Quizzes
Test your knowledge after completing chapters:
- Multiple choice questions
- Instant feedback with explanations
- Pass/fail determination (70% required)
- Retry attempts available

### ⚙️ Customizable Configuration
Adjust the application to your needs:
```yaml
# config.yaml examples
execution:
  timeout_seconds: 60

search:
  fuzzy_match: true

quizzes:
  enabled: true
  passing_score: 75
```

---

## 📚 Complete Chapter Outline

### Chapter 1: Introduction to Python 🚀
- What is Python?
- History and philosophy
- Installing Python
- Setting up your development environment
- Python shell basics
- First program: Hello World
- Understanding Python code
- Comments and documentation

### Chapter 2: Data Types & Variables 📦
- Variables and data types
- Primitive data types (int, float, str, bool)
- Type conversion
- String manipulation
- Number formatting
- Working with bytes
- Best practices

### Chapter 3: Control Flow ♾️
- Conditional statements (if, elif, else)
- Boolean operations
- Loops (for, while)
- Loop control (break, continue, pass)
- Pattern matching (match/case) - Python 3.10+
- Common patterns

### Chapter 4: Functions 📚
- Function definitions
- Parameters and return values
- Default arguments
- *args and **kwargs
- Lambda functions
- Anonymous functions
- Function scope
- Recursive functions

### Chapter 5: Modules & Packages 📦
- Import system
- Standard library modules
- Creating your own modules
- Package structure
- Installation and dependencies
- pip and virtual environments
- Module discovery
- Best practices

### Chapter 6: Error Handling ⚠️
- Exception handling
- Try-except blocks
- Custom exceptions
- Exception chaining
- Debugging techniques
- Logging vs exceptions
- Best practices
- Error recovery

### Chapter 7: Working with Files 📁
- Reading and writing files
- File operations
- Context managers
- Path manipulation (os, pathlib)
- CSV file handling
- JSON serialization
- Binary file I/O
- Working with large files

### Chapter 8: Collections & Iterators 📊
- Lists and list comprehensions
- Dictionaries and dict comprehensions
- Sets and set operations
- Tuples and namedtuples
- Iterators and generators
- itertools module
- collections module
- Common data structures

### Chapter 9: Classes & OOP 🏗️
- Object-oriented programming basics
- Classes and objects
- Class methods and static methods
- Inheritance and polymorphism
- Special methods (__init__, __str__, etc.)
- Encapsulation and properties
- Abstract base classes
- Design patterns

### Chapter 10: Advanced Python ⚡
- Decorators (function and class)
- Generators and coroutines
- Context managers (with statements)
- Asyncio and async/await
- Metaprogramming
- Type hints
- Data classes
- Performance optimization

---

## 🛠️ Installation & Setup

### Install Dependencies

**Option 1: Manual Installation**
```bash
pip install colorama PyYAML
```

**Option 2: Using requirements.txt**
```bash
pip install -r requirements.txt
```

**Option 3: Virtual Environment (Recommended)**
```bash
python -m venv explorer_env
source explorer_env/bin/activate  # On Windows: explorer_env\Scripts\activate.bat
pip install -r requirements.txt
```

### Configure the Application

1. **Use defaults** (recommended for beginners):
   ```bash
   python main.py
   ```

2. **Custom configuration**:
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml to your preferences
   python main.py
   ```

3. **Generate quizzes**:
   ```bash
   python generate_quizzes.py
   ```

---

## 📖 Command Reference

### Application Commands

| Command | Description |
|---------|-------------|
| `1-N` | Select a chapter |
| `exit`, `quit`, `q` | Exit the application |
| `help` | Show help message |
| `stats` | View statistics and progress |
| `fav` | Toggle favorites mode |
| `config` | Display current configuration |

### During Examples

| Command | Description |
|---------|-------------|
| `1-N` | Select an example to run |
| `y` | Try quiz (if enabled) |

---

## 🎯 Example Workflow

```
============================================================
Welcome to the Python Features Explorer!
============================================================
Search chapters (press Enter to see all): python
Search chapters (press Enter to see all)

===  Python Features Explorer - Chapters  ===

Progress: 0/10 chapters (0%)
Favorites: 0 of 10

  1. Introduction to Python (1/1 examples)  ☰  ✨
  2. Data Types & Variables (2/2 examples)  ☰
  3. Control Flow (5/5 examples)            ☰
  4. Functions (6/6 examples)               ☰
  5. Modules & Packages (4/4 examples)      ☰
  6. Error Handling (4/4 examples)          ☰
  7. Working with Files (5/5 examples)      ☰
  8. Collections & Iterators (7/7 examples) ☰
  9. Classes & OOP (5/5 examples)           ☰
  10. Advanced Python (6/6 examples)        ☰
  11. Exit Application

Search chapters (press Enter to see all)

```

**Try these commands:**
- `python` → Filter to show only Python-related chapters
- `1` → Enter Chapter 1: Introduction to Python
- `y` → Try quiz after completing examples
- `stats` → View your overall progress
- `fav` → Enable favorite mode

---

## 🔧 Configuration

Advanced customization through `config.yaml`:

```yaml
# Application settings
app:
  name: "Python Features Explorer"
  version: "2.0.0"
  debug: false

# Execution settings
execution:
  timeout_seconds: 30
  max_examples_per_session: 0
  shell: "python3"

# Display preferences
display:
  show_descriptions: true
  show_progress_bars: true
  content_width: 80
  wide_separators: false

# Search configuration
search:
  fuzzy_match: true
  min_characters: 2
  search_scope: "all"

# Progress tracking
progress:
  enabled: true
  storage_file: "user_progress.json"
  auto_save: true

# Theme settings
theme:
  mode: "auto"  # auto, dark, light
  colors:
    header: "cyan"
    chapter_title: "green"
    example: "blue"

# Quizzes
quizzes:
  enabled: true
  questions_per_chapter: 5
  passing_score: 70
  allow_retries: true

# Security
security:
  sandbox_mode: false
  allowed_directories: ["examples"]
  blocked_functions: ["os.system", "eval", "exec"]

# Logging
logging:
  level: "INFO"
  file: "python_explorer.log"
  max_size_mb: 10
```

See [FEATURES.md](FEATURES.md) for complete configuration options.

---

## 📝 Logging & Diagnostics

All activities are logged to `python_explorer.log`:
- Application startup and shutdown
- Chapter loading details
- Examples executed
- Progress changes
- Errors and warnings

View logs for troubleshooting:
```bash
tail -n 50 python_explorer.log
```

---

## 🎓 Learning Tips

1. **Complete all examples** - Practice is key to learning
2. **Take quizzes** - Reinforce concepts
3. **Track your progress** - Stay motivated with statistics
4. **Use favorites** - Bookmark important chapters
5. **Search effectively** - Find concepts quickly
6. **Review the logs** - Learn from issues and errors

---

## 📋 System Requirements

- **Python**: 3.8 or higher (3.10+ recommended for latest features)
- **Operating System**: Any OS with Python support (Windows, macOS, Linux)
- **Disk Space**: Minimal (< 5 MB)
- **Memory**: Standard requirements for Python execution

---

## 🔍 Search Examples

Searching works on:
- Chapter titles (e.g., "function", "loop")
- Descriptions (e.g., "introduction", "basic")
- Example names (e.g., "math", "json")

**Examples:**
```bash
Search chapters> os           # Find all OS-related content
Search chapters> data        # Find all data type content
Search chapters> class       # Find OOP content
Search chapters> loop        # Find control flow content
```

---

## 🛡️ Security Considerations

This application executes Python scripts, which carry inherent risks:

- **Examples run with your user privileges**
- **No sandboxing by default** - Scripts have file system access
- **Review code before execution** - Always read example content

For more details, see [security.md](security.md).

**For production use, we recommend:**
- Running in a containerized environment
- Enabling sandbox mode in config
- Reviewing all example code
- Using restricted access permissions

---

## 📚 Documentation

- **[README.md](README.md)** - Main documentation and project overview
- **[QUICK_START.md](QUICK_START.md)** - Step-by-step setup guide
- **[FEATURES.md](FEATURES.md)** - Detailed feature documentation
- **[security.md](security.md)** - Security considerations and best practices

---

## 🔄 Version History

### Version 2.0.0 (Current) - April 2024
**New:** Features mentioned above (search, progress tracking, themes, quizzes, etc.)

### Version 1.0
- Initial release
- Basic chapter navigation
- Example execution
- Manual progress tracking

---

## 🤝 Contributing

While this is an educational project, contributions are welcome!

**Suggested improvements:**
- Additional chapters or examples
- Better search algorithms
- Enhanced quiz functionality
- Improved user interface
- Additional themes

---

## 📧 Support & Feedback

- **Documentation**: See [FEATURES.md](FEATURES.md)
- **Logging**: Check `python_explorer.log` for issues
- **Configuration**: Review [FEATURES.md](FEATURES.md) for config options
- **Issues**: Please report problems through the project's issue tracker

---

## 🎉 Getting Started

1. **Install dependencies**: `pip install colorama PyYAML`
2. **Run application**: `python main.py`
3. **Explore chapters**: Browse the content
4. **Learn by doing**: Execute examples
5. **Test yourself**: Take quizzes

**Happy Learning!** 🐍

---

<div align="center">

Made with ❤️ for Python learners everywhere

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>
