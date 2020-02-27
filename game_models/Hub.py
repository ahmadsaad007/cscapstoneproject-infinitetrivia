"""
Hub
===
"""

from dataclasses import dataclass, field


@dataclass
class Hub:
    """Backend hub which serves static html pages and connects users to games.

    :param games: a dictionary of games, with each corresponding game's game-code as the key.
    :param num_games: the current number of active games.
    """

    games: dict = field(default_factory=dict)
    num_games: int = 0
    # player_database

    def create_game(self) -> str:
        """Creates a new game session and corresponding Game instance.

        :returns: a game code corresponding to the newly created Game instance, or the empty string if the game does not exist.
        :rval: str
        """
        pass

    def remove_game(self, game_code: str) -> bool:
        """Removes the game corresponding to *game_code* from the dictionary of active games.

        :returns: True if the game was successfully removed, False otherwise
        :rval: bool
        """
        pass

    def start_game(self, game_code: str) -> bool:
        """Starts the game corresponding to *game_code*.

        :returns: True if game was successfully started, False otherwise
        :rval: bool
        """
        pass

    def serve_front_page(self):
        """Serves the front page html to the front-end."""
        pass

    def serve_about_page(self):
        """Server the about page html to the front-end."""
        pass

    def serve_login_page(self):
        """Serve the login page html to the front-end."""
        pass

    def serve_create_page(self):
        """Serve the create game page html to the front-end."""
        pass

    def serve_join_game_page(self):
        """Serve the join game page html to the front-end."""

    def gen_gamecode(self) -> str:
        """Generates a unique gamecode string.

        :returns: a unique gamecode string
        :rtype: str
        """
        pass

    def login(self, credentials) -> bool:
        """Logs the user in, provided user *credentials*.

        :returns: True if the login was successful, False otherwise.
        :rtype: bool
        """
        pass

    def validate_credentials(self, credentials) -> bool:
        """Checks user *credentials* against the player database.

        :returns: True if the user provided credentials are valid, False otherwise.
        :rtype: bool
        """
        pass
