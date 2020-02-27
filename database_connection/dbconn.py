from dataclasses import dataclass
import sqlite3

@dataclass
class DBConn:

    """Database utilities

        :param DBFile: the name of the SQLite database file

    """


    DBFile: str = 

    def update_user(self):
        pass

    def get_user(self):
        pass

    def delete_user(self):
        pass

    def update_tunit(self):
        pass

    def get_tunit(self):
        pass

    def delete_tunit(self):
        pass

    def update_question(self):
        pass

    def get_question(self):
        pass

    def delete_question(self):
        pass

