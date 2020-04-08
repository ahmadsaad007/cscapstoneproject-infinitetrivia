import sys
import os

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager

# Handle import junk
top_level_dir = os.path.abspath('../')
# include trivia generator modules
sys.path.append(top_level_dir)

app = Flask(__name__)
socketio = SocketIO(app)
games = dict()

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

from app import login_validation
from app import routes
from app import game_models
from app import socket
#from app.login_validation import User
from app.login_validation import auth

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app#
#app.register_blueprint(auth_blueprint)
