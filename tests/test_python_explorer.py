"""Unit tests for Python Features Explorer.

Run with: pytest -v
"""

import unittest
import os
import sys
import json
import tempfile
import shutil
from unittest.mock import mock_open, patch, MagicMock
from datetime import datetime
from dataclasses import asdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import (
        PythonExplorer,
        Chapter,
        UserProgress,
        ConfigurationError,
        ExampleExecutionError,
        QuizGenerator,
        QuizQuestion,
        COLORAMA_AVAILABLE,
    )
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    print("Make sure main.py is executable and dependencies are installed")
    sys.exit(1)


class TestChapterDataclass(unittest.TestCase):
    """Test Chapter dataclass."""

    def test_chapter_creation(self):
        """Test creating a Chapter object."""
        chapter = Chapter(
            number='1',
            name='Introduction to Python',
            readme_path='/path/to/readme.md',
            examples=['example1', 'example2']
        )

        self.assertEqual(chapter.number, '1')
        self.assertEqual(chapter.name, 'Introduction to Python')
        self.assertEqual(len(chapter.examples), 2)

    def test_chapter_defaults(self):
        """Test Chapter default values."""
        chapter = Chapter(
            number='2',
            name='Basic Syntax',
            readme_path='/path/to/readme2.md'
        )

        self.assertEqual(chapter.examples, [])
        self.assertEqual(chapter.description, '')


class TestUserProgressDataclass(unittest.TestCase):
    """Test UserProgress dataclass."""

    def test_progress_creation(self):
        """Test creating UserProgress object."""
        progress = UserProgress(
            username='test_user',
            completed_chapters=['1'],
            viewed_examples={'1': ['example1']}
        )

        self.assertEqual(progress.username, 'test_user')
        self.assertEqual(len(progress.completed_chapters), 1)

    def test_progress_defaults(self):
        """Test UserProgress default values."""
        progress = UserProgress()

        self.assertEqual(progress.username, 'default')
        self.assertEqual(len(progress.completed_chapters), 0)
        self.assertEqual(progress.total_time_spent, 0)


class TestPythonExplorerInitialization(unittest.TestCase):
    """Test PythonExplorer initialization."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Create required directory structure
        os.makedirs('content/ch01')
        os.makedirs('examples/ch01')

        # Create sample README file
        readme_content = """# Chapter 1: Introduction to Python

This is a test chapter about Python basics.

## Learning Objectives
1. Understand Python syntax
2. Use variables
3. Basic data types
"""
        with open('content/ch01/README.md', 'w') as f:
            f.write(readme_content)

        # Create sample example file
        with open('examples/ch01/hello.py', 'w') as f:
            f.write('print("Hello, World!")\n')

        # Create default config
        with open('config.yaml', 'w') as f:
            f.write('# Test configuration\napp:\n  name: "Test"\n')

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_config_defaults(self):
        """Test application loads with default config."""
        explorer = PythonExplorer()

        self.assertEqual(explorer.config['app']['name'], 'Python Features Explorer')
        self.assertTrue(explorer.config['progress']['enabled'])

    def test_load_chapters(self):
        """Test loading chapters from directory."""
        explorer = PythonExplorer()

        # Should load at least one chapter
        self.assertGreater(len(explorer.chapters), 0)

        # Check chapter structure
        chapter = explorer.chapters[0]
        self.assertEqual(chapter.name, self._extract_chapter_name('ch01'))
        self.assertIn('ch01', chapter.number)

    def test_load_nonexistent_dir(self):
        """Test loading when content directory doesn't exist."""
        # Remove content directory
        shutil.rmtree('content', ignore_errors=True)

        explorer = PythonExplorer()

        self.assertEqual(len(explorer.chapters), 0)


class TestPythonExplorerMethods(unittest.TestCase):
    """Test PythonExplorer methods."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Create required directory structure
        os.makedirs('content/ch01')
        os.makedirs('content/ch02')
        os.makedirs('examples/ch01')
        os.makedirs('examples/ch02')

        # Create sample README files
        for chapter_num in ['01', '02']:
            readme_content = f"""# Chapter {chapter_num}: Test Chapter

