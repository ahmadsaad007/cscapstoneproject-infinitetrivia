from app import socketio
from flask import request



@socketio.on('create_game')
def create_game(game_options):
    # TODO: potentially create game code server side instead of client side?
    host_id = request.sid
    return game_options['code']


@socketio.on('join_game')
def join_game(data):
    player = data['player']
    code = data['code']
