"""
Game Settings
=============
"""

from dataclasses import dataclass


@dataclass
class GameSettings:
    """Class which holds the settings of a current game instance.
    
    :param game_mode: the type of game that will be played.
    :param topic: If *game_mode* involves categories, the general category of the game.
    :param max_players: the maximum number of players allowed to join the game.
    :param number_of_rounds: the number of rounds to be played for a given game.
    :param response_timer: how long players have, in seconds, to answer a question before timing out.
    """

    topic: str
    game_mode: str
    max_players: int
    number_of_rounds: int
    response_timer: int
