#!/usr/bin/env python3
"""Python Features Explorer - Interactive CLI application."""

import subprocess
import os
from typing import Dict, List, Tuple


class PythonExplorer:
    """Main application class for exploring Python features."""

    def __init__(self):
        self.chapters = self._load_chapters()

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

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("PYTHON FEATURES EXPLORER".center(60))
        print("=" * 60)
        
        for idx, chapter in enumerate(self.chapters, 1):
            print(f"{idx}. {chapter['name']}")
        
        print(f"\n{len(self.chapters) + 1}. Exit")
        return input("\nSelect a chapter (1-{})> ".format(len(self.chapters) + 1))

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


def main():
    """Main application entry point."""
    explorer = PythonExplorer()
    
    # Demo mode: test with a sample flow
    print("\n" + "=" * 60)
    print("Welcome to the Python Features Explorer!")
    print("Type 'exit' to quit, or enter a number to select.")
    print("=" * 60)
    
    while True:
        try:
            choice = explorer.display_menu()
            choice_idx = int(choice)
            
            if choice_idx == len(explorer.chapters) + 1:
                print("\nGoodbye! Happy coding! 🐍\n")
                break
            
            if 1 <= choice_idx <= len(explorer.chapters):
                chapter = explorer.chapters[choice_idx - 1]
                example_choice = explorer.display_chapter_details(chapter)
                
                if example_choice and example_choice.isdigit() and int(example_choice) <= len(chapter.get('examples', [])):
                    chapter_dir = chapter['name'].lower().replace(' ', '_')
                    explorer.run_example(chapter_dir, chapter['examples'][int(example_choice) - 1])
                else:
                    input("\nPress Enter to continue...")
            else:
                print("Invalid selection! Please try again.")
                input("\nPress Enter to continue...")
        
        except ValueError:
            print("Invalid input! Please enter a number.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
