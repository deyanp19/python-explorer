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
    quiz_history: Dict[str, List] = field(default_factory=dict)
    example_ratings: Dict[str, float] = field(default_factory=dict)
    favorites: List[str] = field(default_factory=list)
    last_session: Optional[str] = None
    total_time_spent: int = 0  # in minutes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary."""
        return {
            'username': self.username,
            'completed_chapters': self.completed_chapters,
            'viewed_examples': self.viewed_examples,
            'quiz_scores': {k: float(v) if isinstance(v, (int, float)) else v 
                          for k, v in self.quiz_scores.items()},
            'quiz_history': self.quiz_history,
            'example_ratings': self.example_ratings,
            'favorites': self.favorites,
            'last_session': self.last_session,
            'total_time_spent': self.total_time_spent
        }


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
        'quizzes': {
            'enabled': False,
            'questions_per_quiz': 5,
            'passing_score': 70,
            'max_quiz_retries': -1,
            'show_explanations': True,
            'retry_after_fail': True
        },
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

            # Load quiz questions if available
            quiz_questions = []
            quiz_file = os.path.join('quizzes', f'quiz_ch{number}.json')
            if os.path.exists(quiz_file):
                try:
                    with open(quiz_file, 'r') as f:
                        quiz_data = json.load(f)
                        quiz_questions = quiz_data.get('questions', [])
                        logger.info(f"Loaded {len(quiz_questions)} questions from {quiz_file}")
                except Exception as e:
                    logger.warning(f"Failed to load quiz file {quiz_file}: {e}")
                    quiz_questions = []

            return Chapter(
                number=number,
                name=chapter_name,
                readme_path=readme_path,
                examples=examples,
                description=description,
                quiz_questions=quiz_questions
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
        """Display quiz for a chapter with enhanced randomized questions."""
        quiz_config = self.config.get('quizzes', {})
        if not quiz_config.get('enabled', False):
            print("\nQuizzes are not enabled. Enable in config.yaml to use.")
            return True

        # Get questions from chapter (loaded from JSON)
        questions = getattr(chapter, 'quiz_questions', [])
        
        if not questions:
            print(f"\nNo quiz questions available for {chapter.name}")
            return True

        # Randomly select questions if pool is larger than needed
        num_questions = quiz_config.get('questions_per_quiz', 11)
        if len(questions) > num_questions:
            import random
            questions = random.sample(questions, num_questions)
            # Update chapter's quiz_questions to reflect selection
            chapter.quiz_questions = questions

        # Handle retry logic
        retry_config = quiz_config.get('retry_after_fail', True)
        max_retries = quiz_config.get('max_quiz_retries', -1)
        
        # Check if user can retry
        can_retry = retry_config and max_retries != 0
        
        # Display quiz header
        print(f"\n{self._get_formatted_text('QUIZ', 'cyan')} - {chapter.name}")
        print("=" * 50)
        print(f"Questions: {len(questions)} | Passing score: {quiz_config.get('passing_score', 70)}%")
        
        if can_retry:
            attempts = self.user_progress.quiz_history.get(chapter.number, [])
            if max_retries > 0:
                print(f"Retries: {len(attempts)}/{max_retries}")
            else:
                print(f"Unlimited retries allowed")

        score = 0
        total = min(len(questions), quiz_config.get('questions_per_quiz', 5))
        attempts = []

        # Process each question
        for i, question in enumerate(questions[:total], 1):
            print(f"\n{i}. {question['question']}")
            
            # Display options without revealing the answer
            for j, option in enumerate(question['options'], 1):
                print(f"   ○ {j}. {self._get_formatted_text(option, 'white')}")

            try:
                answer = int(self._get_input(f"Enter your answer ({1}-{len(question['options'])})> "))
                if 1 <= answer <= len(question['options']):
                    is_correct = (answer == question['answer'])
                    
                    attempts.append({
                        'question': i,
                        'user_answer': answer,
                        'correct': question['answer'],
                        'correct_answer': question['options'][question['answer'] - 1],
                        'is_correct': is_correct
                    })
                    
                    if is_correct:
                        print(f"{self._get_formatted_text('✓ Correct!', 'green')}")
                        score += 1
                    else:
                        print(f"{self._get_formatted_text('✗ Incorrect!', 'red')}")
                        correct_answer_text = question['options'][question['answer'] - 1]
                        print(f"  Correct answer: {correct_answer_text}")
                        if quiz_config.get('show_explanations', True) and question.get('explanation'):
                            print(f"  Explanation: {question['explanation']}")
                else:
                    print(f"{self._get_formatted_text('Invalid number!', 'yellow')}")
                    attempts.append({
                        'question': i,
                        'user_answer': None,
                        'correct': question['answer'],
                        'correct_answer': question['options'][question['answer'] - 1],
                        'is_correct': False
                    })
            except ValueError:
                print(f"{self._get_formatted_text('Invalid input!', 'yellow')}")
                attempts.append({
                    'question': i,
                    'user_answer': None,
                    'correct': question['answer'],
                    'correct_answer': question['options'][question['answer'] - 1],
                    'is_correct': False
                })

        # Calculate results
        percentage = (score / total) * 100
        passing = quiz_config.get('passing_score', 70)
        
        # Save attempt to history
        if chapter.number not in self.user_progress.quiz_history:
            self.user_progress.quiz_history[chapter.number] = []
        self.user_progress.quiz_history[chapter.number].append(attempts)
        
        # Display summary
        print("\n" + self._get_formatted_text('QUIZ RESULTS', 'yellow'))
        print("=" * 50)
        print(f"Score: {score}/{total} ({percentage:.1f}%)")
        
        status_color = 'green' if percentage >= passing else 'red'
        print(f"Status: {self._get_formatted_text('PASSED' if percentage >= passing else 'FAILED', status_color)}")
        print(f"Required: {passing}% to pass")
        
        # Detailed review if failed
        if percentage < passing:
            print("\n" + self._get_formatted_text('REVIEW YOUR ANSWERS:', 'yellow'))
            correct_count = sum(1 for a in attempts if a['is_correct'])
            incorrect_count = total - correct_count
            print(f"  Correct: {correct_count}/{total}")
            print(f"  Incorrect: {incorrect_count}/{total}")
            
            for attempt in attempts:
                if not attempt['is_correct']:
                    answer_display = f"{attempt['user_answer']}" if attempt['user_answer'] else "Skipped/Invalid"
                    print(f"  - Q{attempt['question']}: You answered '{answer_display}'")
                    print(f"    Correct: {attempt['correct_answer']}")
            
            if can_retry:
                print(f"\n{self._get_formatted_text('Tip: You can retry the quiz!', 'cyan')}")
            else:
                print(f"\n{self._get_formatted_text('Complete the examples and try again later.', 'yellow')}")

        # Update progress
        if percentage >= passing:
            print(f"\n{self._get_formatted_text('✓ Congratulations! Quiz passed!', 'green')}")
            self.complete_chapter(chapter.number)
            self.user_progress.quiz_scores[chapter.number] = percentage
            return True
        else:
            print(f"\n{self._get_formatted_text('✗ Keep practicing! Retake quiz after reviewing content', 'yellow')}")
            return False

    def _generate_fallback_quiz_questions(self, chapter: Chapter, content: str = "") -> List[Dict]:
        """Generate 11 quiz questions from chapter content as fallback."""
        questions = []
        
        chapter_num = int(chapter.number) if chapter.number.isdigit() else 1
        
        if chapter_num == 1:
            questions = [
                {
                    'question': 'What is the correct function to output text in Python?',
                    'options': ['output()', 'print()', 'write()', 'echo()'],
                    'answer': 2,
                    'explanation': 'The print() function in Python outputs text to the console.'
                },
                {
                    'question': 'What symbol is used for single-line comments in Python?',
                    'options': ['//', '#', '/*', '--'],
                    'answer': 2,
                    'explanation': 'The # symbol starts a single-line comment in Python.'
                },
                {
                    'question': 'Which keyword is used to import modules in Python?',
                    'options': ['include', 'import', 'using', 'require'],
                    'answer': 2,
                    'explanation': 'The import keyword is used to import modules in Python.'
                },
                {
                    'question': 'What is Python primarily known for?',
                    'options': ['Complex syntax', 'Readability', 'Speed', 'Hardware control'],
                    'answer': 2,
                    'explanation': 'Python is known for its simple and readable syntax.'
                },
                {
                    'question': 'Which data type represents decimal numbers?',
                    'options': ['int', 'float', 'str', 'bool'],
                    'answer': 2,
                    'explanation': 'float data type represents decimal (floating-point) numbers.'
                },
                {
                    'question': 'What is the correct extension for Python files?',
                    'options': ['.py', '.python', '.pt', '.pc'],
                    'answer': 1,
                    'explanation': 'Python files use the .py extension.'
                },
                {
                    'question': 'Which keyword defines a function in Python?',
                    'options': ['func', 'define', 'def', 'function'],
                    'answer': 3,
                    'explanation': 'The def keyword is used to define functions in Python.'
                },
                {
                    'question': 'What does Python use to define code blocks?',
                    'options': ['Braces', 'Indentation', 'Semicolons', 'Keywords'],
                    'answer': 2,
                    'explanation': 'Python uses indentation to define code blocks.'
                },
                {
                    'question': 'Which built-in function returns the type of an object?',
                    'options': ['kind()', 'type()', 'category()', 'class()'],
                    'answer': 2,
                    'explanation': 'The type() function returns the data type of an object.'
                },
                {
                    'question': 'What is the result of 10 / 3 in Python 3?',
                    'options': ['3', '3.33', '3.0', '3.333...'],
                    'answer': 4,
                    'explanation': 'Python 3 division returns a float result.'
                },
                {
                    'question': 'Which statement creates a variable in Python?',
                    'options': ['var x = 5', 'int x = 5', 'x = 5', 'declare x = 5'],
                    'answer': 3,
                    'explanation': 'Python uses simple assignment: variable_name = value.'
                }
            ]
        elif chapter_num == 2:
            questions = [
                {
                    'question': 'Which data structure is ordered and mutable?',
                    'options': ['list', 'tuple', 'set', 'dict'],
                    'answer': 1,
                    'explanation': 'Lists are ordered and mutable (can be changed).'
                },
                {
                    'question': 'Which data structure is ordered but immutable?',
                    'options': ['list', 'tuple', 'set', 'dict'],
                    'answer': 2,
                    'explanation': 'Tuples are ordered and immutable (cannot be changed).'
                },
                {
                    'question': 'What syntax is used to create a dictionary?',
                    'options': ['[]', '()', '{}', '<>'],
                    'answer': 3,
                    'explanation': 'Curly braces {} are used to create dictionaries.'
                },
                {
                    'question': 'How do you access an element by index in a list?',
                    'options': ['list.key', 'list[index]', 'list.name', 'list(0)'],
                    'answer': 2,
                    'explanation': 'Square brackets with index: list[index] accesses elements.'
                },
                {
                    'question': 'Which method adds an element to the end of a list?',
                    'options': ['push()', 'add()', 'append()', 'insert()'],
                    'answer': 3,
                    'explanation': 'append() adds an element to the end of a list.'
                },
                {
                    'question': 'What does set() do with duplicate values?',
                    'options': ['Keeps all duplicates', 'Removes duplicates', 'Errors out', 'Counts them'],
                    'answer': 2,
                    'explanation': 'Sets automatically remove duplicate values.'
                },
                {
                    'question': 'Which syntax creates a list comprehension?',
                    'options': ['for x in list: x', '[x for x in list]', 'list(x for x in list)', '(x for x in list)'],
                    'answer': 2,
                    'explanation': 'List comprehensions use square brackets: [expression for item in iterable].'
                },
                {
                    'question': 'How do you get the number of elements in a list?',
                    'options': ['list.size()', 'list.length', 'len(list)', 'size(list)'],
                    'answer': 3,
                    'explanation': 'The len() function returns the number of elements.'
                },
                {
                    'question': 'Which data structure stores key-value pairs?',
                    'options': ['list', 'tuple', 'set', 'dict'],
                    'answer': 4,
                    'explanation': 'Dictionaries store data as key-value pairs.'
                },
                {
                    'question': 'What is the main difference between list and tuple?',
                    'options': ['Lists are immutable', 'Tuples are immutable', 'Lists can only store ints', 'Tuples are unordered'],
                    'answer': 2,
                    'explanation': 'Tuples are immutable (cannot be modified after creation).'
                },
                {
                    'question': 'Which operator checks if an item is in a list?',
                    'options': ['in', 'contains', 'has', 'is'],
                    'answer': 1,
                    'explanation': 'The in operator checks membership: item in list.'
                }
            ]
        elif chapter_num == 3:
            questions = [
                {
                    'question': 'Which keyword starts a conditional statement?',
                    'options': ['when', 'else', 'if', 'case'],
                    'answer': 3,
                    'explanation': 'The if keyword begins conditional statements.'
                },
                {
                    'question': 'What keyword exits a loop immediately?',
                    'options': ['break', 'continue', 'exit', 'stop'],
                    'answer': 1,
                    'explanation': 'The break statement exits a loop immediately.'
                },
                {
                    'question': 'What keyword skips to the next iteration?',
                    'options': ['break', 'continue', 'skip', 'next'],
                    'answer': 2,
                    'explanation': 'The continue statement skips to the next loop iteration.'
                },
                {
                    'question': 'Which keyword is used for iteration loops?',
                    'options': ['while', 'for', 'repeat', 'loop'],
                    'answer': 2,
                    'explanation': 'The for keyword is used for iterating over sequences.'
                },
                {
                    'question': 'What keyword starts a loop based on a condition?',
                    'options': ['while', 'for', 'if', 'until'],
                    'answer': 1,
                    'explanation': 'The while loop repeats while a condition is true.'
                },
                {
                    'question': 'Which keyword handles alternative conditions?',
                    'options': ['else', 'otherwise', 'alt', 'switch'],
                    'answer': 1,
                    'explanation': 'The else keyword handles alternative conditions.'
                },
                {
                    'question': 'What keyword handles additional conditions?',
                    'options': ['elif', 'else if', 'elseif', 'if else'],
                    'answer': 1,
                    'explanation': 'The elif keyword checks additional conditions.'
                },
                {
                    'question': 'Which statement is a placeholder that does nothing?',
                    'options': ['null', 'pass', 'skip', 'ignore'],
                    'answer': 2,
                    'explanation': 'The pass statement is a placeholder that does nothing.'
                },
                {
                    'question': 'Can you use else with for loops?',
                    'options': ['No', 'Yes, executes when loop finishes', 'Yes, executes when loop breaks', 'Only with while'],
                    'answer': 2,
                    'explanation': 'Yes, else with for executes when the loop finishes normally (not broken).'
                },
                {
                    'question': 'What is the indentation requirement in Python?',
                    'options': ['Optional', '4 spaces minimum', 'Consistent indentation required', 'Any spaces work'],
                    'answer': 3,
                    'explanation': 'Python requires consistent indentation for code blocks.'
                },
                {
                    'question': 'How do you write a multi-way conditional?',
                    'options': ['if-else', 'if-elif-else', 'switch-case', 'multiple-if'],
                    'answer': 2,
                    'explanation': 'Use if-elif-else chains for multi-way conditionals.'
                }
            ]
        elif chapter_num == 4:
            questions = [
                {
                    'question': 'Which keyword defines a function?',
                    'options': ['func', 'define', 'def', 'function'],
                    'answer': 3,
                    'explanation': 'The def keyword is used to define functions.'
                },
                {
                    'question': 'What are *args used for?',
                    'options': ['Keyword arguments', 'Variable positional arguments', 'Default arguments', 'Named arguments'],
                    'answer': 2,
                    'explanation': '*args collects variable positional arguments into a tuple.'
                },
                {
                    'question': 'What are **kwargs used for?',
                    'options': ['Positional arguments', 'Variable keyword arguments', 'Required arguments', 'Default arguments'],
                    'answer': 2,
                    'explanation': '**kwargs collects variable keyword arguments into a dictionary.'
                },
                {
                    'question': 'What keyword creates anonymous functions?',
                    'options': ['lambda', 'anonymous', 'fn', 'func'],
                    'answer': 1,
                    'explanation': 'The lambda keyword creates anonymous (unnamed) functions.'
                },
                {
                    'question': 'Which function applies a function to all items?',
                    'options': ['map()', 'apply()', 'do()', 'run()'],
                    'answer': 1,
                    'explanation': 'map() applies a function to each item in an iterable.'
                },
                {
                    'question': 'Which function filters items based on a condition?',
                    'options': ['filter()', 'select()', 'where()', 'extract()'],
                    'answer': 1,
                    'explanation': 'filter() constructs an iterator from items where the function returns true.'
                },
                {
                    'question': 'What does the LEGB rule refer to?',
                    'options': ['Loop structures', 'Variable scope', 'Function arguments', 'Module imports'],
                    'answer': 2,
                    'explanation': 'LEGB rules the order of variable scope: Local, Enclosing, Global, Built-in.'
                },
                {
                    'question': 'Where are local variables defined?',
                    'options': ['Inside functions', 'Outside functions', 'In classes', 'In modules'],
                    'answer': 1,
                    'explanation': 'Local variables are defined inside functions.'
                },
                {
                    'question': 'What is the purpose of a function?',
                    'options': ['To repeat code', 'To organize reusable code', 'To define variables', 'To import modules'],
                    'answer': 2,
                    'explanation': 'Functions organize code into reusable, named blocks.'
                },
                {
                    'question': 'How do you return a value from a function?',
                    'options': ['print()', 'return', 'export', 'yield'],
                    'answer': 2,
                    'explanation': 'The return statement sends a value back from a function.'
                },
                {
                    'question': 'What happens if a function has no return statement?',
                    'options': ['Errors', 'Returns None', 'Returns 0', 'Returns False'],
                    'answer': 2,
                    'explanation': 'Functions without return statements return None.'
                }
            ]
        elif chapter_num == 5:
            questions = [
                {
                    'question': 'What keyword defines a class?',
                    'options': ['class', 'define', 'object', 'struct'],
                    'answer': 1,
                    'explanation': 'The class keyword is used to define classes.'
                },
                {
                    'question': 'What is the constructor method in Python classes?',
                    'options': ['__init__', '__construct__', '__start__', '__build__'],
                    'answer': 1,
                    'explanation': '__init__ is the constructor method called when creating objects.'
                },
                {
                    'question': 'What are methods ending with __ called?',
                    'options': ['Private methods', 'Dunder methods', 'Static methods', 'Class methods'],
                    'answer': 2,
                    'explanation': 'Methods with double underscores are called dunder or magic methods.'
                },
                {
                    'question': 'What does inheritance allow?',
                    'options': ['Multiple classes', 'Class reuse and extension', 'Function overloading', 'Variable types'],
                    'answer': 2,
                    'explanation': 'Inheritance allows creating new classes that reuse and extend existing classes.'
                },
                {
                    'question': 'What is the first parameter of instance methods?',
                    'options': ['self', 'this', 'cls', 'object'],
                    'answer': 1,
                    'explanation': 'self refers to the instance and is the first parameter of instance methods.'
                },
                {
                    'question': 'What is polymorphism?',
                    'options': ['Many constructors', 'Same method, different classes', 'Hidden data', 'Class nesting'],
                    'answer': 2,
                    'explanation': 'Polymorphism allows different classes to respond differently to the same method call.'
                },
                {
                    'question': 'How do you create an instance of a class?',
                    'options': ['class()', 'new Class()', 'Class()', 'make Class()'],
                    'answer': 3,
                    'explanation': 'Call the class like a function: Class_Name()'
                },
                {
                    'question': 'What does __str__ method do?',
                    'options': ['Compares objects', 'Returns string representation', 'Initializes', 'Destroys'],
                    'answer': 2,
                    'explanation': '__str__ returns a human-readable string representation of the object.'
                },
                {
                    'question': 'What is encapsulation?',
                    'options': ['Multiple classes', 'Hiding implementation details', 'Class inheritance', 'Method overloading'],
                    'answer': 2,
                    'explanation': 'Encapsulation hides internal details and exposes only necessary interfaces.'
                },
                {
                    'question': 'How do you access an object attribute?',
                    'options': ['object(attribute)', 'object.attribute', 'object[attribute]', 'object->attribute'],
                    'answer': 2,
                    'explanation': 'Use dot notation: object.attribute'
                },
                {
                    'question': 'What is the base class for all Python classes?',
                    'options': ['Base', 'Root', 'object', 'Parent'],
                    'answer': 3,
                    'explanation': 'object is the base class for all Python classes.'
                }
            ]
        elif chapter_num == 6:
            questions = [
                {
                    'question': 'Which block handles exceptions?',
                    'options': ['except', 'error', 'catch', 'handle'],
                    'answer': 1,
                    'explanation': 'The except block handles exceptions.'
                },
                {
                    'question': 'Which block always executes?',
                    'options': ['finally', 'always', 'end', 'done'],
                    'answer': 1,
                    'explanation': 'The finally block always executes, regardless of exceptions.'
                },
                {
                    'question': 'What happens when dividing by zero?',
                    'options': ['Returns 0', 'Returns None', 'Raises ZeroDivisionError', 'Returns infinity'],
                    'answer': 3,
                    'explanation': 'Division by zero raises a ZeroDivisionError.'
                },
                {
                    'question': 'How do you catch multiple exception types?',
                    'options': ['Multiple except blocks', 'except (Exception1, Exception2)', 'catch {Exception1, Exception2}', 'one except for all'],
                    'answer': 2,
                    'explanation': 'Use except (Exception1, Exception2) to catch multiple types.'
                },
                {
                    'question': 'What keyword raises an exception?',
                    'options': ['throw', 'raise', 'error', 'trigger'],
                    'answer': 2,
                    'explanation': 'The raise keyword is used to manually raise exceptions.'
                },
                {
                    'question': 'What is the base exception class?',
                    'options': ['Error', 'Exception', 'BaseError', 'StandardError'],
                    'answer': 2,
                    'explanation': 'Exception is the base class for all built-in exceptions.'
                },
                {
                    'question': 'Which block contains risky code?',
                    'options': ['try', 'risky', 'RISKY', 'risky'],
                    'answer': 1,
                    'explanation': 'The try block contains code that might raise exceptions.'
                },
                {
                    'question': 'How do you create a custom exception?',
                    'options': ['class CustomError(Exception)', 'def CustomError(Exception)', 'class Exception(CustomError)', 'def Exception(CustomError)'],
                    'answer': 1,
                    'explanation': 'Custom exceptions inherit from Exception: class CustomError(Exception).'
                },
                {
                    'question': 'Can you have else with try-except?',
                    'options': ['No', 'Yes, executes if no exception', 'Only with finally', 'Yes, always'],
                    'answer': 2,
                    'explanation': 'Yes, else executes when no exception is raised in try.'
                },
                {
                    'question': 'What exception occurs with invalid type conversion?',
                    'options': ['TypeError', 'ValueError', 'SyntaxError', 'NameError'],
                    'answer': 2,
                    'explanation': 'ValueError occurs when a function receives an argument of correct type but invalid value.'
                },
                {
                    'question': 'What exception occurs with undefined variables?',
                    'options': ['UndefinedError', 'NameError', 'VariableError', 'ReferenceError'],
                    'answer': 2,
                    'explanation': 'NameError occurs when a variable is not defined.'
                }
            ]
        elif chapter_num == 7:
            questions = [
                {
                    'question': 'Which keyword ensures proper resource cleanup?',
                    'options': ['try', 'finally', 'with', 'resource'],
                    'answer': 3,
                    'explanation': 'The with keyword ensures proper resource cleanup using context managers.'
                },
                {
                    'question': 'Which function opens files?',
                    'options': ['file()', 'open()', 'read()', 'fopen()'],
                    'answer': 2,
                    'explanation': 'The open() function is used to open files in Python.'
                },
                {
                    'question': 'What mode opens a file for writing?',
                    'options': ['r', 'w', 'a', 'x'],
                    'answer': 2,
                    'explanation': 'The w mode opens a file for writing (overwrites existing content).'
                },
                {
                    'question': 'What mode opens a file for reading?',
                    'options': ['r', 'w', 'a', 'x'],
                    'answer': 1,
                    'explanation': 'The r mode opens a file for reading (default mode).'
                },
                {
                    'question': 'How do you read the entire file content?',
                    'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.content()'],
                    'answer': 1,
                    'explanation': 'The read() method reads the entire file content as a string.'
                },
                {
                    'question': 'How do you read one line from a file?',
                    'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.line()'],
                    'answer': 2,
                    'explanation': 'The readline() method reads one line from the file.'
                },
                {
                    'question': 'How do you read all lines into a list?',
                    'options': ['file.read()', 'file.readline()', 'file.readlines()', 'file.lines()'],
                    'answer': 3,
                    'explanation': 'The readlines() method reads all lines into a list.'
                },
                {
                    'question': 'Which method writes to a file?',
                    'options': ['file.write()', 'file.print()', 'file.output()', 'file.send()'],
                    'answer': 1,
                    'explanation': 'The write() method writes a string to the file.'
                },
                {
                    'question': 'What happens when opening a non-existent file in w mode?',
                    'options': ['Error', 'Creates new file', 'Returns None', 'Opens read-only'],
                    'answer': 2,
                    'explanation': 'Opening in w mode creates a new file if it does not exist.'
                },
                {
                    'question': 'What is a context manager?',
                    'options': ['File handler', 'Manages resources with with statement', 'Exception handler', 'Variable manager'],
                    'answer': 2,
                    'explanation': 'A context manager manages resources using the with statement, ensuring cleanup.'
                },
                {
                    'question': 'Which module provides contextmanager decorator?',
                    'options': ['contextlib', 'context', 'manager', 'withlib'],
                    'answer': 1,
                    'explanation': 'The contextlib module provides the contextmanager decorator.'
                }
            ]
        elif chapter_num == 8:
            questions = [
                {
                    'question': 'Which keyword creates a generator?',
                    'options': ['generate', 'yield', 'return', 'yield from'],
                    'answer': 2,
                    'explanation': 'The yield keyword produces a value and pauses the function.'
                },
                {
                    'question': 'What is the main benefit of generators?',
                    'options': ['Faster execution', 'Memory efficiency', 'Parallel processing', 'Type safety'],
                    'answer': 2,
                    'explanation': 'Generators are memory efficient as they generate values on-demand.'
                },
                {
                    'question': 'Which decorator modifies a function?',
                    'options': ['decorator', '@decorator_name', 'decorate', '@wrap'],
                    'answer': 2,
                    'explanation': 'Decorators use @decorator_name syntax above the function.'
                },
                {
                    'question': 'What is a decorator?',
                    'options': ['A class method', 'A function that modifies another function', 'A variable marker', 'A type hint'],
                    'answer': 2,
                    'explanation': 'A decorator is a function that takes another function and extends its behavior.'
                },
                {
                    'question': 'What is the purpose of type hints?',
                    'options': ['Runtime type checking', 'Code documentation and IDE support', 'Faster execution', 'Memory management'],
                    'answer': 2,
                    'explanation': 'Type hints improve code documentation and enable better IDE autocomplete.'
                },
                {
                    'question': 'Which operator is used for unpacking in function calls?',
                    'options': ['*', '**', 'spread', 'expand'],
                    'answer': 1,
                    'explanation': '** is used for unpacking keyword arguments (dictionaries).'
                },
                {
                    'question': 'What does the * operator do for unpacking?',
                    'options': ['Unpacks keyword args', 'Unpacks positional args', 'Multiplies', 'Splat operator'],
                    'answer': 2,
                    'explanation': '* unpacks positional arguments (lists, tuples) into separate parameters.'
                },
                {
                    'question': 'Which keyword creates a lambda function?',
                    'options': ['lambda', 'anonymous', 'fn', 'func'],
                    'answer': 1,
                    'explanation': 'The lambda keyword creates small anonymous functions.'
                },
                {
                    'question': 'What is the syntax for type hinting a function?',
                    'options': ['def func(x: int) -> int:', 'def func(x int) int:', 'def func(x: int):', 'def func(int x): int'],
                    'answer': 1,
                    'explanation': 'Type hints use def func(param: type) -> return_type:'
                },
                {
                    'question': 'What is a generator function?',
                    'options': ['A function returning a list', 'A function using yield', 'A function creating objects', 'A function generating random numbers'],
                    'answer': 2,
                    'explanation': 'A generator function uses yield to produce a sequence of values.'
                },
                {
                    'question': 'How many times can a generator yield values?',
                    'options': ['Once', 'Multiple times', 'Twice', 'Never'],
                    'answer': 2,
                    'explanation': 'Generators can yield multiple values, resuming from where they paused.'
                }
            ]
        elif chapter_num == 9:
            questions = [
                {
                    'question': 'Which module provides threading support?',
                    'options': ['threading', 'threads', 'concurrent', 'asyncio'],
                    'answer': 1,
                    'explanation': 'The threading module provides thread-based parallelism.'
                },
                {
                    'question': 'Which method starts a thread?',
                    'options': ['thread.start()', 'thread.run()', 'start(thread)', 'thread.begin()'],
                    'answer': 1,
                    'explanation': 'The start() method begins thread execution.'
                },
                {
                    'question': 'Which module provides multiprocessing support?',
                    'options': ['multiprocessing', 'processes', 'parallel', 'multiprocess'],
                    'answer': 1,
                    'explanation': 'The multiprocessing module allows CPU-bound parallel execution.'
                },
                {
                    'question': 'What is GIL?',
                    'options': ['Global Internal Lock', 'Global Interpreter Lock', 'General Instruction List', 'Global Interface Layer'],
                    'answer': 2,
                    'explanation': 'The Global Interpreter Lock limits CPU-bound threads to one core.'
                },
                {
                    'question': 'Which keyword defines an async function?',
                    'options': ['async', 'async def', 'await', 'coroutine'],
                    'answer': 2,
                    'explanation': 'The async def syntax defines an asynchronous function.'
                },
                {
                    'question': 'Which keyword pauses in async functions?',
                    'options': ['pause', 'wait', 'await', 'suspend'],
                    'answer': 3,
                    'explanation': 'The await keyword pauses execution until the awaited coroutine completes.'
                },
                {
                    'question': 'What is threading used for?',
                    'options': ['CPU-bound tasks', 'I/O-bound tasks', 'Data processing', 'Matrix math'],
                    'answer': 2,
                    'explanation': 'Threading is best for I/O-bound tasks that wait for external resources.'
                },
                {
                    'question': 'What is multiprocessing used for?',
                    'options': ['I/O-bound tasks', 'CPU-bound tasks', 'Network requests', 'File operations'],
                    'answer': 2,
                    'explanation': 'Multiprocessing uses multiple CPU cores for CPU-bound tasks.'
                },
                {
                    'question': 'Which module provides asyncio support?',
                    'options': ['async', 'asyncio', 'async_support', 'coroutine'],
                    'answer': 2,
                    'explanation': 'The asyncio module provides async/await support.'
                },
                {
                    'question': 'What is the advantage of async/await?',
                    'options': ['Multi-core CPU use', 'Single-threaded concurrency', 'Memory reduction', 'Speed increase'],
                    'answer': 2,
                    'explanation': 'Async/await enables concurrent I/O operations in a single thread.'
                }
            ]
        elif chapter_num == 10:
            questions = [
                {
                    'question': 'Which class counts element occurrences?',
                    'options': ['Counter', 'Count', 'ElementCount', 'Frequency'],
                    'answer': 1,
                    'explanation': 'Counter from collections counts hashable objects.'
                },
                {
                    'question': 'Which class creates tuples with named fields?',
                    'options': ['NamedTuple', 'Named', 'FieldTuple', 'Record'],
                    'answer': 1,
                    'explanation': 'namedtuple from collections creates tuples with named fields.'
                },
                {
                    'question': 'Which function chains multiple iterables?',
                    'options': ['chain()', 'combine()', 'merge()', 'join()'],
                    'answer': 1,
                    'explanation': 'itertools.chain() concatenates multiple iterables.'
                },
                {
                    'question': 'Which function groups consecutive elements?',
                    'options': ['groupby()', 'group()', 'batch()', 'section()'],
                    'answer': 1,
                    'explanation': 'itertools.groupby() groups consecutive elements with the same key.'
                },
                {
                    'question': 'Which module handles date and time?',
                    'options': ['time', 'datetime', 'calendar', 'date'],
                    'answer': 2,
                    'explanation': 'The datetime module handles dates and times.'
                },
                {
                    'question': 'Which module provides system parameters?',
                    'options': ['sys', 'system', 'params', 'env'],
                    'answer': 1,
                    'explanation': 'The sys module provides access to system-specific parameters.'
                },
                {
                    'question': 'Which module provides operating system interfaces?',
                    'options': ['os', 'system', 'filesystem', 'platform'],
                    'answer': 1,
                    'explanation': 'The os module provides operating system interfaces.'
                },
                {
                    'question': 'What does os.path.join() do?',
                    'options': ['Joins file paths', 'Joins strings', 'Joins lists', 'Joins directories'],
                    'answer': 1,
                    'explanation': 'os.path.join() intelligently joins path components.'
                },
                {
                    'question': 'Which function reads environment variables?',
                    'options': ['os.getenv()', 'os.getenv()', 'os.environ()', 'os.get_var()'],
                    'answer': 2,
                    'explanation': 'os.getenv() or os.environ[KEY] reads environment variables.'
                },
                {
                    'question': 'Which module provides random number generation?',
                    'options': ['random', 'rand', 'randomize', 'chance'],
                    'answer': 1,
                    'explanation': 'The random module provides random number generation functions.'
                },
                {
                    'question': 'What does itertools.accumulate() do?',
                    'options': ['Accumulates values cumulatively', 'Accumulates lists', 'Accumulates dicts', 'Accumulates counters'],
                    'answer': 1,
                    'explanation': 'itertools.accumulate() returns accumulated sums or other binary functions.'
                }
            ]
        else:
            questions = [
                {
                    'question': f'What is the main topic of chapter {chapter_num}?',
                    'options': [
                        f'Python chapter {chapter_num} topics',
                        'General Python syntax',
                        'Data structures only',
                        'Object-oriented programming'
                    ],
                    'answer': 1,
                    'explanation': f'Chapter {chapter_num} covers advanced Python concepts.'
                },
                {
                    'question': 'What is Python?',
                    'options': [
                        'A high-level programming language',
                        'A database system',
                        'A web browser',
                        'An operating system'
                    ],
                    'answer': 1,
                    'explanation': 'Python is a versatile, high-level programming language.'
                },
                {
                    'question': 'Which data type is immutable?',
                    'options': ['list', 'dict', 'tuple', 'set'],
                    'answer': 3,
                    'explanation': 'Tuples are immutable data structures.'
                },
                {
                    'question': 'What symbol starts a comment?',
                    'options': ['//', '#', '/*', '--'],
                    'answer': 2,
                    'explanation': 'The # symbol starts single-line comments in Python.'
                },
                {
                    'question': 'Which keyword imports modules?',
                    'options': ['import', 'include', 'using', 'require'],
                    'answer': 1,
                    'explanation': 'The import keyword imports modules in Python.'
                },
                {
                    'question': 'What defines a function?',
                    'options': ['def', 'func', 'define', 'function'],
                    'answer': 1,
                    'explanation': 'The def keyword defines functions in Python.'
                },
                {
                    'question': 'Which loop iterates over sequences?',
                    'options': ['for', 'while', 'repeat', 'loop'],
                    'answer': 1,
                    'explanation': 'The for loop iterates over sequences in Python.'
                },
                {
                    'question': 'What handles exceptions?',
                    'options': ['try/except', 'try/catch', 'handle/error', 'try/finally'],
                    'answer': 1,
                    'explanation': 'try/except blocks handle exceptions in Python.'
                },
                {
                    'question': 'Which module handles file I/O?',
                    'options': ['built-in', 'fileio', 'filesystem', 'io'],
                    'answer': 1,
                    'explanation': 'File I/O is handled by built-in functions like open().'
                },
                {
                    'question': 'What is a Python module?',
                    'options': [
                        'A file containing Python code',
                        'A compiled binary',
                        'A database connection',
                        'A network protocol'
                    ],
                    'answer': 1,
                    'explanation': 'Modules are files containing Python code that can be imported.'
                }
            ]
        
        return questions[:11]

    def show_statistics(self) -> None:
        """Display user statistics."""
        print("\n" + self._get_formatted_text("USER STATISTICS", "green"))
        print("=" * 60)

        completed = len(self.user_progress.completed_chapters)
        total = len(self.chapters)
        progress_pct = int((completed / total) * 100) if total > 0 else 0

        # Quiz statistics
        quiz_scores = self.user_progress.quiz_scores
        quizzes_completed = len(quiz_scores)
        avg_quiz_score = sum(quiz_scores.values()) / len(quiz_scores) if quiz_scores else 0
        
        stats = [
            (f"Total Chapters", f"{total}"),
            (f"Completed Chapters", f"{completed} ({progress_pct}%)" if total > 0 else "0 (0%)"),
            (f"Favorited Chapters", f"{len(self.user_progress.favorites)}"),
            (f"Examples Rated", f"{len(self.user_progress.example_ratings)}"),
            (f"Quizzes Completed", f"{quizzes_completed}"),
            (f"Average Quiz Score", f"{avg_quiz_score:.1f}%" if quizzes_completed > 0 else "0%"),
            (f"Last Session", f"{self.user_progress.last_session or 'Never'}"),
            (f"Total Time Spent", f"{self.user_progress.total_time_spent} min"),
        ]

        for label, value in stats:
            print(f"{label:25} {value}")

        print("\n" + "-" * 60)
        print("CHAPTER PROGRESS:")
        print("-" * 60)

        # Chapter progress with quiz status
        for chapter in self.chapters:
            status = "✓" if chapter.number in self.user_progress.completed_chapters else " "
            viewed = len(self.user_progress.viewed_examples.get(chapter.number, []))
            examples = len(chapter.examples)
            viewed_pct = int((viewed / examples) * 100) if examples > 0 else 0
            
            # Quiz status
            quiz_status = ""
            if chapter.number in quiz_scores:
                score = quiz_scores[chapter.number]
                if score >= 70:
                    quiz_status = self._get_formatted_text(f" [Quiz: {score:.0f}%]", 'green')
                else:
                    quiz_status = self._get_formatted_text(f" [Quiz: {score:.0f}%]", 'yellow')
            
            status_line = f"  {status} Chap {chapter.number:2}: {chapter.name[:30]:<30} {viewed}/{examples} examples ({viewed_pct}%){quiz_status}"
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
                                viewed_count = len(explorer.user_progress.viewed_examples.get(chapter.number, []))
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
