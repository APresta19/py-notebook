"""
Example Hello World using flaskwebgui for Sprint 1.

General purpose: How to set up a simple Flask application and run it using flaskwebgui.
"""

from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    ui = FlaskUI(app=app, server="flask", width=800, height=600)
    ui.run()