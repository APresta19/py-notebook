"""
Question storage module for Sprint 1.

General purpose: This module provides a simple in-memory storage mechanism for questions. 
It allows adding, retrieving, and listing questions.

Classes:
- QuestionStorage: A class that manages the storage of questions.

Functions:
TBD

"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

