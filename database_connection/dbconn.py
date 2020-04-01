"""
Database Connection
===================
"""
from dataclasses import dataclass
import random
import sqlite3

from trivia_generator import TUnit
from typing import List, Optional
from trivia_generator.web_scraper import Article


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
        for variable in self.__dict__.keys():
            if self.__dict__[variable] != other.__dict__[variable]:
                return False
        return True


@dataclass
class DBConn:
    """
    Class representing a database connection.
    """

    DB_CONFIG_FILE: str = "db.cfg"
    db_filename: str = None
    max_importance: float = None

    def __init__(self, filename=None):
        if filename is None:
            with open(DBConn.DB_CONFIG_FILE, "r") as file:
                self.db_filename = file.read().split("=")[1]
        else:
            self.db_filename = filename

    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

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
        :returns: the list of strings representing the names of the categories.
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
        :returns: the list of article_ids associated with that category.
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
        :return: database user_id or -1 if not found
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
        query = """
        SELECT user_id
        FROM user
        WHERE username = ?
        """
        cursor.execute(query, (user.username,))
        user_id = cursor.fetchone()[0]
        db.close()
        return user_id

    def update_user(self, user: DBUser) -> int:
        """ Updates a user in the database.

        :param user: the DBUser object to be added to the database
        :type user: DBUser
        :raises: sqlite3.DatabaseError
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
        cursor.execute(query, (user.username,))
        rows = cursor.fetchone()
        if rows is not None:
            user_id = rows[0]
        else:
            user_id = -1
        db.close()
        print('stuff')
        return user_id

    def update_password(self, username: str, password: str) -> int:
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        UPDATE user
        SET password = ?
        WHERE username = ?
        """
        cursor.execute(query, (password, username))
        db.commit()
        db.close()

    def select_user(self, username: str) -> Optional[DBUser]:
        """Gets a user from the database by username.

        :param username: username to be retrieved
        :type username: str
        :raises sqlite3.DatabaseError:
        :returns: an object representing a player
        :rtype: Player
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

    # TODO(ALEX): fix tunit and question methods when format finalized

    def insert_tunit(self, tunit: TUnit) -> int:
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO t_unit (
            article_id, 
            sentence, 
            url, 
            access_timestamp,
            lat, 
            long, 
            num_likes,
            num_mehs,
            num_dislikes)
        VALUES (?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(query, (
            tunit.article_id,
            tunit.sentence,
            tunit.url,
            tunit.access_timestamp,
            tunit.latitude,
            tunit.longitude,
            tunit.num_likes,
            tunit.num_mehs,
            tunit.num_dislikes
        ))
        db.commit()
        query = """
        SELECT t_unit_Id
        FROM t_unit
        WHERE sentence = ?
        """
        cursor.execute(query, (tunit.sentence,))
        t_unit_id = cursor.fetchone()
        db.close()
        return t_unit_id

    def update_tunit(self, tunit: TUnit):
        """Updates a TUnit in the database.

        :param tunit: a TUnit object to be deleted from database
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        UPDATE t_unit
        SET sentence = ?,
            url = ?,
            access_timestamp = ?,
            lat = ?,
            long = ?,
            num_likes = ?,
            num_mehs = ?,
            num_dislikes = ?
        WHERE t_unit_Id = ?
        """
        cursor.execute(query, (
            tunit.sentence,
            tunit.url,
            tunit.access_timestamp,
            tunit.latitude,
            tunit.longitude,
            tunit.num_likes,
            tunit.num_mehs,
            tunit.num_dislikes
        ))
        db.commit()
        db.close()

    def select_tunit_random(self) -> TUnit:
        """Gets a TUnit from the database by random.

        :raises sqlite3.DatabaseError:
        :returns: an object representing a TUnit
        :rtype: TUnit
        """
        db = sqlite3.connect(self.db_filename)
        db.row_factory = self.__dict_factory
        cursor = db.cursor()
        query = """
        SELECT 
            t_unit_Id,
            article_id,
            sentence,
            url,
            access_timestamp,
            lat,
            long,
            num_likes,
            num_mehs,
            num_dislikes
        FROM t_unit
        ORDER BY RANDOM() LIMIT 1;
        """
        cursor.execute(query)
        tunit = cursor.fetchone()
        db.close()
        return tunit

    def select_tunit_category(self, category: str) -> list:
        """Gets a list of TUnits from the database by category.

        :param category: the category used to to find TUnits
        :type category: str
        :raises sqlite3.DatabaseError:
        :returns: a list of TUNit objects
        :rtype: List[TUnit]
        """
        db = sqlite3.connect(self.db_filename)
        db.row_factory = self.__dict_factory
        cursor = db.cursor()
        query = """
        SELECT 
            t_unit_Id,
            t.article_id,
            sentence,
            url,
            access_timestamp,
            lat,
            long,
            num_likes,
            num_mehs,
            num_dislikes
        FROM t_unit t
        JOIN article_category ac on t.article_id = ac.article_id
        JOIN category c on ac.category_id = c.category_id
        WHERE c.name = ?
        """
        cursor.execute(query, (category,))
        db_tunit = cursor.fetchone()

        # query = """
        # SELECT name
        # FROM category
        # JOIN article_category ac on category.category_id = ac.category_id
        # JOIN t_unit tu on ac.article_id = tu.article_id
        # WHERE tu.article_id = ?
        # """
        # cursor.execute(query, (db_tunit["article_id"],))
        # categories = []
        # for row in cursor.fetchall():
        #     categories.append(row["name"])

        db.close()
        return TUnit(
            db_tunit["sentence"],
            db_tunit["article_id"],
            db_tunit["url"],
            db_tunit["access_timestamp"],
            db_tunit["t_unit_Id"],
            db_tunit["lat"],
            db_tunit["long"],
            db_tunit["num_likes"].
            db_tunit["num_mehs"],
            db_tunit["num_dislikes"]
        )

    def select_tunit_location(self, lat: float, long: float) -> list:
        """Gets a list of TUnits from the database by location.

        :param lat: a latitude coordinate
        :type lat: float
        :param long: a longitudinal coordinate
        :type long: float
        :raises sqlite3.DatabaseError:
        :returns: a list of TUNit objects
        :rtype: List[TUnit]
        """
        db = sqlite3.connect(self.db_filename)
        db.row_factory = self.__dict_factory
        cursor = db.cursor()
        query = """
        SELECT t_unit_id, 
            article_id, 
            sentence, 
            rank, 
            url, 
            access_timestamp, 
            lat, 
            long, 
            num_likes,
            num_mehs,
            num_dislikes
        FROM t_unit
        WHERE lat > ? - 0.5 AND lat < ? + 0.5
        AND 
        long > ? - 0.5 AND long < ? + 0.5
        """
        cursor.execute(query, (lat, lat, long, long))
        db_tunit = cursor.fetchone()
        if db_tunit is None:
            return None

        # query = """
        # SELECT name
        # FROM category
        # JOIN article_category ac on category.category_id = ac.category_id
        # JOIN t_unit tu on ac.article_id = tu.article_id
        # WHERE tu.article_id = ?
        # """
        # cursor.execute(query, (db_tunit["article_id"],))
        # categories = []
        # for row in cursor.fetchall():
        #     categories.append(row["name"])

        db.close()
        return TUnit(
            db_tunit["sentence"],
            db_tunit["article_id"],
            db_tunit["url"],
            db_tunit["access_timestamp"],
            db_tunit["t_unit_Id"],
            db_tunit["lat"],
            db_tunit["long"],
            db_tunit["num_likes"].
            db_tunit["num_mehs"],
            db_tunit["num_dislikes"]
        )

    def delete_tunit(self, tunit: TUnit):
        """Deletes a user from the database.

        :param tunit: a TUnit object to be deleted from database
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        DELETE FROM t_unit
        WHERE t_unit_Id = ?
        """
        cursor.execute(query, (tunit.t_unit_id,))
        db.commit()
        db.close()

    def insert_question(self, question: str, answer: str, t_unit_id: int) -> str:
        """Adds a question entry in the database.

        :param question: the question text to be added
        :type question: str
        :param tunit: the TUnit the question is associated with
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO question (t_unit_id, text, answer)
        VALUES (?,?,?)
        """
        cursor.execute(query, (t_unit_id, question, answer))
        db.commit()
        query = """
        SELECT qu_id
        FROM question
        WHERE text = ?
        """
        cursor.execute(query, (question,))
        q_id = cursor.fetchone()
        db.commit()
        db.close()
        return q_id

    def select_questions(self, tunit: TUnit) -> List[tuple]:
        """Gets a list of questions associated with a TUnit.

        :param tunit: the TUnit to retrieve questions from
        :type tunit: TUnit
        :raises sqlite3.DatabaseError:
        :return: a list of tuple representions of a question and its answer
        :rtype: List[(str, str)]
        """
        db = sqlite3.connect(self.db_filename)
        db.row_factory = self.__dict_factory
        cursor = db.cursor()
        query = """
        SELECT text, answer
        FROM question
        WHERE t_unit_id = ?
        """
        cursor.execute(query, (tunit.t_unit_id,))
        questions = []
        for row in cursor.fetchall():
            questions.append(row["name"])
        db.close()
        return questions

    def delete_question(self, question: str):
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        DELETE FROM question
        WHERE question.text = ?
        """
        cursor.execute(query, (question,))
        db.commit()
        db.close()

    def insert_category(self, category: str, importance: float) -> int:
        """Adds a category to the database.

        :param category: the category to be added to the database
        :type category: str
        :param importance: relevance of category
        :type importance: float
        :raises sqlite3.DatabaseError:
        """
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO category (name, importance) 
        VALUES (?,?)        
        """
        cursor.execute(query, (category, importance))
        db.commit()
        query = """
        SELECT category_id
        FROM category
        WHERE name = ?
        """
        cursor.execute(query, (category,))
        category_id = cursor.fetchone()
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

    def insert_vote(self, user: DBUser, q_id: int, interesting_rating: int, question_rating: int):
        """Adds a quality vote associated with a user and a question.

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
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO votes_on (user_id, q_id, interesting_rating, question_rating)
        VALUES (?,?,?,?)
        """
        cursor.execute(query, (user.user_id, q_id, interesting_rating, question_rating))
        db.commit()
        db.close()

    def select_articles_location(self, lat: float, long: float) -> list:
        """ Retrieves Articles from the database based on a location

        :param lat: the latitude coordinate
        :type lat: float
        :param long: the longitudinal coordinate
        :type long: float
        :raises sqlite3.DatabaseError:
        :returns: a list of Articles
        :rtype: List[Article]
        """
        db = sqlite3.connect(self.db_filename)
        db.row_factory = self.__dict_factory
        cursor = db.cursor()
        query = """
        SELECT a.article_id, title
        FROM article a
        JOIN t_unit tu on a.article_id = tu.article_id
        WHERE tu.lat > ? - 0.5 AND tu.lat < ? + 0.5 AND
        tu.long > ? - 0.5 AND tu.long < ? + 0.5
        """
        cursor.execute(query, (lat, lat, long, long))
        articles = []
        for article in cursor.fetchall():
            articles.append(article)
        db.close()
        return articles
