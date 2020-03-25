from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
games = dict()

from app import routes
from app import game_models
from app import socket
