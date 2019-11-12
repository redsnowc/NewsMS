import sys
import os

from getpass import getpass
from colorama import Fore

from service.user_service import UserService
from service.news_service import NewsService
from message.message import Message
from settings.settings import Config
from libs.helper import clear_screen as cls, handle_error, check_null, input_cycle, exit_sys, log_out, time_sleep, \
    is_number, next_page, prev_page


def start():
    """
    启动入口
    :return: none
    """
    print(Message.start_msg["welcome"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        login()
    elif input_val == "2":
        exit_sys()
    else:
        handle_error(Message.common_msg["error"], start)


def login():
    """
    登陆
    :return: none
    """
    username = input(Message.login_msg["username"])
    check_null(username, Message.login_msg["username_error"], login)

    password = getpass(Message.login_msg["password"])
    if not password:
        password = input_cycle(
            password, Message.login_msg["pwd_error"], Message.login_msg["password"], kind="password"
        )
    user_service = UserService()
    user = user_service.login(username, password)

    if not user:
        handle_error(Message.login_msg["login_error"], start)
    else:
        cls()
        if user["role"] == 1:
            manage_admin(user)
        elif user["role"] == 2:
            manage_editor(user)


def manage_admin(user):
    """
    管理员身份管理页面
    :param user: 管理员信息
    :return: none
    """
    print(Message.manage_msg["option_admin"])
    print(Message.manage_msg["leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        manage_news(user)
    elif input_val == "2":
        pass
    elif input_val == "back":
        log_out()
    elif input_val == "exit":
        exit_sys()
    else:
        handle_error(Message.common_msg["error"], manage_admin, user)


def manage_editor(user):
    """
    编辑身份管理页面
    :param user: 编辑信息
    :return: none
    """
    print(Message.manage_msg["option_editor"])
    print(Message.manage_msg["leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        edit_news(user)
    elif input_val == "back":
        log_out()
    elif input_val == "exit":
        exit_sys()
    else:
        handle_error(Message.common_msg["error"], manage_admin, user)


def manage_news(user):
    """
    管理新闻，仅管理员可见
    :param user: 管理员身份信息
    :return: none
    """
    print(Message.manage_news_msg["option"])
    print(Message.manage_news_msg["leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        approval_news(user)
    elif input_val == "2":
        cls()
        delete_nes(user)
    elif input_val == "back":
        cls()
        manage_admin(user)
    else:
        handle_error(Message.common_msg["error"], manage_news, user)


def approval_news(user, page=1):
    page = page
    news_service = NewsService()
    results = news_service.get_padding_news(page, Config.page_size)
    pages = news_service.get_padding_pages()
    index = 1
    for i in results:
        print(Fore.BLUE + "\n%s. %s %s %s \n" % (index, i[1], i[2], i[3]))
        index += 1
    print("---------------------\n")
    print("%s/%s\n" % (page, pages))
    print("---------------------")
    print(Message.approval_news_msg["leave"])
    input_val = input(Message.approval_news_msg["prompt"])

    if is_number(input_val):
        index = is_number(input_val)
        if 10 >= index >= 1:
            news_id = results[index - 1][0]
            news_service.approval_news(news_id)
            cls()
            print(Message.approval_news_msg["approval_success"])
            approval_news(user, page)
        else:
            handle_error(Message.approval_news_msg["news_id_error"], approval_news, user, page)
    elif input_val == "back":
        cls()
        manage_news(user)
    elif input_val == "prev":
        page = prev_page(page, approval_news, user)
    elif input_val == "next":
        page = next_page(page, pages, approval_news, user)
    else:
        handle_error(Message.common_msg["error"], approval_news, user, page)


def delete_nes(user):
    pass


def edit_news(user):
    """
    编辑新闻，临时，仅编辑身份可见
    :param user: 编辑身份信息
    :return: none
    """
    print(Fore.RED + "新闻模块开发中...\n")
    time_sleep(3)
    cls()
    start()


if __name__ == "__main__":
    cls()
    start()
