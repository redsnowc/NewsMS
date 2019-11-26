from mysql.connector.pooling import MySQLConnectionPool
from redis import ConnectionPool

from settings.settings import Config

try:
    mysql_pool = MySQLConnectionPool(**Config.mysql_config)
except Exception as e:
    print(e)

try:
    redis_pool = ConnectionPool(**Config.redis_config)
except Exception as e:
    print(e)


if __name__ == "__main__":
    print(mysql_pool)
    print(redis_pool)
