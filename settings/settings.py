import os

"""
    配置文件
"""


class Config:
    # 数据库连接配置
    mysql_config = {
                       "host": "localhost",
                       "port": 3306,
                       "user": "root",
                       "password": os.getenv("mysql_pwd", "1234"),
                       "database": "vega",
                       "pool_size": 10,
                   }
    # 秘钥
    secret_key = os.getenv("secret_key", "abc")
    # 每页显示数量
    page_size = 10

