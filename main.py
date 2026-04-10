#!/usr/bin/env python3
"""Python Features Explorer - Interactive CLI application with enhanced features.

This application provides a structured learning experience for Python programming
with search, progress tracking, quizzes, and a user-friendly interface.
"""

import subprocess
import os
import sys
import json
import re
import shutil
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import yaml
import logging

# Import colorama for cross-platform terminal colors
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    Fore = Back = Style = None


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='python_explorer.log'
)
logger = logging.getLogger(__name__)

# QuizQuestion dataclass for quiz functionality
@dataclass
class QuizQuestion:
    """Represents a quiz question."""
    chapter_number: str
    question: str
    options: List[str]
    answer: int  # 1-indexed
    explanation: str


@dataclass
class Chapter:
    """Dataclass representing a learning chapter."""
    number: str
    name: str
    readme_path: str
    examples: List[str] = field(default_factory=list)
    description: str = ""
    quiz_questions: List[Dict] = field(default_factory=list)


@dataclass
class UserProgress:
    """Dataclass representing user progress."""
    username: str = "default"
    completed_chapters: List[str] = field(default_factory=list)
    viewed_examples: Dict[str, List[str]] = field(default_factory=dict)
    quiz_scores: Dict[str, float] = field(default_factory=dict)
    example_ratings: Dict[str, float] = field(default_factory=dict)
    favorites: List[str] = field(default_factory=list)
    last_session: Optional[str] = None
    total_time_spent: int = 0  # in minutes


class ConfigurationError(Exception):
    """Exception raised when there's a configuration issue."""
    pass


class ExampleExecutionError(Exception):
    """Exception raised when example execution fails."""
    pass


class ChapterNotFoundError(Exception):
    """Exception raised when a chapter is not found."""
    pass


