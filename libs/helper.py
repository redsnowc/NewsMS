import os
import sys
import time
import re

from getpass import getpass
from colorama import Fore

from model.connection_pool import pool
from message.message import Message


def execute_select_sql(sql, *args):
    """
    执行查询语句
    :param sql: sql 语句
    :param args: 传递给 sql 语句的参数
    :return: 查询结果
    """
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [i for i in args])
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        if "connection" in dir():
            connection.close()


def execute_other_sql(sql, *args):
    """
    执行非查询语句，增删该都需要手动操作事务机制
    :param sql: sql 语句
    :param args: 传递给 sql 语句的参数
    :return: none
    """
    try:
        connection = pool.get_connection()
        connection.start_transaction()
        cursor = connection.cursor()
        cursor.execute(sql, [i for i in args])
        connection.commit()
    except Exception as e:
        if "connection" in dir():
            connection.rollback()
        print(e)
    finally:
        if "connection" in dir():
            connection.close()


def clear_screen():
    """
    处理不同平台的清屏命令
    :return: none
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")


def handle_error(error_msg, callback, *args, need_cls=True):
    """
    处理输入错误相关提示
    :param error_msg: 错误提示信息
    :param callback: 回调函数
    :param args: 回调函数参数
    :param need_cls: 是否需要清屏 default=True
    :return: none
    """
    if need_cls:
        clear_screen()
    print(error_msg)
    if callback:
        try:
            callback(*args)
        except TypeError as e:
            print(e)
    else:
        return False


def check_null(value, error_msg, *args, callback=None, need_cls=True):
    """
    判断空值
    :param value: 需要检查的值
    :param error_msg: 错误信息
    :param callback: 回调函数
    :param need_cls: 是否需要清屏 default=True
    :return: none
    """
    if not value:
        if need_cls:
            clear_screen()
        handle_error(error_msg, callback, *args, need_cls=need_cls)


def input_cycle(value, error_msg, prompt_msg, kind="common", need_cls=False):
    """
    循环执行 input 要求用户输入必填项
    :param value: 需要判断的值
    :param error_msg: 错误提示信息
    :param prompt_msg: 输入提示信息
    :param kind: 输入类型，default=common，可选值 password
    :param need_cls: 是否需要清屏 default=False
    :return: 用户输入的值
    """
    while not check_null(value, error_msg, need_cls=need_cls):
        if kind == "password":
            input_value = getpass(prompt_msg)
        else:
            input_value = input(prompt_msg)
        if input_value:
            return input_value


def exit_sys():
    """
    退出程序
    :return: none
    """
    print(Message.common_msg["exit"])
    sys.exit()


def log_out():
    """
    退出登录
    :return: none
    """
    clear_screen()
    print(Message.common_msg["logout"])
    from app import start
    start()


def time_sleep(second):
    """
    暂停操作
    :param second: 暂停时间(秒)
    :return: none
    """
    print("\n%s秒后自动跳转..." % second)
    count = 0
    while count < second:
        time.sleep(1)
        count += 1


def is_number(val):
    """
    判断字符串是不是整数
    :param val: 需要判断的字符串
    :return: False or 转换后的数字
    """
    try:
        int(val)
        return int(val)
    except ValueError:
        return False


def next_page(page, pages, callback, *args):
    """
    下一页操作
    :param page: 当前页
    :param pages: 总页数
    :param callback: 回调函数
    :param args: 回调函数可选参数
    :return: 翻页后的页码
    """
    if page == pages:
        handle_error(Message.common_msg["next_error"], callback, *args, page)
        return page
    else:
        page += 1
        clear_screen()
        callback(*args, page)
        return page


def prev_page(page, callback, *args):
    """
        上一页操作
        :param page: 当前页
        :param callback: 回调函数
        :param args: 回调函数可选参数
        :return: 翻页后的页码
        """
    if page == 1:
        handle_error(Message.common_msg["prev_error"], callback, *args, page)
        return page
    else:
        page -= 1
        clear_screen()
        callback(*args, page)
        return page


def list_results(page, results, pages):
    """
    列出查询结果集
    该函数通过循环生成模板字符串和格式化数据的方式渲染显示的数据
    :param page: 当前页码
    :param results: 查询结果集
    :param pages: 总页数
    :return: none
    """
    index = 1
    for i in results:
        length = len(i)
        str_tmp = "\n%s. "
        data = [index]
        for j in range(1, length):
            str_tmp += "%s "
            data.append(i[j])
        str_tmp += "\n"
        print(Fore.BLUE + str_tmp % tuple(data))
        index += 1
    print("---------------------\n")
    print("%s/%s\n" % (page, pages))
    print("---------------------")
    print(Message.common_msg["leave"])


def handle_input(input_val, results, service, callback, user, page):
    """
    处理输入分页编号的后续数据库操作
    :param input_val: 输入的编号
    :param results: 查询结果集
    :param service: service 处理函数
    :param callback: 回调函数
    :param user: 用户数据
    :param page: 当前页
    :return: none
    """
    index = is_number(input_val)
    if len(results) >= index >= 1:
        data_id = results[index - 1][0]
        service(data_id)
        clear_screen()
        print(Message.common_msg["success"])
        callback(user, page)
    else:
        handle_error(Message.common_msg["id_error"], callback, user, page)


def display_judge(page, results, pages, service, callback, up_callback, user):
    """
    显示结果集并依据输入执行对应的数据库操作
    考虑到对于分页展示并需要通过编号操作的函数重复代码较多，所以将重复的部分再次抽离封装
    :param page: 当前页码
    :param results: 查询结果集
    :param pages: 总页数
    :param service: service 处理函数
    :param callback: 回调函数 (调用当前页面)
    :param up_callback: 上层回调函数 (回到上层页面)
    :param user: 用户数据
    :return: none
    """
    list_results(page, results, pages)
    input_val = input(Message.manage_news_msg["prompt"])

    if is_number(input_val):
        handle_input(input_val, results, service, callback, user, page)
    elif input_val == "back":
        clear_screen()
        up_callback(user)
    elif input_val == "prev":
        page = prev_page(page, callback, user)
    elif input_val == "next":
        page = next_page(page, pages, callback, user)
    else:
        handle_error(Message.common_msg["error"], callback, user, page)


def get_password(pwd_msg):
    """
    获取密码，需判断密码不能为空，且两次输入一致
    :param pwd_msg: 密码输入框提示信息
    :return: 正确输入的密码
    """
    new_pwd = getpass(pwd_msg)
    if not new_pwd:
        new_pwd = input_cycle(
            new_pwd, Message.common_msg["pwd_error"], pwd_msg, kind="password"
        )

    repeat_pwd = getpass(Message.common_msg["pwd_repeat"])
    if not repeat_pwd:
        repeat_pwd = input_cycle(
            repeat_pwd, Message.common_msg["pwd_error"], Message.common_msg["pwd_repeat"], kind="password"
        )

    if repeat_pwd != new_pwd:
        handle_error(Message.common_msg["equal_error"], get_password, pwd_msg, need_cls=False)
    else:
        return new_pwd


def get_email(prompt):
    """
    依据正则判断邮箱是否正确，且邮箱不能为空
    :return: 正确输入的邮箱
    """
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    email = input(prompt)
    if not email:
        email = input_cycle(email, Message.common_msg["email_error"], prompt)
    while not re.match(regex, email):
        print(Message.common_msg["email_invalid"])
        email = input_cycle(email, Message.common_msg["email_error"], prompt)
        if re.match(regex, email):
            break
    return email


def get_role_id(role_info):
    """
    获取角色 id，判断用户输入的角色 id 是否在正确的范围
    :param role_info: 数据库中的角色信息
    :return: 正确的角色 id
    """
    input_val = input(Message.common_msg["role_id"])
    role_id = is_number(input_val)
    role_id_range = [i[0] for i in role_info]
    if role_id:
        if role_id in role_id_range:
            return role_id
    handle_error(Message.common_msg["role_error"], get_role_id, role_info, need_cls=False)


def handle_save(service, *args):
    """
    处理用户操作后是否保存操作
    :param service: 保存之后的 service 操作
    :param args: 不定参数，传递给 sql 语句做格式化字符串
    :return:
    """
    input_vale = input(Message.common_msg["save"])
    if input_vale.lower() == "y":
        print(Message.common_msg["saved"])
        service(*args)
    elif input_vale.lower() == "n":
        print(Message.common_msg["cancel"])
    else:
        handle_error(Message.common_msg["error"], handle_save, *args, need_cls=False)


def check_duplicate(value, service):
    """

    :param value:
    :param service:
    :return:
    """
    return service(value)
