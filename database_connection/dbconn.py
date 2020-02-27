from dataclasses import dataclass
from web_app.app import Player
from trivia_generator import TUnit
from typing import List
import sqlite3


@dataclass
class DBConn:

    """Database utilities

        :param DBFile: the name of the SQLite database file. Will be fetched at runtime from database config file.

    """

    DBFile: str = None

    def update_user(self, user: Player):
        """Adds or updates a user in the database

        :param user: the Player object to be added to the database
        :type user: Player
        :raises: sqlite3.DatabaseError
        """
        pass

    def get_user(self, username: str) -> Player:
        """Gets a user from the database by username

        :param username: username to be retrieved
        :type username: str
        :raises sqlite3.DatabaseError:
        :returns: an object representing a player
        :rtype: Player
        """
        pass

    def delete_user(self, user: Player):
        """Deletes a user from the database

        :param user: a Player object to be deleted from database
        :type user: Player
        :raises sqlite3.DatabaseError:
        """
        pass

    def update_tunit(self, tunit: TUnit):
        """Adds or updates a TUnit in the database

        :param tunit: a TUnit object to be deleted from databse
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        pass

    def get_tunit_random(self) -> TUnit:
        """Gets a TUnit from the database by random

        :raises sqlite3.DatabaseError:
        :returns: an object representing a TUnit
        :rtype: TUnit
        """
        pass

    def get_tunit_category(self, category: str) -> List[TUnit]:
        """Gets a list of TUnits from the database by category

        :param category: the category used to to find TUnits
        :type category: str
        :raises sqlite3.DatabaseError:
        :returns: a list of TUNit objects
        :rtype: List[TUnit]
        """
        pass

    def get_tunit_location(self, lat: float, long: float) -> List[TUnit]:
        """Gets a list of TUnits from the database by location

        :param lat: a latitude coordinate
        :type lat: float
        :param long: a longitudinal coordinate
        :type long: float
        :raises sqlite3.DatabaseError:
        :returns: a list of TUNit objects
        :rtype: List[TUnit]
        """
        pass

    def delete_tunit(self, tunit: TUnit):
        """Deletes a user from the database

        :param tunit: a TUnit object to be deleted from database
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        pass

    def add_question(self, question: str, tunit: TUnit):
        """Adds a question entry in the database

        :param question: the question text to be added
        :type question: str
        :param tunit: the TUnit the question is associated with
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        pass

    def get_questions(self, tunit: TUnit) -> List[(str, str)]:
        """Gets a list of questions associated with a TUnit

        :param tunit: the TUnit to retrieve questions from
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        :return: a list of tuple representions of a question and its answer
        :rtype: List[(str, str)]
        """
        pass

    def delete_question(self, question: str, tunit: TUnit):
        """Deletes a question from the database

        :param question: the question text to be deleted
        :type question: str
        :param tunit: the TUnit the question is associated with
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        pass

    def add_category(self, category: str):
        """Adds a category to the database

        :param category: the category to be added to the database
        :type category: str
        :raises sqlite3.DatabaseError:
        """
        pass

    def delete_category(self, category: str):
        """Deletes a category from the database

        :param category: the category to be deleted from the database
        :type category: str
        :raises sqlite3.DatabaseError:
        """
        pass

    def add_vote(self, user: Player, question: str, interesting_rating: int, question_rating: int):
        """Adds a quality vote associated with a user and a question

        :param user: the user who generated the vote
        :type user: Player
        :param question: the question the user voted on
        :type question: str
        :param interesting_rating: the rating of how interesting the trivia was
        :type interesting_rating: int
        :param question_rating: the rating of understandable the question was
        :type question_rating: int
        :raises sqlite3.DatabaseError:
        """
        pass
