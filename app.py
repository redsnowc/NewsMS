import sys
import os

from service.user_service import UserService
from message.message import Message
from libs.helper import clear_screen as cls, handle_error, check_null, input_cycle


def start():
    print(Message.start_msg["welcome"])
    input_val = input(Message.start_msg["prompt"])
    if input_val == "1":
        cls()
        login()
    elif input_val == "2":
        print(Message.start_msg["exit"])
        sys.exit()
    else:
        handle_error(Message.start_msg["error"], start)


def login():
    username = input(Message.login_msg["username"])
    check_null(username, Message.login_msg["username_error"], login)
    password = input(Message.login_msg["password"])
    if not password:
        password = input_cycle(password, Message.login_msg["pwd_error"], Message.login_msg["password"])
    user_service = UserService()
    user = user_service.login(username, password)
    if not user:
        handle_error(Message.login_msg["login_error"], start)
    else:
        pass


if __name__ == "__main__":
    cls()
    start()
