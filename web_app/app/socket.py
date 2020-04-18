import random

from app import socketio, games
from app.game_models.Game import Game
from app.game_models.Player import Player
from app.game_models.GameSettings import GameSettings
from app.validations import is_game_code_valid
from app.validations import is_game_name_valid
from flask import request
from flask_socketio import join_room


@socketio.on('create_game')
def create_game(game_options):
    # TODO: potentially create game code server side instead of client side?
    code = game_options['code']
    # create game mode object
    settings = GameSettings(game_options['code'])
    # create new Game object and add to game dict
    game = Game(code, settings, request.sid)
    games[code] = game
    return game_options['code']


@socketio.on('join_game')
def join_game(data):
    code = data['code']
    name = data['name']
    print(name, " attempting to join game")
    if not is_game_code_valid(code):
        print("error: ", code, " is bad code")
        return "ERR_INVALID_CODE"
    if not is_game_name_valid(code, name):
        print("error: ", name, " is an invalid name")
        return "ERR_INVALID_NAME"
    player = Player(name=name,
                    ID=request.sid,
                    connected=True,
                    current_score=0,
                    number_fooled=0,
                    is_registered=False,  # TODO
                    current_answer="",
                    current_lie="")
    game = games[code]
    if not game.add_player_to_lobby(player):
        print("error: could not join")
        return "ERR_COULD_NOT_JOIN"
    else:
        socketio.emit("add_player_to_lobby", name, room=game.host_id)
        print("added player to lobby!")
        join_room(code)
        return "ADDED_TO_LOBBY"


@socketio.on('disconnect')
def on_disconnect():
    print("disconnected!")
    sid = request.sid
    for game in games.values():
        ls = [player for player in game.players if player.ID == sid]
        if len(ls) != 0:
            print(ls[0].name, "leaving game ", game.host_id)
            socketio.emit("remove_player_from_lobby", ls[0].name, room=game.host_id)
            break


@socketio.on('start_game')
def start_game(code):
    game = games[code]
    game.start_game()
    data = game.get_score()
    round_number = game.get_round_number()
    socketio.emit("display_splash_screen", round_number, room=code)
    return data


@socketio.on('request_scores')
def request_scores(code):
    game = games[code]
    scores = game.get_score()
    print("got request for scores!")
    print(scores)
    round_number = game.get_round_number()
    socketio.emit('display_splash_screen', round_number, room=code)
    return scores


@socketio.on('request_trivia')
def request_trivia(code):
    print("got a trivia request from game ", code)
    return games[code].get_next_trivia()


@socketio.on('prompt_response')
def prompt_response(code):
    print("prompting for response")
    socketio.emit('display_text_response_prompt', "answer", room=code)


@socketio.on('prompt_fibbage_response')
def prompt_fibbage_response(code):
    print("prompting for fibbage response")
    game = games[code]
    data = game.get_fibbage_lies_and_answer()
    answer_list = data['lies']
    answer_list.append(data['answer'])
    random.shuffle(answer_list)
    socketio.emit('display_fibbage_response_prompt', answer_list, room=code)


@socketio.on('prompt_lie')
def prompt_lie(code):
    print("prompting for lies")
    socketio.emit('display_text_response_prompt', "lie", room=code)


@socketio.on('submit_answer')
def submit_answer(data):
    code = data['code']
    game = games[code]
    print("got answer:", data['answer'])
    data['sid'] = request.sid
    return_val = game.submit_answer(data)
    if return_val[1] is True:
        print('all players are in')
        socketio.emit('all_players_in', room=game.host_id)
    return return_val[0]


@socketio.on('submit_lie')
def submit_lie(data):
    code = data['code']
    game = games[code]
    print("got lie:", data['lie'])
    data['sid'] = request.sid
    return_val = game.submit_lie(data)
    if return_val[1] is True:
        print('all players have lied')
        socketio.emit('all_lies_in', room=game.host_id)
    return return_val[0]


@socketio.on('answer_timeout')
def answer_timeout(code):
    socketio.emit('answer_timeout', room=code)


@socketio.on('get_answers')
def get_answers(code):
    print("got request for trivia answers")
    game = games[code]
    data = game.get_trivia_answer_and_responses()
    # prompt users for trivia rank once answer is displayed
    socketio.emit('prompt_trivia_rank', room=code)
    return data


@socketio.on('get_fibbage_answer_and_responses')
def get_lies_and_answer(code):
    print("got request for fibbage lies and answer")
    game = games[code]
    data = game.get_fibbage_answer_and_responses()
    return data


@socketio.on('submit_trivia_rank')
def submit_trivia_rank(data):
    code = data['code']
    game = games[code]
    game.submit_trivia_rank(data['rank'])
    return True
