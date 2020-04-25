"""
Database Connection
===================
"""
from dataclasses import dataclass
from math import cos, sin, asin, radians, sqrt
from random import random
from sqlite3 import connect
from os import path
from typing import Optional
from configparser import ConfigParser

from trivia_generator import TUnit
from flask_login import UserMixin
from trivia_generator.TUnit import TUnit
from trivia_generator.web_scraper import Article


@dataclass
class DBUser(UserMixin):
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

    DB_CONFIG_FILE: str = "db.ini"
    db_filename: str = None
    max_importance: float = None
    search_radius: float = None

    def __init__(self, filename=None, search_radius=None):
        local_path = path.dirname(path.abspath(__file__))
        config_filepath = path.join(local_path, DBConn.DB_CONFIG_FILE)
        config = ConfigParser()
        config.read(config_filepath)
        self.db_filename = local_path + '/' + (config['DATABASE']['DatabaseFile'] if filename is None else filename)
        self.search_radius = float(config['DATABASE']['SearchRadius']) if search_radius is None else search_radius

    @staticmethod
    def _distance(lat: float, long: float, query_lat: float, query_long: float):
        if lat is None or long is None:
            return -1
        lat = radians(lat)
        long = radians(long)
        query_lat = radians(query_lat)
        query_long = radians(query_long)
        d_lon = query_long - long
        d_lat = query_lat - lat
        a = sin(d_lat / 2) ** 2 + cos(lat) * cos(query_lat) * sin(d_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 3956
        return c * r

    def _select_lat_long(self, zip_code: str) -> tuple:
        db = connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT lat, long
                FROM location
                WHERE zip = ?
                """
        cursor.execute(query, (zip_code,))
        lat_long = cursor.fetchone()
        db.close()
        return lat_long if lat_long is not None else (None, None)

    def select_max_importance(self) -> float:
        """Gets the max importance score of the category with the maximum importance score, if not yet recorded.
        """
        if self.max_importance is None:
            db = connect(self.db_filename)
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
        db = connect(self.db_filename)
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
        db = connect(self.db_filename)
        cursor = db.cursor()

        min_select_importance = random() * self.select_max_importance()

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

        db = connect(self.db_filename)
        cursor = db.cursor()
        min_select_importance = random() * self.select_max_importance()

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
        :raises: DatabaseError
        :returns: the list of strings representing the names of the categories.
        :rtype: [str]
        """
        db = connect(self.db_filename)
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
        :raises: DatabaseError
        :returns: the list of article_ids associated with that category.
        :rtype: [(int, str)]
        """
        db = connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT DISTINCT a.article_id, a.title
                FROM article_category ac
                    JOIN category c ON ac.category_id = c.category_id
                    JOIN article  a ON ac.article_id = a.article_id
                WHERE c.name LIKE ?;
                """
        cursor.execute(query, ('%' + category + '%',))
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
        :raises: DatabaseError
        :return: database user_id
        :rtype: int
        """
        db = connect(self.db_filename)
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
        :raises: DatabaseError
        :return: database user_id or -1 if user not found
        :rtype: int
        """
        db = connect(self.db_filename)
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

    def select_password(self, username: str) -> str:
        """
        Retrieves a password entry from the database for the specified user

        :param username: user's username
        :type username: str
        :raises: sqlite3.DatabaseError
        :return: password entry
        """
        db = connect(self.db_filename)
        query = '''
        SELECT password
        FROM user
        WHERE username = ?
        '''
        password = db.cursor().execute(query, (username,)).fetchone()[0]
        db.close()
        return password

    def update_password(self, username: str, password: str) -> int:
        """ Updates a user in the database.

        :param username: the DBUser object to be added to the database
        :type username: str
        :param password: new password
        :type password: str
        :raises: DatabaseError
        :return: database user_id or -1 if user not found
        :rtype: int
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        :returns: an object representing a player or None
        :rtype: DBUser or None
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        :returns: t_unit_Id or -1 of not found
        :rtype: int
        """
        db = connect(self.db_filename)
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

        :raises DatabaseError:
        :returns: an object representing a TUnit
        :rtype: TUnit
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        :returns: a list of TUnit objects
        :rtype: [TUnit] or empty list if category not found
        """
        db = connect(self.db_filename)
        cursor = db.cursor()
        query = """
                SELECT DISTINCT sentence, tu.article_id, url, access_timestamp, t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit tu
                JOIN article_category ac on tu.article_id = ac.article_id
                JOIN category c on ac.category_id = c.category_id
                WHERE c.name LIKE ?
                """
        cursor.execute(query, ('%' + category + '%',))
        t_unit_list = [TUnit(*t_unit_tuple) for t_unit_tuple in cursor.fetchall()]
        db.close()
        return t_unit_list

    def select_tunit_location(self, zip_code: str) -> list:
        """Gets a list of TUnits from the database by location.

        :raises DatabaseError:
        :returns: a list of TUNit objects
        :rtype: [TUnit] or empty list if not found
        """
        lat, long = self._select_lat_long(zip_code)
        db = connect(self.db_filename)
        db.create_function('DISTANCE', 4, DBConn._distance)
        cursor = db.cursor()
        query = '''
                SELECT sentence, article_id, url, access_timestamp, tu.t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit tu
                JOIN (
                    SELECT t_unit_Id, DISTANCE(lat, long, ?, ?) d
                    FROM t_unit
                    WHERE d < ? AND d >= 0
                ) l ON tu.t_unit_Id = l.t_unit_Id
                '''
        cursor.execute(query, (lat, long, self.search_radius))
        t_unit_list = [TUnit(*t_unit_tuple) for t_unit_tuple in cursor.fetchall()]
        db.close()
        return t_unit_list

    def delete_tunit(self, t_unit: TUnit):
        """Deletes a TUnit from the database.

        :param t_unit: a TUnit object to be deleted from database
        :type t_unit: TUnit
        :raises DatabaseError:
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        :returns: the category id
        :rtype: int
        """
        db = connect(self.db_filename)
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
        :raises DatabaseError:
        """
        db = connect(self.db_filename)
        cursor = db.cursor()
        query = """
                DELETE FROM category
                WHERE category.name = ?
                """
        cursor.execute(query, (category,))
        db.commit()
        db.close()

    def select_articles_location(self, zip_code: str) -> list:
        """ Retrieves Articles from the database based on a location


        :raises DatabaseError:
        :returns: a list of tuples representing an article id and title
        :rtype: [(int, str)]
        """
        lat, long = self._select_lat_long(zip_code)
        db = connect(self.db_filename)
        db.create_function('DISTANCE', 4, DBConn._distance)
        cursor = db.cursor()
        query = """
                SELECT a.article_id, a.title
                FROM article a
                JOIN (
                    SELECT article_id, DISTANCE(lat, long, ?, ?) d
                    FROM article
                    WHERE d < ? AND d >= 0
                ) l ON a.article_id = l.article_id
                """
        cursor.execute(query, (lat, long, self.search_radius))
        article_list = cursor.fetchall()
        db.close()
        return article_list
