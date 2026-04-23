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
from lesson_interface import lesson_storage

_lesson_storage = lesson_storage()

app = Flask(__name__)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/', methods=['GET'])
def home():
    requested_lesson_id = request.args.get('lesson', default=1, type=int)
    lesson = _lesson_storage.get_lesson_by_id(requested_lesson_id)

    if lesson is None:
        requested_lesson_id = 1
        lesson = _lesson_storage.get_lesson_by_id(requested_lesson_id)

    next_lesson = _lesson_storage.get_next_lesson(requested_lesson_id)

    return render_template(
        'Question_Test.html',
        lesson=lesson,
        current_lesson_id=requested_lesson_id,
        next_lesson_id=next_lesson.id if next_lesson else None,
        next_lesson_title=next_lesson.title if next_lesson else None
    )

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

    

        
