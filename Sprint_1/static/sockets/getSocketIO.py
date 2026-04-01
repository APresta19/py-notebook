from flask_socketio import SocketIO
from flask import Flask
from localStoragePy import localStoragePy


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
localStorage = localStoragePy('pynotebook-namespace', 'text')

socketio = SocketIO()