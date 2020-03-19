"""
Database Connection
===================
"""
from dataclasses import dataclass
import sqlite3

from game_models import Player
from trivia_generator import TUnit
from typing import List
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


@dataclass
class DBConn:
    """Class representing a database connection.

    :param db_filename: the name of the SQLite database file. Will be fetched at runtime from database config file.
    """

    DB_CONFIG_FILE: str = "database_connection/db.cfg"
    db_filename: str = None

    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def __coordinate_search_query(lat, long):
        query = None
        if lat >= 0 and long >= 0:
            query = """
            WHERE lat > ? - 0.5 AND lat < ? + 0.5
                AND long > ? - 0.5 AND long < ? + 0.5
            """
        elif lat < 0 and long >= 0:
            query = """
            WHERE lat > ? - 0.5 AND lat < ? + 0.5
                AND long > ? + 0.5 AND long < ? - 0.5
            """
        elif lat >= 0 and long < 0:
            query = """
            WHERE lat > ? + 0.5 AND lat < ? - 0.5
                AND long > ? - 0.5 AND long < ? + 0.5
            """
        elif lat < 0 and long < 0:
            query = """
            WHERE lat > ? + 0.5 AND lat < ? - 0.5
                AND long > ? + 0.5 AND long < ? - 0.5
            """
        return query

    def __init__(self):
        with open(DBConn.DB_CONFIG_FILE, "r") as file:
            self.db_filename = file.read().split("=")[1]

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
        return rows

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
        user_id = cursor.fetchone()
        db.close()
        return user_id

    def update_user(self, user: DBUser):
        """Adds or updates a user in the database.

        :param user: the Player object to be added to the database
        :type user: Player
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
        db.close()

    def update_password(self, username: str, password: str):
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

    def select_user(self, username: str) -> DBUser:
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
        return DBUser(*user)

    def delete_user(self, user: DBUser):
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

    def insert_tunit(self, tunit: TUnit) -> int:
        db = sqlite3.connect(self.db_filename)
        cursor = db.cursor()
        query = """
        INSERT INTO t_unit (
            article_id, 
            sentence, 
            rank, 
            url, 
            access_timestamp,
            lat, 
            long, 
            has_superlative, 
            has_contrasting, 
            root_word, 
            subj_word, 
            readability)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(query, (
            tunit.article_id,
            tunit.sentence,
            tunit.trivia_rank,
            tunit.url,
            tunit.access_timestamp,
            tunit.latitude,
            tunit.longitude,
            tunit.has_superlative,
            tunit.has_contrasting,
            tunit.root_word,
            tunit.subj_word,
            tunit.readability
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
            rank = ?,
            url = ?,
            access_timestamp = ?,
            lat = ?,
            long = ?,
            has_superlative = ?,
            has_contrasting = ?,
            root_word = ?,
            subj_word = ?,
            readability = ?
        WHERE t_unit_Id = ?
        """
        cursor.execute(query, (
            tunit.sentence,
            tunit.trivia_rank,
            tunit.url,
            tunit.access_timestamp,
            tunit.latitude,
            tunit.longitude,
            tunit.has_superlative,
            tunit.has_contrasting,
            tunit.root_word,
            tunit.subj_word,
            tunit.readability,
            tunit.t_unit_id
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
            rank,
            url,
            access_timestamp,
            lat,
            long,
            has_superlative,
            has_contrasting,
            root_word,
            subj_word,
            readability
        FROM t_unit
        ORDER BY RANDOM() LIMIT 1;
        """
        cursor.execute(query)
        tunit = cursor.fetchone()
        db.close()
        return tunit

    def select_tunit_category(self, category: str) -> List[TUnit]:
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
            rank,
            url,
            access_timestamp,
            lat,
            long,
            has_superlative,
            has_contrasting,
            root_word,
            subj_word,
            readability
        FROM t_unit t
        JOIN article_category ac on t.article_id = ac.article_id
        JOIN category c on ac.category_id = c.category_id
        WHERE c.name = ?
        """
        cursor.execute(query, (category,))
        db_tunit = cursor.fetchone()

        query = """
        SELECT name
        FROM category
        JOIN article_category ac on category.category_id = ac.category_id
        JOIN t_unit tu on ac.article_id = tu.article_id
        WHERE tu.article_id = ?
        """
        cursor.execute(query, (db_tunit["article_id"],))
        categories = []
        for row in cursor.fetchall():
            categories.append(row["name"])

        db.close()
        return TUnit(
            db_tunit["sentence"],
            db_tunit["article_id"],
            db_tunit["url"],
            categories,
            db_tunit["access_timestamp"],
            db_tunit["has_superlative"],
            db_tunit["has_contrasting"],
            db_tunit["root_word"],
            db_tunit["subj_word"],
            db_tunit["readability"],
            db_tunit["t_unit_Id"],
            db_tunit["lat"],
            db_tunit["long"],
            db_tunit["rank"]
        )

    def select_tunit_location(self, lat: float, long: float) -> List[TUnit]:
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
            has_superlative, 
            has_contrasting, 
            root_word, 
            subj_word, 
            readability
        FROM t_unit
        """
        query += self.__coordinate_search_query(lat, long)
        self.__coordinate_search_query(lat, long)
        cursor.execute(query, (lat, lat, long, long))
        db_tunit = cursor.fetchone()

        query = """
        SELECT name
        FROM category
        JOIN article_category ac on category.category_id = ac.category_id
        JOIN t_unit tu on ac.article_id = tu.article_id
        WHERE tu.article_id = ?
        """
        cursor.execute(query, (db_tunit["article_id"],))
        categories = []
        for row in cursor.fetchall():
            categories.append(row["name"])

        db.close()
        return TUnit(
            db_tunit["sentence"],
            db_tunit["article_id"],
            db_tunit["url"],
            categories,
            db_tunit["access_timestamp"],
            db_tunit["has_superlative"],
            db_tunit["has_contrasting"],
            db_tunit["root_word"],
            db_tunit["subj_word"],
            db_tunit["readability"],
            db_tunit["t_unit_Id"],
            db_tunit["lat"],
            db_tunit["long"],
            db_tunit["rank"]
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

    def insert_question(self, question: str, answer: str, tunit: TUnit) -> str:
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
        cursor.execute(query, (tunit["t_unit_Id"], question, answer))
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

    def select_articles_location(self, lat: float, long: float) -> List[Article]:
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
        SELECT article_id, title
        FROM article 
        """
        query += self.__coordinate_search_query(lat, long)
        cursor.execute(query, (lat, lat, long, long))
        articles = []
        for article in cursor.fetchall():
            articles.append(article)
        db.close()
        return articles