This is chapter {chapter_num}, a test for testing purposes.
Contains basic Python information.
"""
            with open(f'content/ch{chapter_num}/README.md', 'w') as f:
                f.write(readme_content)

            with open(f'examples/ch{chapter_num}/test.py', 'w') as f:
                f.write(f'print("Chapter {chapter_num}")\n')

        # Create default config
        with open('config.yaml', 'w') as f:
            f.write('# Test configuration\napp:\n  name: "Test"\n')

        self.explorer = PythonExplorer()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_extract_chapter_number(self):
        """Test chapter number extraction."""
        content = "Chapter 1: Introduction to Python"
        number = self.explorer._extract_chapter_number(content.split('\n'))
        self.assertEqual(number, '1')

    def test_extract_description(self):
        """Test description extraction."""
        content = ["# Chapter 1", "", "This is a test description.",
                   "With multiple sentences in it."]
        desc = self.explorer._extract_description(content)
        self.assertIn('test description', desc.lower())

    def test_search_chapters(self):
        """Test chapter search functionality."""
        results = self.explorer._search_chapters('test')
        self.assertEqual(len(results), 2)

        results = self.explorer._search_chapters('python')
        self.assertEqual(len(results), 2)

    def test_search_no_results(self):
        """Test search with no matches."""
        results = self.explorer._search_chapters('xyz123nonexistent')
        self.assertEqual(len(results), 0)


class TestProgressTracking(unittest.TestCase):
    """Test progress tracking functionality."""

    def setUp(self):
        """Set up progress test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Create temporary progress file
        self.progress_file = 'test_progress.json'
        self.initial_data = {
            'username': 'test_user',
            'completed_chapters': [],
            'viewed_examples': {},
            'quiz_scores': {},
            'example_ratings': {},
            'favorites': [],
            'last_session': None,
            'total_time_spent': 0
        }

        with open(self.progress_file, 'w') as f:
            json.dump(self.initial_data, f)

        # Create minimal structure
        os.makedirs('content/ch01')
        with open('content/ch01/README.md', 'w') as f:
            f.write('# Chapter 1\n\nTest description.\n')

        os.makedirs('examples/ch01')
        with open('examples/ch01/test.py', 'w') as f:
            f.write('print("test")\n')

        # Create config file
        with open('config.yaml', 'w') as f:
            f.write('progress:\n  enabled: true\n  storage_file: test_progress.json\n')

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_progress(self):
        """Test loading progress from file."""
        explorer = PythonExplorer()

        self.assertEqual(explorer.user_progress.username, 'test_user')
        self.assertEqual(len(explorer.user_progress.completed_chapters), 0)

    def test_save_progress(self):
        """Test saving progress to file."""
        explorer = PythonExplorer()

        explorer.user_progress.completed_chapters.append('1')
        explorer.user_progress.last_session = datetime.now().isoformat()
        explorer._save_user_progress()

        # Reload and verify
        with open(self.progress_file, 'r') as f:
            saved_data = json.load(f)

        self.assertIn('1', saved_data['completed_chapters'])
        self.assertIsNotNone(saved_data['last_session'])

    def test_progress_persistence(self):
        """Test that progress persists across instances."""
        # First instance
        explorer1 = PythonExplorer()
        explorer1.user_progress.completed_chapters.append('1')
        explorer1._save_user_progress()

        # Second instance (new instance should reload saved data)
        explorer2 = PythonExplorer()
        self.assertIn('1', explorer2.user_progress.completed_chapters)


class TestExampleExecution(unittest.TestCase):
    """Test example execution functionality."""

    def setUp(self):
        """Set up execution test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Create minimal structure
        os.makedirs('content/ch01')
        with open('content/ch01/README.md', 'w') as f:
            f.write('# Chapter 1\n\nTest description.\n')

        os.makedirs('examples/ch01')

        # Create test example that will work
        with open('examples/ch01/simple.py', 'w') as f:
            f.write('print("Test execution")\n')

        # Create config file
        config_content = """
execution:
  timeout_seconds: 5
  shell: "python3"
progress:
  enabled: true
