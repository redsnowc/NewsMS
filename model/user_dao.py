"""
用户类，处理用户相关数据库操作
"""
from settings.settings import Config
from libs.helper import execute_select_sql


class UserDao:
    def __init__(self):
        self.check_user_sql = """
            SELECT username, role_id FROM t_user WHERE username=%s AND AES_DECRYPT(UNHEX(password), %s) = %s
        """

    # 判断是否用户是否存在
    def check_user(self, username, password):
        info = execute_select_sql(self.check_user_sql, username, Config.secret_key, password)
        if info:
            return {"username": info[0][0], "role": info[0][1]}
        return False


if __name__ == "__main__":
    user = UserDao()
    a = user.check_user("admin", "123456")
    print(a)
