import sys
import os

from getpass import getpass
from colorama import Fore

from service.user_service import UserService
from service.news_service import NewsService
from message.message import Message
from settings.settings import Config
from libs.helper import clear_screen as cls, handle_error, check_null, input_cycle, exit_sys, log_out, time_sleep, \
    is_number, next_page, prev_page, list_results, handle_input, display_judge, get_password, get_role_id, handle_save, \
    get_email

news_service = NewsService()
user_service = UserService()


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
    username = input(Message.common_msg["username"])
    check_null(username, Message.common_msg["username_error"], callback=login)

    password = getpass(Message.common_msg["password"])
    if not password:
        password = input_cycle(
            password, Message.common_msg["pwd_error"], Message.common_msg["password"], kind="password"
        )
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
        cls()
        manage_users(user)
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
    print(Message.manage_msg["child_leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        approval_news(user)
    elif input_val == "2":
        cls()
        delete_news(user)
    elif input_val == "back":
        cls()
        manage_admin(user)
    else:
        handle_error(Message.common_msg["error"], manage_news, user)


def approval_news(user, page=1):
    """
    审核新闻，仅管理员可见
    :param user: 用户数据
    :param page: 初始显示页码 default=1
    :return: none
    """
    page = page
    results = news_service.get_padding_news(page)
    pages = news_service.count_padding_pages()
    display_judge(page, results, pages, news_service.approval_news, approval_news, manage_news, user)


def delete_news(user, page=1):
    """
    删除新闻，仅管理员可见
    :param user: 用户数据
    :param page: 初始显示页码 default=1
    :return: none
    """
    page = page
    results = news_service.get_all_news(page)
    pages = news_service.count_all_pages()
    display_judge(page, results, pages, news_service.delete_news, delete_news, manage_news, user)


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


def manage_users(user):
    print(Message.manage_users["option"])
    print(Message.manage_msg["child_leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        add_user(user)
    elif input_val == "2":
        cls()
        edit_user(user)
    elif input_val == "3":
        cls()
        delete_user(user)
    elif input_val == "back":
        cls()
        manage_admin(user)
    else:
        handle_error(Message.common_msg["error"], manage_news, user)


def add_user(user):
    role_info = user_service.get_all_roles()
    username = input(Message.common_msg["username"])
    check_null(username, Message.common_msg["username_error"], user, callback=add_user)
    pwd = get_password(Message.common_msg["password"])


def edit_user(user, page=1):
    page = page
    users = user_service.get_all_users(page)
    pages = user_service.count_all_pages()
    list_results(page, users, pages)
    input_val = input(Message.manage_users["prompt"])

    if is_number(input_val):
        index = is_number(input_val)
        if len(users) >= index >= 1:
            cls()
            edit_user_input(user, users, index, page)
        else:
            handle_error(Message.common_msg["id_error"], edit_news, user, page)
    elif input_val == "back":
        cls()
        manage_users(user)
    elif input_val == "prev":
        page = prev_page(page, edit_news, user)
    elif input_val == "next":
        page = next_page(page, pages, edit_news, user)
    else:
        handle_error(Message.common_msg["error"], edit_news, user, page)


def edit_user_input(user, users, index, page):
    user_id = users[index - 1][0]
    user_info = user_service.get_user(user_id)
    role_info = user_service.get_all_roles()

    print(Message.edit_user["old_username"] % user_info[0][0])
    new_username = input(Message.edit_user["new_username"])
    check_null(new_username, Message.common_msg["username_error"], user, users, index, page, callback=edit_user_input)

    new_pwd = get_password(Message.edit_user["new_pwd"])

    print(Message.edit_user["old_email"] % user_info[0][1])
    new_email = get_email()

    for i in role_info:
        print(Fore.BLUE + "\n%s. %s" % (i[0], i[1]))

    new_role_id = get_role_id(role_info)
    handle_save(user_service.edit_user, new_username, new_pwd, new_email, new_role_id, user_id)

    time_sleep(3)
    cls()
    print(Message.common_msg["success"])
    edit_user(user, page)


def delete_user(user, page=1):
    page = page
    results = user_service.get_all_users(page)
    pages = user_service.count_all_pages()
    display_judge(page, results, pages, user_service.delete_user, delete_user, manage_users, user)


if __name__ == "__main__":
    cls()
    start()
