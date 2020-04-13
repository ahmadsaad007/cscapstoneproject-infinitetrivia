import sys
import os

from flask import Flask
from flask_socketio import SocketIO

# Handle import junk
top_level_dir = os.path.abspath('../')
# include trivia generator modules
sys.path.append(top_level_dir)

app = Flask(__name__)
socketio = SocketIO(app)
games = dict()

from app import routes
from app import game_models
from app import socket
