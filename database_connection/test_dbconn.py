import sqlite3
import unittest
from os import remove, path
from scipy.stats import chisquare

from database_connection.dbconn import DBConn, DBUser
from trivia_generator.TUnit import TUnit


class TestDBConn(unittest.TestCase):
    DB_FILENAME = 'test.db'
    SCHEMA_FILENAME = 'test_sql/test_schema.sql'
    DATA_FILENAME = 'test_sql/test_data.sql'
    REMOVE_DATA_FILENAME = 'test_sql/test_remove_data.sql'

    @classmethod
    def setUpClass(cls) -> None:
        """
        Runs before the first test
        """
        if path.exists(TestDBConn.DB_FILENAME):
            remove(TestDBConn.DB_FILENAME)
        test_db = sqlite3.connect(cls.DB_FILENAME)
        with open(cls.SCHEMA_FILENAME, 'r') as f:
            test_db.cursor().executescript(f.read())
        test_db.commit()
        test_db.close()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Runs after the last test
        """
        remove(cls.DB_FILENAME)
        pass

    def setUp(self) -> None:
        """
        Runs before each test method
        """
        test_db = sqlite3.connect(TestDBConn.DB_FILENAME)
        with open(TestDBConn.DATA_FILENAME, 'r') as f:
            test_db.cursor().executescript(f.read())
        test_db.commit()
        test_db.close()

    def tearDown(self) -> None:
        """
        Runs after each test method
        """
        test_db = sqlite3.connect(TestDBConn.DB_FILENAME)
        with open(TestDBConn.REMOVE_DATA_FILENAME, 'r') as f:
            test_db.cursor().executescript(f.read())
        test_db.commit()
        test_db.close()

    def test_select_random_article(self):
        observations = {}
        for j in range(10000):
            article_id, article_text = DBConn(TestDBConn.DB_FILENAME).select_random_article()
            self.assertEqual(article_id, ord(article_text) - 97)
            if article_id in observations.keys():
                observations[article_id] += 1
            else:
                observations[article_id] = 1
        act_chisq, p = chisquare(list(observations.values()))
        # NOTE(Alex): This value is retrieved from a chi square critical value chart with 9 degrees of freedom
        # (10 articles - 1) and using a P value of 0.01
        exp_max_chisq = 21.67
        self.assertLess(act_chisq, exp_max_chisq)

    def test_select_article_categories(self):
        article_id = 0
        exp_categories = ['category_a', 'category_b', 'category_c']
        act_categories = DBConn(TestDBConn.DB_FILENAME).select_article_categories(article_id)
        self.assertEqual(exp_categories, act_categories)

    def test_select_category_articles(self):
        category = 'category_b'
        exp_articles = [(0, 'a'), (1, 'b')]
        act_articles = DBConn(TestDBConn.DB_FILENAME).select_category_articles(category)
        self.assertEqual(exp_articles, act_articles)

    def test_insert_user(self):
        exp_user = DBUser(username='Jim', email='jim@email.com')
        exp_password = 'pass'
        user_id = DBConn(TestDBConn.DB_FILENAME).insert_user(exp_user, exp_password)
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        query = '''
        SELECT *
        FROM user
        WHERE user_id = ?
        '''
        rows = conn.cursor().execute(query, (user_id,)).fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        row = rows[0]  # row: (1, 'Jim', 'jim@email', 'pass', 0, 0, 0, 0)
        exp_user.user_id = row[0]
        act_user = DBUser(user_id=row[0], username=row[1], email=row[2], wins=row[4], losses=row[5],
                          num_answered=row[6], num_answered_correct=row[7])
        act_password = row[3]
        self.assertEqual(exp_user, act_user)
        self.assertEqual(exp_password, act_password)

    def test_update_user_exists(self):
        exp_user = DBUser(username='Jack', email='jack@email.com', wins=8, losses=8, num_answered=16,
                          num_answered_correct=8)
        exp_password = 'pass2'
        user_id = DBConn(TestDBConn.DB_FILENAME).update_user(exp_user)
        query = '''
        SELECT *
        FROM user
        WHERE user_id = ?
        '''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        rows = conn.cursor().execute(query, (user_id,)).fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        row = rows[0]  # row: (1, 'Jim', 'jim@email', 'pass', 0, 0, 0, 0)
        exp_user.user_id = row[0]
        act_user = DBUser(user_id=row[0], username=row[1], email=row[2], wins=row[4], losses=row[5],
                          num_answered=row[6], num_answered_correct=row[7])
        act_password = row[3]
        self.assertEqual(exp_user, act_user)
        self.assertEqual(exp_password, act_password)

    def test_update_user_does_not_exist(self):
        user = DBUser(username='Jane', email='jane@email.com')
        exp_user_id = -1
        act_user_id = DBConn(TestDBConn.DB_FILENAME).update_user(user)
        self.assertEqual(exp_user_id, act_user_id)

    def test_update_password(self):
        exp_username = 'Jill'
        exp_password = 'test'
        DBConn(TestDBConn.DB_FILENAME).update_password(exp_username, exp_password)
        query = '''
        SELECT username, password
        FROM user
        WHERE username = ?
        '''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        act_username, act_password = conn.cursor().execute(query, (exp_username,)).fetchone()
        self.assertEqual(exp_username, act_username)
        self.assertEqual(exp_password, act_password)

    def test_select_user_exists(self):
        exp_user = DBUser(0, 'Jill', 'jill@email.com', 5, 5, 10, 5)
        act_user = DBConn(TestDBConn.DB_FILENAME).select_user('Jill')
        self.assertEqual(exp_user, act_user)

    def test_select_user_does_not_exist(self):
        act_user = DBConn(TestDBConn.DB_FILENAME).select_user('bum')
        self.assertIsNone(act_user)

    def test_delete_user(self):
        user = DBUser(0, 'Jill', 'jill@email.com', 5, 5, 10, 5)
        DBConn(TestDBConn.DB_FILENAME).delete_user(user)
        query = '''
        SELECT username
        FROM user
        WHERE username = ?
        '''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        act_user = conn.cursor().execute(query, (user.username,)).fetchone()
        self.assertIsNone(act_user)

    def test_insert_tunit(self):
        exp_t_unit = TUnit('sentence', 0, 'url', 1234, None, 10, 10, 0, 0, 0)
        t_unit_Id = DBConn(TestDBConn.DB_FILENAME).insert_tunit(exp_t_unit)
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        query = """
                SELECT sentence, article_id, url, access_timestamp, t_unit_Id, lat, long, num_likes, num_mehs,
                    num_dislikes
                FROM t_unit
                WHERE t_unit_Id = ?;
                """
        cursor = conn.cursor()
        cursor.execute(query, (t_unit_Id,))
        rows = cursor.fetchall()
        # rows = conn.cursor().execute(query, (t_unit_Id,)).fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        row = rows[0]  # row: ('sentence', 0, 'url', 1234, <t_unit_Id>, 10, 10, 0, 0, 0)
        exp_t_unit.t_unit_id = row[4]
        act_t_unit = TUnit(*row)
        self.assertEqual(exp_t_unit, act_t_unit)

    # TODO(Alex): test_update_tunit_exists()
    def test_update_tunit_exists(self):
        exp_user = DBUser(username='Jack', email='jack@email.com', wins=8, losses=8, num_answered=16,
                          num_answered_correct=8)
        exp_password = 'pass2'
        user_id = DBConn(TestDBConn.DB_FILENAME).update_user(exp_user)
        query = '''
        SELECT *
        FROM user
        WHERE user_id = ?
        '''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        rows = conn.cursor().execute(query, (user_id,)).fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        row = rows[0]  # row: (1, 'Jim', 'jim@email', 'pass', 0, 0, 0, 0)
        exp_user.user_id = row[0]
        act_user = DBUser(user_id=row[0], username=row[1], email=row[2], wins=row[4], losses=row[5],
                          num_answered=row[6], num_answered_correct=row[7])
        act_password = row[3]
        self.assertEqual(exp_user, act_user)
        self.assertEqual(exp_password, act_password)

    # TODO(Alex): test_update_tunit_does_not_exist()
    def test_update_tunit_does_not_exist(self):
        user = DBUser(username='Jane', email='jane@email.com')
        exp_user_id = -1
        act_user_id = DBConn(TestDBConn.DB_FILENAME).update_user(user)
        self.assertEqual(exp_user_id, act_user_id)

    # TODO(Alex): test_select_tunit_random()

    # TODO(Alex): test_select_tunit_category_exists()

    # TODO(Alex): test_select_tunit_category_does_not_exists()

    # TODO(Alex): test_select_tunit_location_exists()

    # TODO(Alex): test_select_tunit_loaction_does_not_exist()

    # TODO(Alex): test_delet_tunit()

    def test_insert_category(self):
        exp_category = ('category', 1.5)
        category_id = DBConn(TestDBConn.DB_FILENAME).insert_category(*exp_category)
        query = '''
        SELECT name, importance
        FROM category
        WHERE name = ?'''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        act_category = conn.cursor().execute(query, (exp_category[0],)).fetchone()
        self.assertEqual(exp_category, act_category)

    def test_delete_category(self):
        category = 'category_a'
        DBConn(TestDBConn.DB_FILENAME).delete_category(category)
        query = '''
        SELECT *
        FROM category
        WHERE name = ?'''
        conn = sqlite3.connect(TestDBConn.DB_FILENAME)
        act_category = conn.cursor().execute(query, (category,)).fetchone()
        self.assertIsNone(act_category)

    def test_select_articles_location_positive(self):
        exp_articles = [(0, 'a'), (1, 'b')]
        location = (30.1, 30.1)
        act_articles = DBConn(TestDBConn.DB_FILENAME).select_articles_location(*location)
        self.assertEqual(exp_articles, act_articles)

    def test_select_articles_location_negative(self):
        exp_articles = [(2, 'c')]
        location = (-30.1, 30.1)
        act_articles = DBConn(TestDBConn.DB_FILENAME).select_articles_location(*location)
        self.assertEqual(exp_articles, act_articles)

    def test_select_articles_location_does_not_exist(self):
        exp_articles = []
        location = (0, 0)
        act_articles = DBConn(TestDBConn.DB_FILENAME).select_articles_location(*location)
        self.assertEqual(exp_articles, act_articles)


if __name__ == '__main__':
    unittest.main()
