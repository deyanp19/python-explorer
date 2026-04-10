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
        """Generate quiz questions from a README file."""
        if not num_questions:
            num_questions = self.config.get('quizzes', {}).get('questions_per_chapter', 5)

        if not os.path.exists(readme_path):
            print(f"Error: File not found: {readme_path}")
            return []

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            questions = []

            # Generate questions from different types of content
            questions.extend(self._generate_code_example_questions(content, chapter_number))
            questions.extend(self._generate_topic_questions(content, chapter_number))
            questions.extend(self._generate_concept_questions(content, chapter_number))

            # Limit to requested number
            questions = questions[:num_questions]

            # Ensure at least some questions exist
            if not questions:
                questions = self._generate_fallback_questions(content, chapter_number)

            self.questions_history.extend(questions)
            return questions

        except Exception as e:
            print(f"Error generating quiz: {e}")
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
                explanation=f"Chapter focuses on {first_item}"
            ))

        return questions

    def _generate_fallback_questions(self, content: str,
                                     chapter_number: str) -> List[QuizQuestion]:
        """Generate fallback questions when specific content not available."""
        return [QuizQuestion(
            chapter_number=chapter_number,
            question="What is the main topic of this chapter?",
            options=[
                "Python Programming Fundamentals",
                "Web Development",
                "Data Science",
                "Machine Learning"
            ],
            answer=1,
            explanation="This chapter introduces Python programming concepts"
        )]

    def generate_quiz_file(self, chapter_number: str, output_file: str) -> bool:
        """Generate quiz questions and save to JSON file."""
        readme_path = os.path.join('content', f'ch{chapter_number}', 'README.md')

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
            chapter_num = chapter_dir.replace('ch', '')[0] if chapter_dir.startswith('ch') else '00'
            readme_path = os.path.join('content', chapter_dir, 'README.md')

            if os.path.exists(readme_path):
                output_file = os.path.join(output_dir, f'quiz_ch{chapter_num}.json')
                if self.generate_quiz_file(chapter_num, output_file):
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
