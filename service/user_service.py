from model.user_dao import UserDao


class UserService:
    def __init__(self):
        self.user_dao = UserDao()

    # 登陆
    def login(self, username, password):
        user = self.user_dao.check_user(username, password)
        return user or False

    # 根据 id 获取用户信息
    def get_user(self, user_id):
        user_info = self.user_dao.get_user(user_id)
        return user_info

    # 获取所有数据
    def get_all_users(self, page):
        users = self.user_dao.get_all_users(page)
        return users

    # 获取所有角色
    def get_all_roles(self):
        roles = self.user_dao.get_all_roles()
        return roles

    # 获取用户总页数
    def count_all_pages(self):
        pages = self.user_dao.count_all_pages()
        return int(pages[0][0])

    # 编辑用户
    def edit_user(self, username, password, email, role_id, user_id):
        self.user_dao.edit_user(username, password, email, role_id, user_id)

    # 添加用户
    def add_user(self, username, password, email, role_id):
        self.user_dao.add_user(username, password, email, role_id)

    # 删除用户
    def delete_user(self, user_id):
        self.user_dao.delete_user(user_id)

    # 检查用户名是否已存在
    def check_username(self, username):
        result = self.user_dao.check_username(username)
        if result[0][0]:
            return True
        return False


if __name__ == "__main__":
    u = UserService()
    a = u.login("admin", 123456)
    print(a)
