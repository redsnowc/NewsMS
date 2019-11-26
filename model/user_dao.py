"""
用户类，处理用户相关数据库操作
"""
from settings.settings import Config
from libs.helper import execute_select_sql, execute_other_sql


class UserDao:
    def __init__(self):
        self.check_user_sql = """
            SELECT id, username, role_id 
            FROM t_user 
            WHERE username=%s 
            AND AES_DECRYPT(UNHEX(password), %s) = %s
        """
        self.get_user_sql = """
            SELECT username, email
            FROM t_user
            WHERE id = %s
        """
        self.get_users_sql = """
            SELECT u.id, u.username, r.role, u.email
            FROM t_user u
            JOIN t_role r
            ON u.role_id = r.id
            WHERE r.role = %s
            ORDER BY r.id
            LIMIT %s, %s
        """
        self.count_pages_sql = """
            SELECT CEIL(COUNT(*) / %s) 
            FROM t_user
            WHERE role_id = %s
        """
        self.delete_user_sql = """
            DELETE FROM t_user 
            WHERE id = %s
        """
        self.edit_user_sql = """
            UPDATE t_user
            SET username = %s, password = HEX(AES_ENCRYPT(%s, %s)), email = %s, role_id = %s
            WHERE id = %s
        """
        self.get_role_sql = """
            SELECT *
            FROM t_role
            WHERE id = %s
            ORDER BY id 
        """
        self.add_user_sql = """
            INSERT INTO t_user(username, password, email, role_id)
            VALUES (%s, HEX(AES_ENCRYPT(%s, %s)), %s, %s)
        """
        self.check_username_sql = """
            SELECT COUNT(*)
            FROM t_user
            WHERE username = %s
        """

    # 判断是否用户是否存在，处理登陆
    def check_user(self, username, password):
        user_info = execute_select_sql(self.check_user_sql, username, Config.secret_key, password)
        if user_info:
            return {"user_id": user_info[0][0], "username": user_info[0][1], "role": user_info[0][2]}
        return False

    # 获取所有用户
    def get_all_users(self, page):
        users_info = execute_select_sql(
            self.get_users_sql.replace("WHERE r.role = %s", ""), (page - 1) * Config.page_size, Config.page_size
        )
        return users_info

    # 根据 ID 搜索单个用户
    def get_user(self, user_id):
        user_info = execute_select_sql(self.get_user_sql, user_id)
        return user_info

    # 获取用户总页数
    def count_all_pages(self):
        pages = execute_select_sql(
            self.count_pages_sql.replace("WHERE role_id = %s", ""), Config.page_size
        )
        return pages

    # 添加用户
    def add_user(self, username, password, email, role_id):
        execute_other_sql(self.add_user_sql, username, password, Config.secret_key, email, role_id)

    # 编辑用户
    def edit_user(self, username, password, email, role_id, user_id):
        execute_other_sql(self.edit_user_sql, username, password,
                          Config.secret_key, email, role_id, user_id)

    # 获取所有角色
    def get_all_roles(self):
        role_info = execute_select_sql(self.get_role_sql.replace("WHERE id = %s", ""))
        return role_info

    # 删除用户
    def delete_user(self, user_id):
        execute_other_sql(self.delete_user_sql, user_id)

    # 检查用户名是否已存在
    def check_username(self, username):
        result = execute_select_sql(self.check_username_sql, username)
        return result


if __name__ == "__main__":
    user = UserDao()
