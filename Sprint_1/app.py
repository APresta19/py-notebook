"""
Interface App Module for Sprint 1. 

General purpose: This module serves as the main interface for the application. It will take input from the controller file and display/update 
the user interface accordingly.

Classes:
TBD

Functions:
TBD 
"""

from flask import Flask, request, render_template
from flaskwebgui import FlaskUI
from static.sockets.getSocketIO import socketio

from controller import process_code

app = Flask(__name__)
socketio.init_app(app, cors_allowed_origins="*")

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

    return render_template('Question_Test.html', result=result, questions_html=questions_html)

@app.route('/render-compiler')
def render_compiler():
    return render_template('Render_Compiler.html')

@socketio.on('compile')
def handle_compile(data):
    print("Received compile event with data: ", data)

@socketio.on('connect')
def handle_connect():
    print("Client connected!")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

from static.services.init_socket import init_socket
init_socket()

def run_app():
    socketio.run(app, host="127.0.0.1", port=5000)


if __name__ == '__main__':
    ui = FlaskUI(app=app, server="flask", width=1920, height=1080, port=5000)
    # Run socketio manually alongside the UI
    import threading
    t = threading.Thread(target=lambda: socketio.run(app, host="127.0.0.1", port=5000))
    t.daemon = True
    t.start()
    ui.run()

    

        