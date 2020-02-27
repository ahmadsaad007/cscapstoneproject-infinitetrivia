from dataclasses import dataclass
from Player import Player
from GameSettings import GameSettings


@dataclass
class Game:
    """Class for a running instance of a game session. Contains All Game
    Logic.

    :param players: A list of the currently active players in the game.
    :param game_settings: A *GameSettings* object which contains the settings of the game.
    :param round_number: the current round number the game is on.
    :param game_code: the game code used to connect to the game.
    :param current_state: the current state of the game.
    :param game_states: a list of all possible game states.
    :param game_room: the ID of the game room used by connecting sockets.
    :param trivia_database: the database containing trivia questions.
    """
    players: list
    game_settings: GameSettings
    round_number: int
    game_code: str
    current_state: str
    game_states: list
    game_room: int
    #  trivia_database: database

    def add_player_to_lobby(player: Player) -> bool:
        """Adds a player to the current game lobby.
        :param player: the player to be added to the game lobby
        :type player: Player
        :returns: True if player was successfully added to lobby, False otherwise
        :rtype: bool
        """
        pass

    def remove_player_from_lobby(player: Player) -> bool:
        """Removes a player from the current game lobby.
        :param player" the player to be removed from the game lobby
        :type player: Player
        :returns: True if player was successfully removed from lobby, False otherwise
        :rtype: bool
        """
        pass

    def start_game() -> bool:
        """Finalizes the lobby and begins a game session.
        :returns: True if the game session was successfully started, false otherwise
        :rtype: bool
        """
        pass

    def display_score() -> bool:
        """Sends instructions to front end to display score information to the host screen and player(s).
        :returns: True if score information was successfully sent to front end, false otherwise
        :rtype: bool
        """
        pass

    def present_trivia() -> bool:
        """Sends the next trivia question to the front end, so it can be displayed on host scren.
        :returns: True if trivia question was properly fetched and sent to front end, False otherwise
        :rtype: bool
        """
        pass

    def get_next_trivia() -> bool:
        """Fetches a trivia question for the upcoming round from the trivia database, based on the current GameSettings.
        :returns: True if trivia question was properly fetched from database, False otherwise
        :rtype: bool
        """
        pass

    def display_category_options() -> bool:
        """If applicable (depending on game mode), send a list of possible categories that a player can choose from to the front end, which will be displayed to the selected user.
        :returns: True if categories were properly fetched from database and sent to frontend, False otherwise
        :rtype: bool
        """
        pass

    def fetch_response() -> bool:
        """Fetches the answers to a trivia question from each player from the front end.
        :returns: True if all answers were fetched from front-end.
        :rtype: bool
        """
        pass

    def display_winner() -> bool:
        """Send information about the winner of a game session to the front end.
        :returns: True if info about winner was successfully sent to frontend, false otherwise.
        :rtype: bool
        """
        pass

    def display_winners_of_round() -> bool:
        """Send information about the winner(s) of the round to the front end. 
        :returns: True if info about winner(s) of the round was successfully sent to frontend, False otherwise.
        :rtype: bool
        """
        pass

    def determine_winners_of_round():
        """Based of off the current trivia and the received answers from each player, determine who won the round.
        """
        pass

    def update_state():
        """Updates the current state of the game. 
        """
        pass

    def prompt_for_lie() -> bool:
        """If applicable (depending on game mode), tell front-end to prompt all player(s) for a fake-answer to a trivia question.
        :returns: True if info was successfully sent to front-end, False otherwise
        :rtype: bool
        """
        pass

    def finish_game() -> bool:
        """After all rounds have been completed, sents "credits" information to front-end and updates statistics for all registered users.
        :returns: True if info was successfully sent to front-end and user statistics were updated, false otherwise
        :rtype: bool
        """
        pass
