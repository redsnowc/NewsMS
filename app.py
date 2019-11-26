from getpass import getpass
from colorama import Fore

from service.user_service import UserService
from service.news_service import NewsService
from service.type_service import TypeService
from message.message import Message
from libs.helper import clear_screen as cls, handle_error, check_null, input_cycle, exit_sys, log_out, time_sleep, \
    is_number, next_page, prev_page, list_results, display_judge, get_password, get_id, handle_save, \
    get_email, get_is_top, edit_list_data

news_service = NewsService()
user_service = UserService()
type_service = TypeService()


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
    :param user: 管理员身份信息
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
    :param user: 编辑身份信息
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
        handle_error(Message.common_msg["error"], manage_editor, user)


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
    :param user: 管理员身份信息
    :param page: 初始显示页码 default=1
    :return: none
    """
    page = page
    results = news_service.get_padding_news(page)
    pages = news_service.count_padding_pages()
    display_judge(
        page, results, pages, news_service.approval_news, approval_news,
        manage_news, user, rocket_search_service=news_service.get_news_detail,
        rocket_cache_service=news_service.cache_news
    )


def delete_news(user, page=1):
    """
    删除新闻，仅管理员可见
    :param user: 管理员身份信息
    :param page: 初始显示页码 default=1
    :return: none
    """
    page = page
    results = news_service.get_all_news(page)
    pages = news_service.count_all_pages()
    display_judge(page, results, pages, news_service.delete_news, delete_news,
                  manage_news, user, rocket_delete_service=news_service.delete_news_redis)


def manage_users(user):
    """
    管理用户，仅管理员可见
    :param user: 管理员身份信息
    :return: none
    """
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
        handle_error(Message.common_msg["error"], manage_users, user)


def add_user(user):
    """
    添加用户，仅管理员可见
    :param user: 管理员身份信息
    :return: none
    """
    role_info = user_service.get_all_roles()
    username = input(Message.common_msg["username"])
    check_null(username, Message.common_msg["username_error"], user, callback=add_user)
    if user_service.check_username(username):
        handle_error(Message.common_msg["username_duplicate"], add_user, user)
    pwd = get_password(Message.common_msg["password"])
    email = get_email(Message.add_user["email"])
    print(email)
    for i in role_info:
        print(Fore.BLUE + "\n%s. %s" % (i[0], i[1]))
    role_id = get_id(role_info, Message.common_msg["role_error"], Message.common_msg["role_id"])
    handle_save(user_service.add_user, username, pwd, email, role_id)

    time_sleep(3)
    cls()
    print(Message.common_msg["success"])
    manage_users(user)


def edit_user(user, page=1):
    """
    编辑用户信息，仅管理员可见
    :param user: 管理员身份信息
    :param page: 初始页码 default=1
    :return: none
    """
    page = page
    users = user_service.get_all_users(page)
    pages = user_service.count_all_pages()
    edit_list_data(user, users, page, pages, Message.manage_users["prompt"],
                   Message.common_msg["id_error"], edit_user_input, edit_user, manage_users)


def edit_user_input(user, users, index, page):
    """
    编辑用户输入界面，仅管理员可见
    :param user: 管理员身份信息
    :param users: 所有用户查询结果集
    :param index: 用户输入编号
    :param page: 当前页码
    :return: none
    """
    user_id = users[index - 1][0]
    user_info = user_service.get_user(user_id)
    role_info = user_service.get_all_roles()

    print(Message.edit_user["old_username"] % user_info[0][0])
    new_username = input(Message.edit_user["new_username"])
    check_null(new_username, Message.common_msg["username_error"], user, users, index, page, callback=edit_user_input)
    if new_username != user_info[0][0]:
        if user_service.check_username(new_username):
            handle_error(Message.common_msg["username_duplicate"], edit_user_input, user, users, index, page)

    new_pwd = get_password(Message.edit_user["new_pwd"])

    print(Message.edit_user["old_email"] % user_info[0][1])
    new_email = get_email(Message.edit_user["new_email"])

    for i in role_info:
        print(Fore.BLUE + "\n%s. %s" % (i[0], i[1]))

    new_role_id = get_id(role_info, Message.common_msg["role_error"], Message.common_msg["role_id"])
    handle_save(user_service.edit_user, new_username, new_pwd, new_email, new_role_id, user_id)

    time_sleep(3)
    cls()
    print(Message.common_msg["success"])
    edit_user(user, page)


def delete_user(user, page=1):
    """
    删除用户，仅管理员可见
    :param user: 管理员身份信息
    :param page: 初始页码 default=1
    :return: none
    """
    page = page
    results = user_service.get_all_users(page)
    pages = user_service.count_all_pages()
    display_judge(page, results, pages, user_service.delete_user, delete_user, manage_users, user)


def edit_news(user):
    """
    编辑新闻，仅编辑身份可见
    :param user: 编辑身份信息
    :return: none
    """
    print(Message.edit_news["option"])
    print(Message.manage_msg["leave"])
    input_val = input(Message.common_msg["prompt"])
    if input_val == "1":
        cls()
        insert_news(user)
    elif input_val == "2":
        cls()
        edit_news_editor(user)
    elif input_val == "back":
        log_out()
    elif input_val == "exit":
        exit_sys()
    else:
        handle_error(Message.common_msg["error"], edit_news, user)


def insert_news(user):
    """
    插入新闻，新闻编辑可见
    :param user: 编辑身份信息
    :return: none
    """
    type_results = type_service.get_all_type()
    news_title = input(Message.edit_news["title"])
    check_null(news_title, Message.edit_news["title_error"], user, callback=insert_news)
    for i in type_results:
        print(Fore.BLUE + "\n%s. %s" % (i[0], i[1]))
    type_id = get_id(type_results, Message.edit_news["type_id_error"], Message.edit_news["type_id"])
    # 临时
    content_id = 1
    is_top = get_is_top()
    handle_save(news_service.insert_news, news_title, user["user_id"], type_id, content_id, is_top)

    time_sleep(3)
    cls()
    print(Message.common_msg["success"])
    edit_news(user)


def edit_news_editor(user, page=1):
    """
    新闻编辑编辑新闻
    :param user: 新闻编辑身份信息
    :param page: 当前页码
    :return: none
    """
    page = page
    results = news_service.get_all_news(page)
    pages = news_service.count_all_pages()
    edit_list_data(user, results, page, pages, Message.edit_news["news_id"],
                   Message.edit_news["news_id_error"], edit_news_editor_input,
                   edit_news_editor, edit_news)


def edit_news_editor_input(user, newses, index, page):
    """
    新闻编辑编辑新闻输入页面
    :param user: 新闻编辑身份信息
    :param newses: 全部新闻查询结果集
    :param index: 用户输入编号
    :param page: 当前页码
    :return:
    """
    news_id = newses[index - 1][0]
    news_info = news_service.get_news_for_edit(news_id)
    type_info = type_service.get_all_type()

    print(Message.edit_news["old_news_title"] % news_info[0][0])
    new_news_title = input(Message.edit_news["new_news_title"])
    check_null(new_news_title, Message.edit_news["title_error"], user, newses, index, page,
               callback=edit_news_editor_input)

    for i in type_info:
        print(Fore.BLUE + "\n%s. %s" % (i[0], i[1]))

    new_type_id = get_id(type_info, Message.edit_news["type_id_error"], Message.edit_news["type_id"])
    new_is_top = get_is_top()
    # TODO 新闻内容
    content_id = 1
    handle_save(news_service.edit_news, new_news_title, new_type_id, content_id, new_is_top, news_id)

    time_sleep(3)
    cls()
    print(Message.common_msg["success"])
    edit_news_editor(user, page)


if __name__ == "__main__":
    cls()
    start()
