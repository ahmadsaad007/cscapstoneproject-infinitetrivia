from trivia_generator.TUnit import TUnit
from database_connection.dbconn import DBConn

conn = DBConn()
t_unit = TUnit('sentence2', 0, 'url2', 0, 7, 10, 10, 0, 0, 0)
t_unit = conn.delete_tunit(t_unit)
print()
