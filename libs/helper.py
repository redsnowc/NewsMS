import os
import sys
import time

from getpass import getpass

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
    pass


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


def check_null(value, error_msg, callback=None, need_cls=True):
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
        handle_error(error_msg, callback, need_cls=need_cls)


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
    暂时操作
    :param second: 暂停时间(秒)
    :return: none
    """
    print("%s秒后自动跳转..." % second)
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
