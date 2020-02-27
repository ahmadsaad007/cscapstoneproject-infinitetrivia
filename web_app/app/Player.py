from dataclasses import dataclass


@dataclass
class Player:
    """Class which represents a player in a class.

    :param name: the chosen display-name of the Player.
    :param current_room: the current game room the player is in.
    :param connected: a boolean signifying whether the player is currently connected to a game.
    :param current_score: an integer representing the current score of the player.
    :param is_registered: a boolean which tells if the player is a registered user.
    :param ID: if the player is registered, the unique ID of the player.
    """

    name: str
    current_room: int
    connected: bool
    current_score: int
    is_registered: bool
    ID: int

    def get_name() -> str:
        """returns the name of the player.
        The name of the user is the currently registered name in the game session.
        :returns: the name of the user
        :rtype: str
        """
        pass

    def get_current_room() -> int:
        """returns the integer ID of the current room the player is in.
        :returns: the integer ID of the player's current room, or -1 if the player is no longer in a game room.
        :rtype: int
        """
        pass

    def is_connected() -> bool:
        """returns True if the player is currently connected to a game session.
        :returns: True if the player is currently connected, False otherwise
        :rtype: bool
        """
        pass

    def update_score(increment: int) -> bool:
        """Updates the current score of the player by *increment*.
        :param increment: the value the player's score should be incremented by
        :returns: True if the player's score was successfully updated, false otherwise.
        :rtype: bool
        """
        pass

    def get_current_score() -> int:
        """Returns the current score of the player.
        :returns: the current score of the player.
        :rtype: int
        """
        pass

    def update_statistics(game_settings, player_db_handle) -> bool:
        """Updates the Player's statistics stored in *player_db_handle* based off of *game_settings*.
        :param game_settings: the game settings of the current game.
        :param player_db_handle: a handle to the database storing registered Player statistics.
        :returns: True if the player database entry was sucessfully updated, False otherwise
        :rtype: bool
        """
        pass

    def is_registered() -> bool:
        """Returns a boolean indicating if the player is a registered user or not.
        :returns: True if the player is registered, False if not.
        :rtype: bool
        """
        pass

    def get_id() -> int:
        """Returns the unique ID of the user.
        :returns: the ID of the user, or -1 if the user does not have a valid ID.
        :rtype: bool
        """
        pass
