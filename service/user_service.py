from model.user_dao import UserDao


class UserService:
    def __init__(self):
        self.user_dao = UserDao()

    def login(self, username, password):
        user = self.user_dao.check_user(username, password)
        return user or False

    def get_user(self, user_id):
        user_info = self.user_dao.get_user(user_id)
        return user_info

    def get_all_users(self, page):
        users = self.user_dao.get_all_users(page)
        return users

    def get_all_roles(self):
        roles = self.user_dao.get_all_roles()
        return roles

    def count_all_pages(self):
        pages = self.user_dao.count_all_pages()
        return int(pages[0][0])

    def edit_user(self, username, password, email, role_id, user_id):
        self.user_dao.edit_user(username, password, email, role_id, user_id)

    def add_user(self, username, password, email, role_id):
        self.user_dao.add_user(username, password, email, role_id)

    def delete_user(self, user_id):
        self.user_dao.delete_user(user_id)


if __name__ == "__main__":
    u = UserService()
    a = u.login("admin", 123456)
    print(a)
