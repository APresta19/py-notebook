"""
Lesson interfacing module for Sprint 1.

General purpose: This module provides a simple interface for students to navigate
and view lessons. It includes a lesson selection menu, lesson display window,
and navigation between lessons and the main menu.

Classes:
- lesson: Represents a lesson with a title and content.
- lesson_storage: Stores and retrieves lesson content.
- lesson_interface: Handles user interaction for lesson navigation.

Functions:
TBD
"""

from dataclasses import dataclass
from typing import List, Optional


# Define a dataclass for lessons
@dataclass
class lesson:
    id: int
    title: str
    content: str
    guidelines: str = ""
    problem_description: str = ""


# Class to store and retrieve lessons
class lesson_storage:
    def __init__(self):
        self.lessons: List[lesson] = self.load_lessons()

    def load_lessons(self) -> List[lesson]:
        # Placeholder lessons
        return [
            lesson(
                id=1,
                title="Variables in Python",
                content="Variables store data values. Example:\n\nx = 5\ny = 'Hello'",
                guidelines=(
                    "• Variable names must start with a letter or underscore, not a number.\n"
                    "• Use descriptive names (e.g. age, not a).\n"
                    "• Python is case-sensitive: myVar and myvar are different.\n"
                    "• You can reassign a variable to a new value at any time."
                ),
                problem_description=(
                    "Create two variables: one named name that stores your name as a string, "
                    "and one named age that stores your age as an integer. "
                    "Then print both variables on separate lines."
                ),
            ),
            lesson(
                id=2,
                title="Loops in Python",
                content="Loops allow repeated execution. Example:\n\nfor i in range(5):\n    print(i)",
                guidelines=(
                    "• Use a for loop when you know how many times to repeat.\n"
                    "• range(n) produces numbers from 0 up to (but not including) n.\n"
                    "• Indent the loop body with 4 spaces — Python requires consistent indentation.\n"
                    "• Use a while loop when repeating until a condition changes."
                ),
                problem_description=(
                    "Write a for loop that prints every even number from 2 to 10 (inclusive). "
                    "Hint: range() accepts a step argument — try range(start, stop, step)."
                ),
            ),
            lesson(
                id=3,
                title="Output in Python",
                content="Use print() to display output. Example:\n\nprint('Hello World')",
                guidelines=(
                    "• print() can take multiple arguments separated by commas.\n"
                    "• Use an f-string for easy variable formatting: print(f'Hello, {name}!').\n"
                    "• The sep parameter controls what goes between items (default is a space).\n"
                    "• The end parameter controls what is printed at the end (default is a newline)."
                ),
                problem_description=(
                    "Using a single print() statement, output your name and age in the format:\n"
                    "My name is <name> and I am <age> years old.\n"
                    "Use an f-string to insert the variable values."
                ),
            ),
        ]

    def get_all_lessons(self) -> List[lesson]:
        return self.lessons

    def get_lesson_by_id(self, lesson_id: int) -> Optional[lesson]:
        for l in self.lessons:
            if l.id == lesson_id:
                return l
        return None


# Class to handle lesson interface
class lesson_interface:
    def __init__(self):
        self.storage = lesson_storage()

    # 1. Create Lesson Selection Interface
    def display_lesson_menu(self):
        print("\n=== Lesson Menu ===")
        lessons = self.storage.get_all_lessons()

        for lesson in lessons:
            print(f"{lesson.id}. {lesson.title}")

        print("0. Return to Main Menu")

    # 2. Implement Lesson Display Window
    def display_lesson(self, lesson_id: int):
        lesson = self.storage.get_lesson_by_id(lesson_id)

        if not lesson:
            print("Lesson not found.")
            return

        print(f"\n=== {lesson.title} ===")

        # 4. Implement Textbox for Lesson Guidelines
        print("\n--- Lesson Content ---")
        print(lesson.content)
        print("----------------------")

    # 5. Navigation between Lessons and Main Menu
    def run(self):
        while True:
            self.display_lesson_menu()
            choice = input("Select a lesson: ")

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            choice = int(choice)

            if choice == 0:
                print("Returning to Main Menu...")
                break

            # 3. Connect Lesson Selection to Lesson Content Retrieval
            self.display_lesson(choice)

            input("\nPress Enter to return to the lesson menu...")