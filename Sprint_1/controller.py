"""
Controller module for Sprint 1.

General purpose: This module serves as the main entry point for the application. It will coordinate the scanning of code, 
generation of questions, and interaction with the user interface.

Classes:
TBD

Functions:
- process_code: The main function that takes a string of code, processes it to extract context, and generates questions based on that context.
- generate_questions: A helper function that takes a context dictionary and generates questions based on the available question templates in the question storage.

"""

import random
from question_storage import question_storage
from scanner import scan_code

# Variable Initialization
storage = question_storage()

"""
Function: process_code

Description: This function takes a string of code as input, processes it to extract context using the scanner, 
and then generates questions based on that context using the question storage.

@precondition: The input is a string of code that may contain variable assignments, print statements, and loops.
@postcondition: Returns a list of generated questions based on the code context and the available question
templates, as well as the context dictionary for potential use in the user interface.

@param code: A string containing the code to be processed.
@return: A tuple containing a list of generated questions and the context dictionary.
"""
def process_code(code: str):

    valid, error = validate_code(code)

    if not valid:
        return{
            "success": False,
            "error": error,
            "questions": [],
        }
    # Scan the code to extract context
    context = scan_code(code)
    
    # Generate questions based on the context and available question templates
    questions = generate_questions(context)

    return {
        "success": True,
        "error": None,
        "questions": questions,
        "context": context
    }


"""
Function: generate_questions

Description: This function takes a context dictionary as input and generates questions based on the available question templates in the question storage. 
It iterates through the question templates and fills in the placeholders with relevant information from the context.

@precondition: The input is a context dictionary that categorizes code elements (e.g., variables, values, loops, prints).
@postcondition: Returns a list of generated questions based on the code context and the available question templates.

@param context: A dictionary containing categorized code elements (e.g., variables, values, loops, prints).
@return: A list of generated questions, where each question is a tuple containing the question text and any associated options (if applicable).
"""
def generate_questions(context):
    questions = []

    for template in storage.get_all_questions():

        if template.id == "var_type":
            for var in context["variables"]:
                q = template.prompt.format(var=var)
                questions.append({
                    "question": q,
                    "options": template.options,
                    "type": template.qtype
                })

        if template.id == "var_value":
            for var in context["variables"]:
                q = template.prompt.format(var=var)
                questions.append({
                    "question": q,
                    "options": template.options,
                    "type": template.qtype
                })

        if template.id == "output":
            q = template.prompt.format()
            questions.append({
                "question": q,
                "options": template.options,
                "type": template.qtype
            })
        
        if template.id == "loop_count":
            for loop in context["loops"]:
                q = template.prompt.format(loop_count=loop)
                questions.append({
                    "question": q,
                    "options": template.options,
                    "type": template.qtype
                })
    
    return questions
    
## Validate function is meerly for TESTING purposes.
def validate_code(code):
    # Basic validation to check if the code is not empty and contains valid characters
    if not code.strip():
        return False, "Code cannot be empty."
    
    # Additional validation can be added here (e.g., checking for balanced parentheses, valid syntax, etc.)
    
    return True, None 