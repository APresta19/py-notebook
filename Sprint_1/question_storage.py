"""
Question storage module for Sprint 1.

General purpose: This module provides a simple in-memory storage mechanism for questions. 
It allows adding, retrieving, and listing questions.

Classes:
- question_template: A class that represents a question template with attributes like question text, options, and correct answer.
- question_storage: A class that manages the storage of questions.

Functions:
TBD

"""
from dataclasses import dataclass #Neccessary for using dataclass decorator, which simplifies the creation of classes that are primarily used to store data.
from typing import List, Dict, Optional

# Define a dataclass for question templates, which will hold the structure of a question, including its ID, category, prompt, type, and optional fields for placeholders and options.
@dataclass
class question_template:
    id: int
    category: str
    prompt: str
    qtype: str
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None

# Class header TBD
class question_storage:
    def __init__(self):
        self.questions: List[question_template] = self.load_questions()
        
    def load_questions(self) -> List[question_template]:
        # For now, we will return some hardcoded questions.
        return [
            # -------- VARIABLE QUESTIONS --------
            question_template(
                id="var_type",
                category="variables",
                prompt="What is the type of {var}?",
                qtype="multiple_choice",
                placeholder=["var"],
                options=["int", "str", "float", "list", "bool"]
            ),

            question_template(
                id="var_value",
                category="variables",
                prompt="What is the value of {var} after execution?",
                qtype="short_answer",
                placeholder=["var"]
            ),

            # -------- OUTPUT QUESTIONS --------
            question_template(
                id="output",
                category="output",
                prompt="What is the output of this code?",
                qtype="short_answer",
                placeholder=[]
            ),

            # -------- LOOP QUESTIONS --------
            question_template(
                id="loop_count",
                category="loops",
                prompt="How many times does this loop run?",
                qtype="multiple_choice",
                placeholder=["loop_count"]
            ),
        ]
    
    def get_all_questions(self) -> List[question_template]:
        return self.questions
    