"""
        with open('config.yaml', 'w') as f:
            f.write(config_content)

        self.explorer = PythonExplorer()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('subprocess.run')
    def test_run_example_success(self, mock_run):
        """Test successful example execution."""
        mock_result = MagicMock()
        mock_result.stdout = "Test execution\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        self.explorer.run_example('ch01', 'simple', '1')

        self.assertIn('1', self.explorer.user_progress.viewed_examples)

    @patch('subprocess.run')
    def test_run_example_not_found(self, mock_run):
        """Test execution when example doesn't exist."""
        self.explorer.run_example('ch01', 'nonexistent', '1')

        # Progress should not be updated
        self.assertNotIn('1', self.explorer.user_progress.viewed_examples)


class TestQuizGenerator(unittest.TestCase):
    """Test quiz question generation."""

    def setUp(self):
        """Set up quiz generator test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Create quiz generator with minimal config
        with open('config.yaml', 'w') as f:
            f.write('quizzes:\n  questions_per_chapter: 3\n  passing_score: 70\n')

        self.generator = QuizGenerator()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_quiz_question_creation(self):
        """Test basic quiz question creation."""
        question = QuizQuestion(
            chapter_number='1',
            question='What is 2 + 2?',
            options=['3', '4', '5', '6'],
            answer=2,
            explanation='2 + 2 equals 4'
        )

        self.assertEqual(question.chapter_number, '1')
        self.assertEqual(len(question.options), 4)
        self.assertEqual(question.answer, 2)

    def test_generates_code_questions(self):
        """Test generating questions from code examples."""
        readme_content = """# Chapter 1

Here's a code example:

```python
import os
import sys
def main():
    print(os.getcwd())
```
"""

        with open('test_readme.md', 'w') as f:
            f.write(readme_content)

        questions = self.generator.generate_quiz(
            'test_readme.md',
            '1'
        )

        # Should generate at least one question
        self.assertGreater(len(questions), 0)

    def test_fallback_questions(self):
        """Test generating fallback questions when no specific content."""
        readme_content = """# Chapter 1

Just some random text without Python code or numbered lists.

No modules mentioned here.
"""

        with open('test_readme2.md', 'w') as f:
            f.write(readme_content)

        questions = self.generator.generate_quiz(
            'test_readme2.md',
            '1',
            num_questions=2
        )

        # Should generate fallback questions
        self.assertEqual(len(questions), 2)


class TestConfigurationLoading(unittest.TestCase):
    """Test configuration loading functionality."""

    def setUp(self):
        """Set up configuration test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_custom_config(self):
        """Test loading custom configuration."""
        with open('config.yaml', 'w') as f:
            f.write("""
execution:
  timeout_seconds: 60
  shell: "python"
display:
  content_width: 100
""")

        explorer = PythonExplorer()

        self.assertEqual(explorer.config['execution']['timeout_seconds'], 60)
        self.assertEqual(explorer.config['display']['content_width'], 100)

    def test_missing_config_uses_defaults(self):
        """Test using default config when file missing."""
        explorer = PythonExplorer()

        # Should use default timeout
        self.assertEqual(explorer.config['execution']['timeout_seconds'], 30)

    def test_merge_config(self):
        """Test deep merging configurations."""
        base = {
            'app': {
                'name': 'Default App',
                'version': '1.0'
            },
            'execution': {
                'timeout_seconds': 30
            }
        }

        override = {
            'app': {
                'version': '2.0'
            },
            'execution': {
                'shell': 'python3'
            }
        }

        result = PythonExplorer._deep_merge(base, override)

        # base values should be preserved
        self.assertEqual(result['app']['name'], 'Default App')
        # override values should be applied
        self.assertEqual(result['app']['version'], '2.0')
        self.assertEqual(result['execution']['shell'], 'python3')


class TestColoramaSupport(unittest.TestCase):
    """Test colorama integration."""

    def test_colorama_availability(self):
        """Test if colorama is available."""
        # This will be True if installed, False otherwise
        self.assertIn(COLORAMA_AVAILABLE, [True, False])

    def test_formatting_without_colorama(self):
        """Test formatting when colorama is not available."""
        with patch('main.COLORAMA_AVAILABLE', False):
            # Reload functions that depend on colorama
            from main import PythonExplorer
            explorer = PythonExplorer()

            text = explorer._get_formatted_text("Test", "green")
            self.assertEqual(text, "Test")


if __name__ == '__main__':
    print("Running Python Features Explorer tests...")
    print("=" * 50)

    # Run tests
    unittest.main(verbosity=2)

    print("\nTests completed!")
