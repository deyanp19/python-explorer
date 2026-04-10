# Quick Start Guide

Get up and running with Python Features Explorer in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Basic understanding of Python

## Installation Steps

### Step 1: Install Dependencies

```bash
cd /home/dido/projects/python/python_quick_robert_oliver/using_math
pip install colorama PyYAML
```

**Required packages:**
- `colorama>=0.4.6` - Terminal colors
- `PyYAML>=6.0` - Configuration parsing

*Note: If you get permission errors, use the system's package manager or create a virtual environment.*

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv explorer_env
source explorer_env/bin/activate  # On Windows: explorer_env\Scripts\activate
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

## Initial Setup

### Option A: Use Default Configuration (Quick Start)

The application comes with sensible defaults. Just run:

```bash
python main.py
```

### Option B: Customize Configuration

1. Copy the example configuration:
```bash
cp config.yaml.example config.yaml
```

2. Edit `config.yaml`:
```yaml
# Example: Change theme
theme:
  mode: "dark"

# Example: Adjust timeout
execution:
  timeout_seconds: 60

# Example: Enable progress tracking
progress:
  enabled: true
  storage_file: "user_progress.json"
```

## First Use

### Launch the Application

```bash
python main.py
```

You'll see:

```
============================================================
Welcome to the Python Features Explorer!
============================================================
Search chapters (press Enter to see all):
```

### Exploring Basic Commands

1. **View all chapters**:
   - Just press **Enter** at the search prompt

2. **Select a chapter**:
   - Type a number (e.g., `1` for Introduction)
   - Press Enter

3. **View chapter content**:
   - Read the displayed README content
   - See available examples

4. **Run an example**:
   - Select an example number
   - Watch the execution
   - Press Enter to continue

5. **Track your progress**:
   - Completed chapters show a ✓
   - Progress percentage at the top
   - View stats anytime with `stats`

### Useful Commands

| Command | Description |
|---------|-------------|
| `exit` | Exit the application |
| `help` | Show available commands |
| `stats` | Display your progress statistics |
| `fav` | Toggle favorite mode |
| `config` | Show current configuration |

### Searching for Chapters

When prompted:
```
Search chapters (press Enter to see all)> python
```

This will filter chapters containing "python" in their name, description, or examples.

## Common Tasks

### Mark a Chapter as Favorite

1. Press `fav` to enable favorite mode
2. Browse chapters
3. Favorites are automatically marked

### Check Your Progress

```bash
# At the main menu, type:
stats
```

Shows:
- Completed chapters
- Progress percentage
- Time spent
- Favorite chapters

### Configure the Application

Edit `config.yaml` for:
- Terminal color themes
- Execution timeout
- Search behavior
- Feature toggles

## Troubleshooting

### Colors Not Displaying

**Issue:** All text is plain text without colors.

**Solution:**
```bash
pip install colorama
```

### No Chapters Appear

**Issue:** Main menu shows no chapters.

**Solution:**
1. Check `content/` directory exists
2. Ensure README files are named correctly
3. Verify directory structure:
   ```
   content/
   ├── ch01/
   │   └── README.md
   ├── ch02/
   │   └── README.md
   ```

### Examples Not Running

**Issue:** Examples fail to execute.

**Solutions:**
- Check Python version (3.8+)
- Verify example files have correct permissions
- Review `python_explorer.log` for errors
- Check timeout value in config

### Progress Not Saving

**Issue:** Progress resets each session.

**Solutions:**
1. Check `config.yaml`:
   ```yaml
   progress:
     enabled: true
   ```
2. Ensure write permissions on storage directory
3. Check `user_progress.json` is not read-only

## Next Steps

### Learning Path

1. **Start with Introduction** (Chapter 1)
2. **Complete all examples** - Practice makes perfect
3. **Take quizzes** if enabled
4. **Track your progress** with stats
5. **Explore other chapters** based on your interests

### Customization

- **Change theme** in `config.yaml`
- **Adjust timeout** for longer examples
- **Enable search** for easy navigation
- **Add favorites** for quick access

## Getting Help

### Check Logs

Review `python_explorer.log` for detailed information about:
- Application startup
- Chapter loading details
- Execution errors
- Progress changes

### Configuration Reference

See `config.yaml` comments or `FEATURES.md` for detailed configuration options.

### Documentation

- `README.md` - Main documentation
- `FEATURES.md` - Detailed feature documentation
- `security.md` - Security considerations

## Support

### Common Questions

> **How do I reset my progress?**
Delete `user_progress.json` and restart the application.

> **Can I create my own chapters?**
Yes! Add new directories to `content/` with README.md files.

> **How do I backup my progress?**
Copy `user_progress.json` to a safe location.

### Community & Feedback

- Check existing documentation for answers
- Review logs for specific error details
- Consider the security implications when customizing

---

## Quick Command Reference

- `python main.py` - Start the application
- `python generate_quizzes.py` - Generate quiz files
- `python generate_chapters.py` - Generate chapter structure
- `pytest` - Run tests

---

**Happy Learning!** 🐍
