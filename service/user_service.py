from model.user_dao import UserDao


class UserService:
    def __init__(self):
        self.user_dao = UserDao()

    def login(self, username, password):
        user = self.user_dao.check_user(username, password)
        return user or False


if __name__ == "__main__":
    u = UserService()
    a = u.login("admin", 123456)
    print(a)
