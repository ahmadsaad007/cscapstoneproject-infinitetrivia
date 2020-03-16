from app import games


def is_game_code_valid(game_code: str) -> bool:
    return game_code in games


def is_game_name_valid(game_code: str, name: str) -> bool:
    if name == "":
        return False
    game = games[game_code]
    return name not in [player.name for player in game.players]