class PythonExplorer:
    """Main application class for exploring Python features."""

    DEFAULT_CONFIG = {
        'app': {'name': 'Python Features Explorer', 'version': '2.0.0'},
        'theme': {'mode': 'auto', 'colors': {}},
        'execution': {'timeout_seconds': 30},
        'progress': {'enabled': True, 'storage_file': 'user_progress.json'},
        'search': {'fuzzy_match': True, 'min_characters': 2},
        'quizzes': {'enabled': False, 'questions_per_quiz': 5},
        'favorites': {'enabled': False, 'max_favorites': 10},
        'display': {'show_descriptions': True, 'content_width': 80},
    }

    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize the explorer with configuration."""
        self.chapters: List[Chapter] = []
        self.config = self.DEFAULT_CONFIG.copy()
        self.user_progress = UserProgress()
        self._load_config(config_path)
        self.chapters = self._load_chapters()
        self._load_user_progress()

    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        self.config = self._deep_merge(self.DEFAULT_CONFIG, yaml_config)
                        logger.info(f"Configuration loaded from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                print(f"Warning: Could not load config file ({config_path}), using defaults")
        else:
            logger.info(f"Config file {config_path} not found, using defaults")

    @staticmethod
    def _deep_merge(base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = PythonExplorer._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def _load_chapters(self) -> List[Chapter]:
        """Load chapter data from content directories."""
        chapters = []

        try:
            content_dir = 'content'
            if not os.path.exists(content_dir):
                print(f"Error: Content directory '{content_dir}' not found")
                logger.error(f"Content directory not found: {content_dir}")
                return chapters

            for chapter_dir in sorted(os.listdir(content_dir)):
                if chapter_dir.startswith('ch') and os.path.isdir(
                    os.path.join(content_dir, chapter_dir)
                ):
                    chapter_info = self._process_chapter(content_dir, chapter_dir)
                    if chapter_info:
                        chapters.append(chapter_info)

            chapters.sort(key=lambda c: int(c.number) if c.number.isdigit() else 999)
            logger.info(f"Loaded {len(chapters)} chapters")

        except Exception as e:
            logger.error(f"Error loading chapters: {e}")
            print(f"Error loading chapters: {e}")

        return chapters

    def _process_chapter(self, content_dir: str, chapter_dir: str) -> Optional[Chapter]:
        """Process a single chapter directory."""
        try:
            chapter_path = os.path.join(content_dir, chapter_dir)
            readme_path = os.path.join(chapter_path, 'README.md')

            if not os.path.exists(readme_path):
                logger.warning(f"README.md not found in {chapter_path}")
                return None

            with open(readme_path, 'r', encoding='utf-8') as f:
                chapter_content = f.readlines()

            # Extract chapter description
            description = self._extract_description(chapter_content)

            # Get chapter name
            chapter_name = chapter_dir.replace('_', ' ').title()

            # Get examples
            examples = []
            examples_path = os.path.join('examples', chapter_dir)
            if os.path.exists(examples_path):
                for file in sorted(os.listdir(examples_path)):
                    if file.endswith('.py'):
                        examples.append(file.replace('.py', ''))

            # Extract chapter number
            number = self._extract_chapter_number(chapter_content)

            return Chapter(
                number=number,
                name=chapter_name,
                readme_path=readme_path,
                examples=examples,
                description=description
            )

        except Exception as e:
            logger.error(f"Error processing {chapter_dir}: {e}")
            print(f"Error processing {chapter_dir}: {e}")
            return None

    def _extract_chapter_number(self, chapter_content: List[str]) -> str:
        """Extract chapter number from content."""
        if not chapter_content:
            return '00'

        match = re.search(r'Chapter\s+(\d+)', chapter_content[0].strip())
        return match.group(1) if match else '00'

    def _extract_description(self, chapter_content: List[str]) -> str:
        """Extract chapter description from README."""
        if len(chapter_content) < 10:
            return ' '.join(chapter_content[:5])

        # Look for first paragraph after title
        in_body = False
        description_lines = []

        for line in chapter_content[1:10]:
            line = line.strip()
            if line.startswith('#'):
                if in_body:
                    break
                continue

            if line and not line.startswith('-') and not line.startswith('*'):
                description_lines.append(line)
                in_body = True

            if len(description_lines) >= 2:
                break

        return ' '.join(description_lines) if description_lines else ''

    def _load_user_progress(self) -> None:
        """Load user progress from file."""
        if not self.config.get('progress', {}).get('enabled', True):
            return

        storage_file = self.config['progress'].get('storage_file', 'user_progress.json')

        if os.path.exists(storage_file):
            try:
                with open(storage_file, 'r') as f:
                    data = json.load(f)
                    self.user_progress = UserProgress(**data)
                    logger.info(f"Loaded progress for user: {self.user_progress.username}")
            except Exception as e:
                logger.warning(f"Failed to load progress: {e}")
                print(f"Warning: Could not load previous progress")
        else:
            logger.info("No progress file found, starting fresh")

    def _save_user_progress(self) -> None:
        """Save user progress to file."""
        if not self.config.get('progress', {}).get('enabled', True):
            return

        storage_file = self.config['progress'].get('storage_file', 'user_progress.json')

        try:
            data = {
                'username': self.user_progress.username,
                'completed_chapters': self.user_progress.completed_chapters,
                'viewed_examples': self.user_progress.viewed_examples,
                'quiz_scores': self.user_progress.quiz_scores,
                'example_ratings': self.user_progress.example_ratings,
                'favorites': self.user_progress.favorites,
                'last_session': self.user_progress.last_session,
                'total_time_spent': self.user_progress.total_time_spent
            }

            with open(storage_file, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Saved progress to {storage_file}")

        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
            print(f"Error saving progress: {e}")

    def display_menu(self) -> str:
        """Display the main menu with search, favorites, and progress."""
        print("\n" + self._get_formatted_header("PYTHON FEATURES EXPLORER"))
        print("=" * 60)

        # Show progress
        if self.chapters:
            completed = len(self.user_progress.completed_chapters)
            total = len(self.chapters)
            progress_pct = int((completed / total) * 100) if total > 0 else 0
            print(f"Progress: {completed}/{total} chapters ({progress_pct}%)")

        # Search bar
        search_results = None
        while True:
            search_input = self._get_input("Search chapters (press Enter to see all)> ").strip().lower()

            if search_input:
                search_results = self._search_chapters(search_input)
                print(f"\nFound {len(search_results)} matching chapter(s):")
                for chapter in search_results:
                    print(f"  {chapter.number}. {chapter.name} - {chapter.description[:50]}")
                print()
            else:
                search_results = self.chapters
                break

            if not self._get_input("Continue searching? (y/n) ").lower().startswith('y'):
                search_results = self.chapters
                break

        # Favorites section
        if self.user_progress.favorites:
            print("\n" + self._get_formatted_text("⭐ FAVORITES", "yellow"))
            for fav_id in self.user_progress.favorites[:5]:
                try:
                    chapter = next(ch for ch in self.chapters if ch.number == fav_id)
                    print(f"  ⭐ {chapter.number}. {chapter.name}")
                except StopIteration:
                    pass

        # Main menu
        print("\n" + "-" * 60)
        print("AVAILABLE CHAPTERS")
        print("-" * 60)

        for idx, chapter in enumerate(self.chapters, 1):
            status = ""
            if chapter.number in self.user_progress.completed_chapters:
                status = " ✓"
            elif chapter.number in self.user_progress.favorites:
                status = " ⭐"

            display_name = f"{idx}. {chapter.name}"
            print(f"  {self._get_formatted_color(display_name + status, 'green')}")

            if self.config.get('display', {}).get('show_descriptions', True) and chapter.description:
                print(f"    {self._get_formatted_color(chapter.description[:70], 'dim')}")

        print(f"\n{len(self.chapters) + 1}. Exit")
        return self._get_input(f"\nSelect a chapter (1-{len(self.chapters) + 1})> ")

    def _search_chapters(self, query: str) -> List[Chapter]:
        """Search chapters by name, description, or examples."""
        search_scope = self.config['search'].get('search_scope', 'all')
        min_chars = self.config['search'].get('min_characters', 2)

        if len(query) < min_chars:
            return []

        results = []
        for chapter in self.chapters:
            match = False

            if search_scope in ['all', 'titles'] and query in chapter.name.lower():
                match = True

            if search_scope in ['all', 'descriptions'] and query in chapter.description.lower():
                match = True

            if search_scope in ['all', 'examples']:
                for example in chapter.examples:
                    if query in example.lower():
                        match = True
                        break

            if match:
                results.append(chapter)

        return results

    def display_chapter_details(self, chapter: Chapter, rendered_content: str = None):
        """Display chapter content and examples with progress tracking."""
        print("\n" + self._get_formatted_text(f"CHAPTER {chapter.number}: {chapter.name.upper()}", "cyan"))
        print("=" * 60)

        # Show cached or fresh content
        if not rendered_content:
            try:
                with open(chapter.readme_path, 'r', encoding='utf-8') as f:
                    rendered_content = f.read()
                # Cache the rendered content for this session
                if not hasattr(self, '_chapter_cache'):
                    self._chapter_cache = {}
                self._chapter_cache[chapter.number] = rendered_content
            except Exception as e:
                print(f"Error reading chapter content: {e}")
                rendered_content = ""

        display_width = self.config.get('display', {}).get('content_width', 80)
        self._print_formatted_text(rendered_content, display_width)

        print("\n" + self._get_formatted_text("Available Examples", "blue"))
        print("-" * 60)

        if chapter.examples:
            for idx, example in enumerate(chapter.examples, 1):
                viewed = "✓" if example in self.user_progress.viewed_examples.get(chapter.number, []) else " "
                print(f"  {viewed} {idx}. {example}")

            print(f"\n{len(chapter.examples) + 1}. Back to menu")

            if self.user_progress.favorites and chapter.number in self.user_progress.favorites:
                print("  ⭐ Already marked as favorite")

        else:
            print("\nNo examples available.")
            input("\nPress Enter to continue...")
            return None

        return self._get_input("\nSelect an example to run (1-{})> ".format(len(chapter.examples) + 1))

    def run_example(self, chapter_name: str, example_name: str, chapter_number: str) -> None:
        """Run a Python example script with error handling and timeout."""
        example_path = os.path.join('examples', chapter_name.lower().replace(' ', '_'), f"{example_name}.py")

        if not os.path.exists(example_path):
            print(f"\n{self._get_formatted_text('Error', 'red')}: Example '{example_name}' not found at {example_path}")
            logger.error(f"Example not found: {example_path}")
            input("\nPress Enter to continue...")
            return

        print("\n" + self._get_formatted_text(f"Running example: {example_name}", "yellow"))
        print("=" * 40)

        timeout = self.config.get('execution', {}).get('timeout_seconds', 30)

        try:
            start_time = datetime.now()

            result = subprocess.run(
                ['python3', example_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            if result.stdout:
                print(self._get_formatted_text("OUTPUT:", "green"))
                print(result.stdout)

            if result.stderr:
                print(self._get_formatted_text("STDERR:", "red"))
                print(result.stderr)

            print(f"\nExample completed in {duration:.2f}s with exit code: {result.returncode}")

        except subprocess.TimeoutExpired as e:
            print(f"{self._get_formatted_text('Error', 'red')}: Example execution timed out ({timeout}s)")
            logger.warning(f"Example {example_name} timed out after {timeout}s")
            input("\nPress Enter to continue...")

        except Exception as e:
            print(f"{self._get_formatted_text('Error running example:', 'red')} {e}")
            logger.error(f"Error running example {example_name}: {e}")
            input("\nPress Enter to continue...")
            return

        # Update progress
        self._update_progress(chapter_number, example_name)

        input("\nPress Enter to continue...")

    def _update_progress(self, chapter_number: str, example_name: str) -> None:
        """Update user progress for viewed example."""
        if chapter_number not in self.user_progress.viewed_examples:
            self.user_progress.viewed_examples[chapter_number] = []

        if example_name not in self.user_progress.viewed_examples[chapter_number]:
            self.user_progress.viewed_examples[chapter_number].append(example_name)
            logger.info(f"Viewed example {example_name} in chapter {chapter_number}")

    def complete_chapter(self, chapter_number: str) -> None:
        """Mark chapter as completed."""
        if chapter_number not in self.user_progress.completed_chapters:
            self.user_progress.completed_chapters.append(chapter_number)
            self.user_progress.last_session = datetime.now().isoformat()
            logger.info(f"Completed chapter {chapter_number}")
            print(f"{self._get_formatted_text('✓', 'green')} Chapter {chapter_number} marked as completed!")

    def toggle_favorite(self, chapter_number: str) -> bool:
        """Toggle favorite status for a chapter."""
        if chapter_number in self.user_progress.favorites:
            self.user_progress.favorites.remove(chapter_number)
            print(f"Removed {chapter_number} from favorites")
            return False
        else:
            if len(self.user_progress.favorites) >= self.config.get('favorites', {}).get('max_favorites', 10):
                print("Maximum favorites reached!")
                return False
            self.user_progress.favorites.append(chapter_number)
            print(f"Added {chapter_number} to favorites")
            return True

    def rate_example(self, chapter_number: str, example_name: str, rating: int) -> None:
        """Rate an example (1-5)."""
        if 1 <= rating <= 5:
            key = f"{chapter_number}:{example_name}"
            self.user_progress.example_ratings[key] = rating
            logger.info(f"Rated example {example_name} as {rating} stars")
            print(f"{self._get_formatted_text('✓', 'green')} Example rated {rating}/5 stars")
        else:
            print("Rating must be between 1 and 5")

    def display_quiz(self, chapter: Chapter) -> bool:
        """Display quiz for a chapter (if available)."""
        quiz_config = self.config.get('quizzes', {})
        if not quiz_config.get('enabled', False):
            print("\nQuizzes are not enabled. Enable in config.yaml to use.")
            return True

        questions = getattr(chapter, 'quiz_questions', [])
        if not questions:
            print(f"\nNo quiz questions available for {chapter.name}")
            return True

        print(f"\n{self._get_formatted_text('QUIZ: ' + chapter.name, 'yellow')}")
        print("=" * 40)

        score = 0
        total = min(len(questions), quiz_config.get('questions_per_quiz', 5))

        for i, question in enumerate(questions[:total], 1):
            print(f"\n{i}. {question['question']}")
            for j, option in enumerate(question['options'], 1):
                print(f"   {j}. {option}")

            try:
                answer = int(self._get_input(f"Enter your answer ({1}-{len(question['options'])})> "))
                if answer == question['answer']:
                    score += 1
                    print(f"{self._get_formatted_text('✓ Correct!', 'green')}")
                else:
                    print(f"{self._get_formatted_text('✗ Incorrect!', 'red')}")
                    print(f"Correct answer: {question['options'][question['answer'] - 1]}")
            except ValueError:
                print("Invalid number, marking as incorrect")

        percentage = (score / total) * 100
        passing = quiz_config.get('passing_score', 70)

        print(f"\n{self._get_formatted_text(f'Quiz Results: {score}/{total} ({percentage:.1f}%)', 'cyan')}")

        if percentage >= passing:
            print(f"{self._get_formatted_text('✓ Passed! Marking chapter as completed.', 'green')}")
            self.complete_chapter(chapter.number)
            self.user_progress.quiz_scores[chapter.number] = percentage
            return True
        else:
            print(f"{self._get_formatted_text(f'✗ Failed (need {passing}% to pass)', 'red')}")
            print("Complete the examples first, then try again!")
            return False

    def show_statistics(self) -> None:
        """Display user statistics."""
        print("\n" + self._get_formatted_text("USER STATISTICS", "green"))
        print("=" * 60)

        completed = len(self.user_progress.completed_chapters)
        total = len(self.chapters)
        progress_pct = int((completed / total) * 100) if total > 0 else 0

        stats = [
            (f"Total Chapters", f"{total}"),
            (f"Completed Chapters", f"{completed} ({progress_pct}%)" if total > 0 else "0 (0%)"),
            (f"Favorited Chapters", f"{len(self.user_progress.favorites)}"),
            (f"Examples Rated", f"{len(self.user_progress.example_ratings)}"),
            (f"Last Session", f"{self.user_progress.last_session or 'Never'}"),
            (f"Total Time Spent", f"{self.user_progress.total_time_spent} min"),
        ]

        for label, value in stats:
            print(f"{label:25} {value}")

        print("\n" + "-" * 60)
        print("CHAPTER PROGRESS:")
        print("-" * 60)

        for chapter in self.chapters:
            status = "✓" if chapter.number in self.user_progress.completed_chapters else " "
            viewed = len(self.user_progress.viewed_examples.get(chapter.number, []))
            examples = len(chapter.examples)
            viewed_pct = int((viewed / examples) * 100) if examples > 0 else 0

            status_line = f"  {status} Chap {chapter.number:2}: {chapter.name[:30]:<30} {viewed}/{examples} examples ({viewed_pct}%)"
            if viewed == examples and chapter.number not in self.user_progress.completed_chapters:
                print(f"  {self._get_formatted_color(status_line, 'green')}")
            else:
                print(status_line)

    def _get_formatted_header(self, text: str) -> str:
        """Format header text."""
        if COLORAMA_AVAILABLE:
            return f"{Style.BRIGHT}{Fore.CYAN}{text}{Style.RESET_ALL}"
        return text

    def _get_formatted_text(self, text: str, color: str) -> str:
        """Format text with color."""
        if not COLORAMA_AVAILABLE:
            return text

        color_map = {
            'cyan': Fore.CYAN,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'red': Fore.RED,
            'white': Fore.WHITE,
            'dim': Fore.LIGHTBLACK_EX,
        }

        color_code = color_map.get(color, '')
        return f"{Style.BRIGHT}{color_code}{text}{Style.RESET_ALL}"

    def _get_formatted_color(self, text: str, color: str) -> str:
        """Colorize text."""
        if COLORAMA_AVAILABLE:
            color_map = {
                'cyan': Fore.CYAN,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'blue': Fore.BLUE,
                'red': Fore.RED,
                'white': Fore.WHITE,
                'dim': Fore.LIGHTBLACK_EX,
            }
            color_code = color_map.get(color, '')
            return f"{color_code}{text}{Style.RESET_ALL}"
        return text

    def _print_formatted_text(self, text: str, width: int = 80) -> str:
        """Print text with wrapping."""
        lines = text.split('\n')
        for line in lines:
            if len(line) > width:
                # Simple word wrap
                words = line.split()
                wrapped_line = []
                current_line = []
                current_length = 0

                for word in words:
                    if current_length + len(word) + 1 <= width:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        wrapped_line.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)

                if current_line:
                    wrapped_line.append(' '.join(current_line))

                for wrapped in wrapped_line:
                    print(self._get_formatted_color(wrapped, 'white'))
            else:
                print(self._get_formatted_color(line, 'white'))
        return text

    def _get_input(self, prompt: str) -> str:
        """Get user input with formatting."""
        try:
            if COLORAMA_AVAILABLE:
                return input(f"{prompt}{Style.RESET_ALL}")
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\n")
            return ""


def main():
    """Main application entry point."""
    explorer = PythonExplorer()

    print("\n" + "=" * 60)
    print("Welcome to the Python Features Explorer!".center(60))
    print("Type 'exit' or 'quit' to quit, or enter a number to select.")
    print("Type 'help' for commands, 'stats' for statistics, 'fav' for favorites")
    print("=" * 60)

    session_start = datetime.now()
    last_save = datetime.now()
    save_interval = 5 * 60  # Save every 5 minutes

    while True:
        try:
            choice = explorer.display_menu()

            if choice.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! Happy coding! 🐍\n")
                break

            if choice.lower() == 'help':
                print("\nAvailable commands:")
                print("  1-N: Select chapter")
                print("  exit, quit, q: Exit application")
                print("  help: Show this help")
                print("  stats: Show user statistics")
                print("  fav: Toggle favorite mode")
                print("  config: Show current configuration")
                print()
                continue

            if choice.lower() == 'stats':
                explorer.show_statistics()
                input("\nPress Enter to continue...")
                continue

            if choice.lower() == 'fav':
                explorer.config['display'].setdefault('toggle_fav_mode', False)
                explorer.config['display']['toggle_fav_mode'] = not explorer.config['display']['toggle_fav_mode']
                fav_mode = "ON" if explorer.config['display']['toggle_fav_mode'] else "OFF"
                print(f"Favorite mode is now {fav_mode}")
                continue

            if choice.lower() == 'config':
                print("\nConfiguration:")
                for section, items in explorer.config.items():
                    print(f"\n[{section}]")
                    for key, value in items.items():
                        print(f"  {key}: {value}")
                continue

            try:
                choice_idx = int(choice)

                if choice_idx == len(explorer.chapters) + 1:
                    print("\nGoodbye! Happy coding! 🐍\n")
                    break

                if 1 <= choice_idx <= len(explorer.chapters):
                    chapter = explorer.chapters[choice_idx - 1]
                    example_choice = explorer.display_chapter_details(chapter)

                    if example_choice and example_choice.isdigit():
                        num_example = int(example_choice)

                        if 1 <= num_example <= len(chapter.examples):
                            chapter_dir = chapter.name.lower().replace(' ', '_')
                            explorer.run_example(chapter_dir, chapter.examples[num_example - 1], chapter.number)

                            # Check if all examples viewed
                            viewed_count = len(explorer.user_progress.viewed_examples.get(chapter.number, []))
                            if viewed_count == len(chapter.examples):
                                print(f"\n{explorer._get_formatted_text('All examples completed! Mark as finished?', 'yellow')}")
                                if explorer._get_input("(y/n) > ").lower().startswith('y'):
                                    explorer.complete_chapter(chapter.number)
                        elif num_example == len(chapter.examples) + 1:
                            # Back to menu
                            if chapter.number not in explorer.user_progress.completed_chapters:
                                viewed_count = len(explorer.user_progress.viewed_examples.get(chapter, []))
                                if viewed_count > 0:
                                    print(f"Progress: {viewed_count}/{len(chapter.examples)} examples")

                        # Enable/disable quiz if available
                        quizzes_config = explorer.config.get('quizzes', {})
                        if quizzes_config.get('enabled', False) and num_example <= len(chapter.examples):
                            if explorer._get_input("\nTry quiz for this chapter? (y/n) ").lower().startswith('y'):
                                if not explorer.display_quiz(chapter):
                                    input("\nPress Enter to continue...")
                                    continue

                        # Favorite toggle
                        if explorer.config.get('display', {}).get('toggle_fav_mode', False):
                            explorer.toggle_favorite(chapter.number)

                    else:
                        input("\nPress Enter to continue...")

            except ValueError:
                if choice.lower().startswith('f'):
                    explorer.toggle_favorite(choice[1:])
                else:
                    print("Invalid selection! Please enter a number or command.")
                    # Only show continuation message if there were valid commands before
                    print("Press Enter to continue. . .")
                    try:
                        input()
                    except EOFError:
                        print("\n")

            # Auto-save progress
            if (datetime.now() - last_save).total_seconds() > save_interval:
                explorer._save_user_progress()
                last_save = datetime.now()

        except EOFError:
            print("\n\nEnd of input. Saving progress and exiting...")
            explorer._save_user_progress()
            break

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Saving progress and exiting...")
            explorer._save_user_progress()
            break

    # Save final progress
    explorer._save_user_progress()

    # Calculate session time
    session_end = datetime.now()
    duration = (session_end - session_start).total_seconds() / 60
    explorer.user_progress.total_time_spent += int(duration)
    explorer._save_user_progress()

    logger.info(f"Session lasted {duration:.1f} minutes")
    print(f"\nSession completed! You spent {duration:.1f} minutes.")


if __name__ == "__main__":
    main()
