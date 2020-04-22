"""
Game Settings
=============
"""


class GameSettings:
    """Class which holds the settings of a current game instance.
    
    :param game_mode: the type of game that will be played.
    :param topic: If *game_mode* involves categories, the general category of the game.
    :param max_players: the maximum number of players allowed to join the game.
    :param number_of_rounds: the number of rounds to be played for a given game.
    :param response_timer: how long players have, in seconds, to answer a question before timing out.
    """
    # def __init__(self, game_mode, category="", zip_code="", topic=None,
    #              max_players=10, number_of_rounds=10, response_timer=30):
    #     self.game_mode = game_mode
    #     self.topic = topic
    #     self.max_players = max_players
    #     self.number_of_rounds = number_of_rounds
    #     self.response_timer = response_timer

    def __init__(self, game_options):
        self.game_mode = game_options['mode']
        if self.game_mode == 'location':
            self.zip_code = game_options['zip_code']
            print('zip code:', self.zip_code)
        elif self.game_mode == 'category':
            self.category = game_options['category']
            print('category:', self.category)
        self.topic = None
        self.max_players = 10
        self.number_of_rounds = 10
        self.response_timer = 30
