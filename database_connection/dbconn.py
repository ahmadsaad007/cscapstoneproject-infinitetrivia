"""
Database Connection
===================
"""
from dataclasses import dataclass
import random
import sqlite3

from trivia_generator.TUnit import TUnit
from typing import Optional


@dataclass
class DBUser:
    user_id: int = None
    username: str = None
    email: str = None
    wins: int = 0
    losses: int = 0
    num_answered: int = 0
    num_answered_correct: int = 0

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


@dataclass
class DBConn:
    """
    Class representing a database connection.
    """

    DB_CONFIG_FILE: str = "db.cfg"
    db_filename: str = None

    def __init__(self, filename=None):
        if filename is None:
            with open(DBConn.DB_CONFIG_FILE, "r") as file:
                self.db_filename = file.read().split("=")[1]
        else:
            self.db_filename = filename

    def select_max_importance(self) -> float:
        """Gets the max importance score of the category with the maximum importance score, if not yet recorded.
        """
        if self.max_importance is None:
            db = sqlite3.connect(self.db_filename)
            cursor = db.cursor()
            cursor.execute('SELECT MAX(importance) FROM category;')
            row = cursor.fetchone()
            self.max_importance = row[0]
            db.close()
        return self.max_importance

    def select_random_article(self) -> tuple:
        """Selects a random article from the database.

        returns: the article id and title of the random article.
        rtype: (int, str)
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        cursor.execute('SELECT article_id, title FROM article ORDER BY random() LIMIT 1;')
        article_id, title = cursor.fetchone()
        db.close()
        return article_id, title

    def select_weighted_random_article(self) -> tuple:
        """Selects a random article from the database weighted by its importance score.

        returns: the article id and title of the random article.
        rtype: (int, str)
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()

        min_select_importance = random.random() * self.select_max_importance()

        query = """
                SELECT article.article_id, article.title, SUM(importance) AS article_importance
                FROM article_category
                    JOIN article ON article.article_id = article_category.article_id
                    JOIN category ON category.category_id = article_category.category_id
                GROUP BY article.article_id
                HAVING SUM(importance) > ?
                ORDER BY RANDOM()
                LIMIT 1;
                """

        cursor.execute(query, [min_select_importance])
        article_id, title, importance = cursor.fetchone()
        db.close()
        return article_id, title, importance

    def select_random_category(self) -> tuple:
        """Selects a random category from the database weighted by its importance score.

        returns: the category id, name, and importance of the category.
        """

        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        min_select_importance = random.random() * self.select_max_importance()

        # Get a random category whose importace score is above min_select_importance
        query = """
                SELECT category_id, name, importance
                FROM category
                WHERE importance >= ?
                ORDER BY RANDOM()
                LIMIT 1;"""
        cursor.execute(query, [min_select_importance])
        row = cursor.fetchone()
        db.close()
        return row

    def select_article_categories(self, article_id: int) -> list:
        """Selects the categories associated with the article with the given article id.

        :param article_id: The ID of the article.
        :type article_id: int
        :raises: sqlite3.DatabaseError
        :returns: the list of strings representing the names of the categories.
        :rtype: [str]
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT name
                FROM article_category
                    JOIN category ON article_category.category_id = category.category_id
                WHERE article_id = ?;
                """
        cursor.execute(query, (article_id,))
        rows = cursor.fetchall()
        db.close()
        return [row[0] for row in rows]

    def select_category_articles(self, category: str) -> list:
        """Selects the categories associated with the article with the given article id.

        :param category: category name.
        :type category: int
        :raises: sqlite3.DatabaseError
        :returns: the list of article_ids associated with that category.
        :rtype: [(int, str)]
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT article.article_id, article.title
                FROM article_category
                    JOIN category ON article_category.category_id = category.category_id
                    JOIN article ON article_category.article_id = article.article_id
                WHERE name = ?;
                """
        cursor.execute(query, (category,))
        rows = cursor.fetchall()
        db.close()
        return rows

    def insert_user(self, user: DBUser, password: str) -> int:
        """
        Inserts a user into the database

        :param user: the DBUser object to be added to the database
        :type user: DBUser
        :param password: the user's password
        :type password: str
        :raises: sqlite3.DatabaseError
        :return: database user_id
        :rtype: int
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO user (username, email, password, wins, losses, num_answered, num_answered_correct)
        VALUES (?,?,?,?,?,?,?)
        """
        cursor.execute(query, (
            user.username,
            user.email,
            password,
            user.wins,
            user.losses,
            user.num_answered,
            user.num_answered_correct))
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return user_id

    def update_user(self, user: DBUser) -> int:
        """ Updates a user in the database.

        :param user: the DBUser object to be added to the database
        :type user: DBUser
        :raises: sqlite3.DatabaseError
        :return: database user_id or -1 if user not found
        :rtype: int
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                UPDATE user
                SET username = ?, email = ?, wins = ?, losses = ?, num_answered = ?, num_answered_correct = ?
                WHERE username = ?
                """
        cursor.execute(query, (
            user.username,
            user.email,
            user.wins,
            user.losses,
            user.num_answered,
            user.num_answered_correct,
            user.username
        ))
        db.commit()
        query = """
                SELECT user_id
                FROM user
                WHERE username = ?
                """
        user_id = cursor.execute(query, (user.username,)).fetchone()
        db.close()
        if user_id is None:
            return -1
        else:
            return user_id[0]

    def update_password(self, username: str, password: str) -> int:
        """ Updates a user in the database.

        :param username: the DBUser object to be added to the database
        :type username: str
        :param password: new password
        :type password: str
        :raises: sqlite3.DatabaseError
        :return: database user_id or -1 if user not found
        :rtype: int
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                UPDATE user
                SET password = ?
                WHERE username = ?
                """
        cursor.execute(query, (password, username))
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        if user_id == 0:
            return -1
        else:
            return user_id

    def select_user(self, username: str) -> Optional[DBUser]:
        """Gets a user from the database by username.

        :param username: username to be retrieved
        :type username: str
        :raises sqlite3.DatabaseError:
        :returns: an object representing a player or None
        :rtype: DBUser or None
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT user_id, username, email, wins, losses, num_answered, num_answered_correct
                FROM user
                WHERE username = ?;
                """
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        db.close()
        if user is not None:
            return DBUser(*user)
        else:
            return None

    def delete_user(self, user: DBUser) -> None:
        """Deletes a user from the database.

        :param user: a users's object to be deleted from database
        :type user: DBUser
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                DELETE FROM user
                WHERE username = ?
                """
        cursor.execute(query, (user.username,))
        db.commit()
        db.close()

    def update_tunit(self, t_unit: TUnit) -> int:
        """Updates a TUnit in the database.

        :param t_unit: a TUnit object to be deleted from database
        :type t_unit: TUnit
        :raises sqlite3.DatabaseError:
        :returns: t_unit_Id or -1 of not found
        :rtype: int
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                REPLACE INTO t_unit (t_unit_Id, sentence, article_id, url, access_timestamp, lat, long, num_likes,
                    num_mehs, num_dislikes)
                VALUES (?,?,?,?,?,?,?,?,?,?);
                """
        cursor.execute(query,
                       (t_unit.t_unit_id, t_unit.sentence, t_unit.article_id, t_unit.url, t_unit.access_timestamp,
                        t_unit.latitude, t_unit.longitude, t_unit.num_likes, t_unit.num_mehs, t_unit.num_dislikes))
        db.commit()
        t_unit.t_unit_id = cursor.lastrowid
        db.close()
        return t_unit.t_unit_id

    def select_tunit_random(self) -> TUnit:
        """Gets a TUnit from the database by random.

        :raises sqlite3.DatabaseError:
        :returns: an object representing a TUnit
        :rtype: TUnit
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT sentence, article_id, url, access_timestamp, t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit
                ORDER BY RANDOM() LIMIT 1;
                """
        cursor.execute(query)
        tunit = TUnit(*cursor.fetchone())
        db.close()
        return tunit

    def select_tunit_category(self, category: str) -> list:
        """Gets a list of TUnits from the database by category.

        :param category: the category used to to find TUnits
        :type category: str
        :raises sqlite3.DatabaseError:
        :returns: a list of TUnit objects
        :rtype: [TUnit] or empty list if category not found
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT  sentence, tu.article_id, url, access_timestamp, t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit tu
                JOIN article_category ac on tu.article_id = ac.article_id
                JOIN category c on ac.category_id = c.category_id
                WHERE c.name = ?
                """
        cursor.execute(query, (category,))
        t_unit_list = [TUnit(*t_unit_tuple) for t_unit_tuple in cursor.fetchall()]
        db.close()
        return t_unit_list

    def select_tunit_location(self, lat: float, long: float) -> list:
        """Gets a list of TUnits from the database by location.

        :param lat: a latitude coordinate
        :type lat: float
        :param long: a longitudinal coordinate
        :type long: float
        :raises sqlite3.DatabaseError:
        :returns: a list of TUNit objects
        :rtype: [TUnit] or empty list if not found
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT sentence, article_id, url, access_timestamp, t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit
                WHERE lat > ? - 0.5 AND lat < ? + 0.5
                AND 
                long > ? - 0.5 AND long < ? + 0.5
                """
        cursor.execute(query, (lat, lat, long, long))
        t_unit_list = [TUnit(*t_unit_tuple) for t_unit_tuple in cursor.fetchall()]
        db.close()
        return t_unit_list

    def delete_tunit(self, t_unit: TUnit):
        """Deletes a TUnit from the database.

        :param t_unit: a TUnit object to be deleted from database
        :type t_unit: TUnit
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                DELETE FROM t_unit
                WHERE t_unit_Id = ?
                """
        cursor.execute(query, (t_unit.t_unit_id,))
        db.commit()
        db.close()

    def insert_category(self, category: str, importance: float) -> int:
        """Adds a category to the database.

        :param category: the category to be added to the database
        :type category: str
        :param importance: relevance of category
        :type importance: float
        :raises sqlite3.DatabaseError:
        :returns: the category id
        :rtype: int
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                INSERT INTO category (name, importance) 
                VALUES (?,?)        
                """
        cursor.execute(query, (category, importance))
        db.commit()
        category_id = cursor.lastrowid
        db.close()
        return category_id

    def delete_category(self, category: str):
        """Deletes a category from the database.

        :param category: the category to be deleted from the database
        :type category: str
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                DELETE FROM category
                WHERE category.name = ?
                """
        cursor.execute(query, (category,))
        db.commit()
        db.close()

    def select_articles_location(self, lat: float, long: float) -> list:
        """ Retrieves Articles from the database based on a location

        :param lat: the latitude coordinate
        :type lat: float
        :param long: the longitudinal coordinate
        :type long: float
        :raises sqlite3.DatabaseError:
        :returns: a list of tuples representing an article id and title
        :rtype: [(int, str)]
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT a.article_id, title
                FROM article a
                JOIN t_unit tu on a.article_id = tu.article_id
                WHERE tu.lat > ? - 0.5 AND tu.lat < ? + 0.5 AND
                tu.long > ? - 0.5 AND tu.long < ? + 0.5
                """
        cursor.execute(query, (lat, lat, long, long))
        article_list = cursor.fetchall()
        db.close()
        return article_list
