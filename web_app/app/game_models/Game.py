"""
Game
====
"""

from .Player import Player
from .GameSettings import GameSettings


class Game:
    """Class for a running instance of a game session. Contains All Game Logic.

    :param players: A list of the currently active players in the game.
    :param game_settings: A *GameSettings* object which contains the settings of the game.
    :param round_number: the current round number the game is on.
    :param game_code: the game code used to connect to the game.
    :param current_state: the current state of the game.
    :param game_states: a list of all possible game states.
    :param game_room: the ID of the game room used by connecting sockets.
    :param trivia_database: the database containing trivia questions.
    """
    # game_states: list

    def __init__(self, game_code: str,
                 game_settings: GameSettings,
                 host_id: str):
        self.players = []
        self.game_code = game_code
        self.game_settings = game_settings
        self.host_id = host_id
        self.round_number = 0
        self.current_state = "LOBBY"

    def add_player_to_lobby(self, player: Player) -> bool:
        """Adds a player to the current game lobby.

        :param player: the player to be added to the game lobby
        :type player: Player
        :returns: True if player was successfully added to lobby, False otherwise
        """
        pass

    def remove_player_from_lobby(self, player: Player) -> bool:
        """Removes a player from the current game lobby.

        :param player: the player to be removed from the game lobby
        :type player: Player
        :returns: True if player was successfully removed from lobby, False otherwise
        """
        pass

    def start_game(self) -> bool:
        """Finalizes the lobby and begins a game session.

        :returns: True if the game session was successfully started, false otherwise
        """
        pass

    def display_score(self) -> bool:
        """Sends instructions to front end to display score information to the host screen and player(s).

        :returns: True if score information was successfully sent to front end, false otherwise
        """
        pass

    def present_trivia(self) -> bool:
        """Sends the next trivia question to the front end, so it can be displayed on host screen.

        :returns: True if trivia question was properly fetched and sent to front end, False otherwise
        """
        pass

    def get_next_trivia(self) -> bool:
        """Fetches a trivia question for the upcoming round from the trivia database, based on the current GameSettings.

        :returns: True if trivia question was properly fetched from database, False otherwise
        """
        pass

    def display_category_options(self) -> bool:
        """If applicable (depending on game mode), send a list of possible categories that a player can choose from to the front end, which will be displayed to the selected user.

        :returns: True if categories were properly fetched from database and sent to frontend, False otherwise
        """
        pass

    def fetch_response(self) -> bool:
        """Fetches the answers to a trivia question from each player from the front end.

        :returns: True if all answers were fetched from front-end.
        """
        pass

    def display_winner(self) -> bool:
        """Send information about the winner of a game session to the front end.

        :returns: True if info about winner was successfully sent to frontend, false otherwise.
        """
        pass

    def display_winners_of_round(self) -> bool:
        """Send information about the winner(s) of the round to the front end. 

        :returns: True if info about winner(s) of the round was successfully sent to frontend, False otherwise.
        """
        pass

    def determine_winners_of_round(self):
        """Based of off the current trivia and the received answers from each player, determine who won the round.
        """
        pass

    def update_state(self):
        """Updates the current state of the game. 
        """
        pass

    def prompt_for_lie(self) -> bool:
        """If applicable (depending on game mode), tell front-end to prompt all player(s) for a fake-answer to a trivia question.

        :returns: True if info was successfully sent to front-end, False otherwise
        """
        pass

    def finish_game(self) -> bool:
        """After all rounds have been completed, sents "credits" information to front-end and updates statistics for all registered users.
        
        :returns: True if info was successfully sent to front-end and user statistics were updated, false otherwise
        """
        pass
