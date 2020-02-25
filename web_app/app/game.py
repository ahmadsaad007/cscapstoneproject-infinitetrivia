from dataclasses import dataclass
from Player import Player


@dataclass
class Game:
    """Class for a running instance of a game session. Contains All Game
    Logic.

    """
    players: list
    game_mode: str
    game_settings:
    round_number: int
    room_code: str
    current_state: str
    game_states: list
    room_socket

    def add_player_to_lobby(player: Player):
        """Adds a player to the current game lobby.
        
        """
