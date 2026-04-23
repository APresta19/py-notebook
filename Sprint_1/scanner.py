"""
Scanner functionality for Sprint 1. 

General purpose: This module is responsible for taking the code input as a single string, parsing it into lines, and sorting those lines
into a dictionary based on their type (e.g., variable assignments, function definitions, output statements). This will allow us to 
easily generate questions based on the code structure.

Classes:
TBD

Functions:
infer_type: A helper function that takes a string value and attempts to infer its type (e.g., int, str, bool)
scan_code: The main function that takes a string of code, splits it into lines, and categorizes each line 
into a context dictionary for later use in question generation.


"""

"""
Function: infer_type

Description: This function takes a string value and attempts to infer its type based on simple heuristics. It checks if the value is a digit (indicating an integer), if it starts with quotes (indicating a string), or if it is "True" or "False" (indicating a boolean). If none of these conditions are met, it returns "unknown".

@precondition: General scanning function recognizes a variable assignment and extracts the value as a string to be passed to this function.
@postcondition: Returns a string indicating the inferred type of the value ("int", "str", "bool", or "unknown") back to scanner for use in
question generation.

@param value: A string representing a value from the code (e.g., "42", '"hello"', "True").
"""
def infer_type(value: str):
    value = value.strip()
    if value.isdigit():
        return "int"
    if value.startswith('"') or value.startswith("'"):
        return "str"
    if value in ["True", "False"]:
        return "bool"
    return "unknown"



"""
Function: scan_code

Description: This function takes a string of code, splits it into lines, and categorizes each line based on its content. 
It looks for variable assignments, print statements, and loops, and organizes this information into a context dictionary.

@precondition: The input is a string of code that may contain variable assignments, print statements, and loops.
@postcondition: Returns a context dictionary that categorizes the code elements, which can be used
for question generation.

@param code: A string containing the code to be scanned.
@return: A dictionary with categorized code elements (e.g., variables, values, loops, prints).
"""
import io
import sys

def scan_code(code: str):
    # The context dictionary is the main return value for later functions regarding question generation.
    context = {
        "variables": {},
        "loops": [],
        "prints": [],
        "outputs": ""
        # Additional categories can be added as needed (e.g., function definitions, conditionals, etc.)
    }

    lines = code.splitlines()
    for line in lines:
        line = line.strip()

        # Variable assignment check
        if "=" in line and not any(op in line for op in ["==", ">=", "<=", "!="]) and not line.startswith(("if ", "elif ", "while ", "for ")): 
            parts = line.split("=")
            var = parts[0].strip()
            context["variables"][var] = None  # placeholder
        
        # Print statement check
        if line.startswith("print("):
            context["prints"].append(line)
        
        # Loop check (very basic, can be expanded to include more complex loop structures)
        if line.startswith("for ") or line.startswith("while "):
            context["loops"].append(line)
        
        # New execution output check 
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()  # Redirect stdout to capture print output

        try:
            local_vars = {}
            exec(code, {}, local_vars)

            # Capture output
            context["output"] = sys.stdout.getvalue().strip()

            # Fill real variable values
            for var in context["variables"]:
                if var in local_vars:
                    context["variables"][var] = local_vars[var]

        except Exception as e:
            context["output"] = f"Error: {str(e)}"

        finally:
            sys.stdout = old_stdout

    return context
        
