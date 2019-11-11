from mysql.connector.pooling import MySQLConnectionPool

from settings.settings import mysql_config

# class ConnectionPoll:
#     def __init__(self, config):
#         self.config = config
#
#     def create_connection(self):
#
#
#
# if __name__ == "__main__":
#     c = ConnectionPoll(mysql_config)
#     s = c.create_connection()
#     con = s.get_connection()
#     cursor = con.cursor()
#     cursor.execute("DESC t_user")
#     print(cursor.fetchall())

try:
    pool = MySQLConnectionPool(**mysql_config)
except Exception as e:
    print(e)


if __name__ == "__main__":
    print(pool)
