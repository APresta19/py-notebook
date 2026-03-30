"""
...

General purpose: This module serves as a temporary tester for the compiler

Classes:
TBD

Functions:
TBD 
"""

from flask import Flask, request, render_template
from flaskwebgui import FlaskUI

from controller import process_code
from static.sockets.getSocketIO import socketio

app = Flask(__name__)
socketio.init_app(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template('Render_Compiler.html')

from static.services.init_socket import init_socket
init_socket()

if __name__ == '__main__':
    ui = FlaskUI(app=app, server="flask", width=800, height=600)
    socketio.run(app, host='0.0.0.0', port=5000)