# Application Documentation

## Overview

The **Python Features Explorer** is a CLI-based interactive application that provides a structured learning experience for Python programming. This documentation covers the application architecture, components, and usage.

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Python Features Explorer                 │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │   main.py    │    │    content   │    │  examples  │ │
│  │  (CLI App)   │◄──►│  (Markdown)  │◄──►│  (Python)  │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│          │                                       │      │
│          ▼                                       ▼      │
│  ┌──────────────┐                         ┌────────────┐ │
│  │  PythonExplorer│                         │  Examples  │ │
│  │  Class       │                         │  Runner    │ │
│  └──────────────┘                         └────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Core Class: PythonExplorer

The `PythonExplorer` class is the heart of the application, responsible for:

1. **Chapter Management**: Loading and organizing content by chapter
2. **Menu System**: Providing interactive navigation
3. **Example Execution**: Running Python scripts and displaying output

#### Methods

##### `__init__()`
Initializes the explorer by loading chapter data from the `content/` directory.

```python
def __init__(self):
    self.chapters = self._load_chapters()
```

##### `_load_chapters()` → `List[Dict[str, str]]`
Scans the content directory for chapter folders and loads their metadata.

```python
def _load_chapters(self) -> List[Dict[str, str]]:
    """Load chapter data from content files."""
    chapters = []
    
    for chapter_dir in os.listdir('content'):
        if chapter_dir.startswith('ch'):
            chapter_path = os.path.join('content', chapter_dir)
            if os.path.isdir(chapter_path):
                chapter_info = self._process_chapter(chapter_path)
                if chapter_info:
                    chapters.append(chapter_info)
    
    chapters.sort(key=lambda c: int(c['number']) if c['number'].isdigit() else 999)
    return chapters
```

##### `_process_chapter(chapter_path: str)` → `Dict[str, str]`
Processes a single chapter directory, extracting:
- Chapter number from the README title
- Chapter name
- Path to README file
- Available example scripts

```python
def _process_chapter(self, chapter_path: str) -> Dict[str, str]:
    """Process a single chapter directory."""
    try:
        chapter_content = []
        with open(os.path.join(chapter_path, 'README.md'), 'r') as f:
            chapter_content = f.readlines()
        
        chapter_name = chapter_path.split('/')[-1].replace('_', ' ').title()
        
        examples = []
        chapter_short_name = chapter_path.split('/')[-1]
        examples_path = os.path.join('examples', chapter_short_name)
        if os.path.exists(examples_path):
            for file in sorted(os.listdir(examples_path)):
                if file.endswith('.py'):
                    examples.append(file.replace('.py', ''))
        
        import re
        number_match = re.search(r'Chapter\s+(\d+)', chapter_content[0].strip())
        chapter_number = number_match.group(1) if number_match else '00'
        
        return {
            'number': chapter_number,
            'name': chapter_name,
            'readme_path': os.path.join(chapter_path, 'README.md'),
            'examples': examples
        }
    except Exception as e:
        print(f"Error processing {chapter_path}: {e}")
        return None
```

##### `display_menu()` → str
Shows the main navigation menu and returns user selection.

```python
def display_menu(self):
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("PYTHON FEATURES EXPLORER".center(60))
    print("=" * 60)
    
    for idx, chapter in enumerate(self.chapters, 1):
        print(f"{idx}. {chapter['name']}")
    
    print(f"\n{len(self.chapters) + 1}. Exit")
    return input("\nSelect a chapter (1-{})> ".format(len(self.chapters) + 1))
```

##### `display_chapter_details(chapter: Dict[str, str])` → str | None
Displays chapter content and available examples, returns user's example selection.

```python
def display_chapter_details(self, chapter: Dict[str, str]):
    """Display chapter content and examples."""
    print("\n" + "-" * 60)
    print(f"CHAPTER {chapter['number']}: {chapter['name'].upper()}")
    print("-" * 60)
    
    with open(chapter['readme_path'], 'r') as f:
        print(f.read())
    
    print("\n" + "Available Examples".center(60))
    print("-" * 60)
    
    if chapter['examples']:
        for idx, example in enumerate(chapter['examples'], 1):
            print(f"{idx}. {example}")
        
        print(f"\n{len(chapter['examples']) + 1}. Back to menu")
        return input("\nSelect an example to run (1-{})> ".format(len(chapter['examples']) + 1))
    else:
        print("\nNo examples available.")
        input("\nPress Enter to continue...")
        return None
```

##### `run_example(chapter_name: str, example_name: str)`
Executes a selected example Python script and displays its output.

```python
def run_example(self, chapter_name: str, example_name: str):
    """Run a Python example script."""
    example_path = os.path.join('examples', chapter_name.lower().replace(' ', '_'), f"{example_name}.py")
    
    if not os.path.exists(example_path):
        print(f"\nError: Example '{example_name}' not found at {example_path}")
        return
    
    print("\nRunning example: {}\n".format("-" * 40))
    
    try:
        result = subprocess.run(
            ['python3', example_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("\nExample completed with exit code: {}".format(result.returncode))
        
    except subprocess.TimeoutExpired:
        print("Error: Example execution timed out (30s)")
    except Exception as e:
        print("Error running example: {}".format(e))
    
    input("\nPress Enter to continue...")
```

## Data Flow

### Chapter Initialization

