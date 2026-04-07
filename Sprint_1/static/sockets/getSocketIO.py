from flask_socketio import SocketIO
from flask import Flask
from localStoragePy import localStoragePy


app = Flask(__name__)
socketio = SocketIO()
localStorage = localStoragePy('pynotebook-namespace', 'text')