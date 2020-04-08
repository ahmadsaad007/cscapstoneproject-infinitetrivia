from app import socketio, games
from app.game_models.Game import Game
from app.game_models.Player import Player
from app.validations import is_game_code_valid
from app.validations import is_game_name_valid
from flask import request
from flask_socketio import join_room


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
                    is_registered=False,  # TODO
                    current_answer="")
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
    socketio.emit('display_text_response_prompt', room=code)


@socketio.on('submit_answer')
def submit_answer(data):
    code = data['code']
    # TODO validate answer
    print("got answer:", data['answer'])
    data['sid'] = request.sid
    return games[code].submit_answer(data)


@socketio.on('answer_timeout')
def answer_timeout(code):
    socketio.emit('answer_timeout', room=code)


@socketio.on('get_answers')
def get_answers(code):
    print("got request for trivia answers")
    game = games[code]
    data = game.get_trivia_answer_and_responses()
    return data


@socketio.on('submit_trivia_rank')
def submit_trivia_rank(data):
    code = data['code']
    game = games[code]
    game.submit_trivia_rank(data['rank'])
    return True