```
1. Application starts (main.py)
2. PythonExplorer instance created
3. _load_chapters() called
4. Loop through content/ directory
5. For each chapter:
   a. Read README.md
   b. Parse chapter number
   c. Scan examples/ directory
   d. Store chapter metadata
6. Sort chapters by number
7. Display main menu
```

### User Interaction Flow

```
User Action → Application Response

1. Enter number 1-10
   ↓
2. display_chapter_details() called
   ↓
3. Display README content
   ↓
4. Display available examples
   ↓
5. User selects example
   ↓
6. run_example() called
   ↓
7. Execute Python script
   ↓
8. Display output/errors
   ↓
9. Wait for user to continue
```

## Error Handling

The application includes robust error handling for:

1. **Invalid Input**: Catches non-numeric input and displays appropriate messages
2. **Missing Files**: Verifies example files exist before execution
3. **Execution Timeouts**: Limits example execution to 30 seconds
4. **Runtime Errors**: Captures and displays Python exceptions
5. **File Processing Errors**: Handles errors when reading chapter content

### Example Error Scenarios

```python
# Invalid input handling
try:
    choice = int(input("Select a chapter: "))
except ValueError:
    print("Invalid input! Please enter a number.")

# File execution timeout
try:
    result = subprocess.run(['python3', 'example.py'], timeout=30)
except subprocess.TimeoutExpired:
    print("Error: Example execution timed out")

# Missing example file
if not os.path.exists(example_path):
    print(f"Error: Example '{name}' not found")
```

## Exit Conditions

The application terminates when:

1. User selects option `{number_of_chapters + 1}` (Exit)
2. User types 'exit' in the menu
3. External interruption (Ctrl+C)

## Output Display

### Standard Output
All stdout from example scripts is captured and displayed with an "OUTPUT:" prefix.

### Standard Error
All stderr output is captured and displayed with a "STDERR:" prefix.

### Exit Codes
The application displays the exit code of each executed example for debugging purposes.

## Configuration

### Timeout Settings
- Default timeout: **30 seconds**
- Configured in `run_example()` method

### File Search Patterns
- Chapter directories start with `ch` and contain a `README.md` file
- Example files must end with `.py`
- Chapters are sorted numerically based on content in README title

## Performance Considerations

1. **File I/O**: Minimal file operations - only reads content at startup
2. **Subprocess**: Efficient spawning of Python interpreters
3. **Memory**: Lightweight - stores only metadata, not full content
4. **Scalability**: Can handle up to ~100 chapters without performance degradation

## Security Considerations

⚠️ **Important**: This application executes arbitrary Python scripts. Consider the following:

1. **Trusted Source**: Only run this application with trusted code
2. **Sandboxing**: Running untrusted scripts could be dangerous
3. **Timeout**: 30-second limit prevents hung processes

## Customization Options

### Modifying Display
- Change divider characters in `display_menu()` and `display_chapter_details()`
- Modify the welcome message in `main()`
- Adjust chapter numbering format

### Extending Functionality
- Add chapter search/filtering
- Implement chapter favorites
- Add example rating system
- Implement progress tracking

## API Reference

### PythonExplorer Class

| Method | Return Type | Description |
|--------|-------------|-------------|
| `__init__()` | None | Initialize explorer and load chapters |
| `_load_chapters()` | List[Dict] | Load chapter metadata from disk |
| `_process_chapter(str)` | Dict \| None | Process individual chapter |
| `display_menu()` | str | Show main menu, return selection |
| `display_chapter_details(Dict)` | str \| None | Show chapter, return selection |
| `run_example(str, str)` | None | Execute example script |

## Usage Examples

### Starting the Application

```bash
$ python3 main.py

============================================================
                  PYTHON FEATURES EXPLORER
============================================================
1. Ch_1_Introduction
2. Ch_2_Data_Structures
...
11. Exit

Select a chapter (1-11)> 1
```

### Running from Different Directory

```bash
cd /path/to/using_math
python3 main.py
```

### Running Specific Example

```bash
python3 examples/ch2_data_structures/lists.py
```

## Troubleshooting

### Common Issues

**Issue**: "Chapter not found"
- **Solution**: Ensure README.md exists in content/chXX_topic directory

**Issue**: "Example execution timed out"
- **Solution**: The example is running too long (>30s). Check for infinite loops.

**Issue**: "Example not found"
- **Solution**: The example file doesn't exist or is named incorrectly

**Issue**: "Invalid input"
- **Solution**: Enter a valid number from the displayed menu

**Issue**: Unicode characters display incorrectly
- **Solution**: Ensure your terminal supports UTF-8 encoding

## Best Practices

1. **Always verify examples** before running
2. **Keep examples focused** on single concepts
3. **Use appropriate timeouts** for long-running examples
4. **Provide clear output** in examples for learning
5. **Document changes** to chapter content

## Future Enhancements

Potential improvements:

- [ ] Add search functionality for chapters
- [ ] Implement progress tracking and saved state
- [ ] Add chapter quizzes
- [ ] Support dark mode terminal display
- [ ] Export examples to Jupyter notebooks
- [ ] Add video tutorials links
- [ ] Integrate with online Python IDEs
- [ ] Add code quality checks for examples

## License

This application is educational material. Use and modify as needed for learning purposes.

---

*Documentation generated for Python Features Explorer v1.0*
