"""
Interface App Module for Sprint 1. 

General purpose: This module serves as the main interface for the application. It will take input from the controller file and display/update 
the user interface accordingly.

Classes:
TBD

Functions:
TBD 
"""

from flask import Flask, request
from flaskwebgui import FlaskUI

from controller import process_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Variable Initialization
    result = ""
    questions_html = ""

    # Handle form submission
    if request.method == 'POST':
        code = request.form.get('code') # For the testing of the code without the need of an IDE, will be changed.
        response = process_code(code)

        print(type(response))
        print(response)
        
        if not response["success"]:
            result = f"<p style='color:red;'>Error: {response['error']}</p>"
        else:
            result = "<p style='color:green;'>Code processed successfully!</p>"

            questions_html = "<h3>Generated Questions:</h3>"
            for q in response["questions"]:
                questions_html += f"<p>{q['question']}</p>"

    return f"""
    <html>
    <head>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const textarea = document.getElementById('codebox');
                textarea.addEventListener('paste', function(e) {{
                    e.preventDefault();
                    alert("Pasting is disabled!");
                }});
            }});
        </script>
    </head>
    <body>
        <h1>Python Learning Notebook</h1>

        <form method="post">
            <textarea id="codebox" name="code" rows="10" cols="60"
            placeholder="Type your Python code here..."></textarea><br><br>

            <button type="submit">Run & Generate Questions</button>
        </form>

        {result}
        {questions_html}
    </body>
    </html>
    """

if __name__ == '__main__':
    ui = FlaskUI(app=app, server="flask", width=800, height=600)
    ui.run()

    

        