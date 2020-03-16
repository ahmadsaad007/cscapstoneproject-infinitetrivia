from app import socketio, games
from app.game_models.Game import Game
from app.game_models.Player import Player
from flask import request


@socketio.on('create_game')
def create_game(game_options):
    # TODO: potentially create game code server side instead of client side?
    code = game_options['code']
    # create new Game object and add to game dict
    game = Game(code, None, request.sid)
    games[code] = game
    return game_options['code']


@socketio.on('join_game')
def join_game(data):
    player = Player(name=data['name'],
                    ID=request.sid,
                    connected=True,
                    current_score=0,
                    is_registered=False)  # TODO
    code = data['code']
    games[code].add_player_to_lobby(player)
