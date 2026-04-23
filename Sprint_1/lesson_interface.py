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
    problem_description_2: str = ""


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
                problem_description_2=(
                    "You are building a simple receipt. Create variables for three items: "
                    "each item should have a name (string) and a price (float). "
                    "Calculate the subtotal by adding all three prices. "
                    "If the subtotal is greater than 20, apply a 10% discount. "
                    "Print each item name and price, then print the final total."
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
                problem_description_2=(
                    "Print a 5x5 multiplication table using nested for loops. "
                    "Each row should show the products for one number (1 through 5). "
                    "Format each value so the columns line up neatly. "
                    "Hint: use print(value, end='\\t') to separate values with a tab, "
                    "and print() with no arguments to move to the next row."
                ),
            ),
            lesson(
                id=3,
                title="Conditionals in Python",
                content="Conditionals control the flow of a program. Example:\n\nx = 10\nif x > 5:\n    print('Greater')\nelif x == 5:\n    print('Equal')\nelse:\n    print('Less')",
                guidelines=(
                    "• Use if to check a condition; the block runs only when the condition is True.\n"
                    "• elif lets you check additional conditions after the first if.\n"
                    "• else runs when none of the above conditions are True.\n"
                    "• Comparison operators: == (equal), != (not equal), >, <, >=, <=.\n"
                    "• Indent each block with 4 spaces — Python requires consistent indentation."
                ),
                problem_description=(
                    "Write a program that stores a number in a variable called score. "
                    "Using if/elif/else, print 'A' if score >= 90, 'B' if score >= 80, "
                    "'C' if score >= 70, or 'F' otherwise."
                ),
                problem_description_2=(
                    "Write a FizzBuzz program for a single number stored in a variable called n. "
                    "Print 'FizzBuzz' if n is divisible by both 3 and 5, "
                    "'Fizz' if divisible by only 3, "
                    "'Buzz' if divisible by only 5, "
                    "or the number itself otherwise. "
                    "Hint: use the modulo operator (%) and check the combined condition first."
                ),
            ),
            lesson(
                id=4,
                title="Cumulative Lesson",
                content="Solve the Problem.",
                guidelines=(
                    "• The problems incorporate the concepts from all of the previous lesson.\n"
                    "• Problem 2 is the extension of problem 1."
                ),
                problem_description=(
                    "Write a program that stores a variable called total set to 0 and a variable called count set to 0. "
                    "Use a for loop to go through every number from 1 to 20 (inclusive). "
                    "Inside the loop, use a conditional to check if the number is odd: if so, add it to total and increment count by 1. "
                    "After the loop, print the sum of all odd numbers and how many odd numbers were found. "
                    "Then use a conditional to print 'Above 100!' if total is greater than 100, or 'At most 100.' otherwise."
                ),
                problem_description_2=(
                    "Extend your program from Problem 1. In the same loop, also track the sum of even numbers in a variable called even_total. "
                    "After the loop, print both the odd sum and the even sum. "
                    "Use a conditional to print 'Odd sum wins' if the odd sum is greater, 'Even sum wins' if the even sum is greater, "
                    "or 'It is a tie!' if they are equal. "
                    "Then create a variable called grand_total equal to total + even_total and print it. "
                    "Use a final conditional to print 'Grand total is divisible by 5' or 'Grand total is not divisible by 5' based on the result."
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

    def get_next_lesson(self, lesson_id: int) -> Optional[lesson]:
        for l in self.lessons:
            if l.id > lesson_id:
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
