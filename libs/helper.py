import os
import sys

from model.connection_pool import pool


def execute_select_sql(sql, *args):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [i for i in args])
        return cursor.fetchall()
    except Exception as e:
        print(e)


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


def handle_error(error_msg, callback, need_cls=True):
    """
    处理输入错误相关提示
    :param error_msg: 错误提示信息
    :param callback: 回调函数
    :param need_cls: 是否需要清屏
    :return: none
    """
    if need_cls:
        clear_screen()
    print(error_msg)
    if callback:
        try:
            callback()
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
    :param need_cls: 是否需要清屏
    :return: none
    """
    if not value:
        if need_cls:
            clear_screen()
        handle_error(error_msg, callback, need_cls)


def input_cycle(value, error_msg, prompt_msg, need_cls=False):
    """
    循环执行 input 要求用户输入必填项
    :param value: 需要判断的值
    :param error_msg: 错误提示信息
    :param prompt_msg: 输入提示信息
    :param need_cls: 是否需要清屏 default=False
    :return: 用户输入的值
    """
    while not check_null(value, error_msg, need_cls=need_cls):
        input_value = input(prompt_msg)
        if input_value:
            return input_value
