from mysql.connector.pooling import MySQLConnectionPool

from settings.settings import Config

try:
    pool = MySQLConnectionPool(**Config.mysql_config)
except Exception as e:
    print(e)


if __name__ == "__main__":
    print(pool)
