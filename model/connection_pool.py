from mysql.connector.pooling import MySQLConnectionPool
from redis import ConnectionPool
from pymongo import MongoClient

from settings.settings import Config

# MySQL
try:
    mysql_pool = MySQLConnectionPool(**Config.mysql_config)
except Exception as e:
    print(e)

# redis
try:
    redis_pool = ConnectionPool(**Config.redis_config)
except Exception as e:
    print(e)

# mongoDB
try:
    client = MongoClient(host=Config.mongo_config["host"], port=Config.mongo_config["port"])
    client.admin.authenticate(Config.mongo_config["username"], Config.mongo_config["password"])
except Exception as e:
    print(e)


if __name__ == "__main__":
    print(mysql_pool)
    print(redis_pool)
    print(client)
