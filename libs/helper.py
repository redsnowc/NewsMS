import os
import sys
import time
import re

from getpass import getpass
from colorama import Fore

from model.connection_pool import mysql_pool
from message.message import Message


def execute_select_sql(sql, *args):
    """
    执行查询语句
    :param sql: sql 语句
    :param args: 传递给 sql 语句的参数
    :return: 查询结果
    """
    try:
        connection = mysql_pool.get_connection()
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
        connection = mysql_pool.get_connection()
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


def rocket(data_id, search_service, cache_service):
    """
    让数据缓存至 redis 数据库
    :param cache_service: 缓存数据的 service
    :param data_id: 数据的 id 值
    :param search_service: 获取数据的 service
    :return: none
    """
    result = search_service(data_id)[0]
    title = result[0]
    username = result[1]
    type_name = result[2]
    # 临时
    content = result[3]
    is_top = result[4]
    create_time = str(result[5])
    cache_service(data_id, title, username, type_name, content, is_top, create_time)


def slow(data_id, delete_service):
    """
    从缓存中删除数据
    :param data_id: 要删除缓存的 key 值
    :param delete_service: 删除缓存数据的 service
    :return: none
    """
    delete_service(data_id)


def handle_input(input_val, results, service, callback, user,
                 page, rocket_search_service, rocket_cache_service, rocket_delete_service):
    """
    处理输入分页编号的后续数据库操作
    :param rocket_delete_service: 从缓存中删除数据的 service
    :param rocket_cache_service: 将数据缓存至 redis 的 service
    :param rocket_search_service: 查询需要缓存到 redis 中数据的 service
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
        if rocket_search_service:
            rocket(data_id, rocket_search_service, rocket_cache_service)
        if rocket_delete_service:
            slow(data_id, rocket_delete_service)
        clear_screen()
        print(Message.common_msg["success"])
        callback(user, page)
    else:
        handle_error(Message.common_msg["id_error"], callback, user, page)


def display_judge(page, results, pages, service, callback, up_callback, user,
                  rocket_search_service=None, rocket_cache_service=None,
                  rocket_delete_service=None):
    """
    显示结果集并依据输入执行对应的数据库操作
    考虑到对于分页展示并需要通过编号操作的函数重复代码较多，所以将重复的部分再次抽离封装
    :param rocket_delete_service: 从缓存中删除数据的 service
    :param rocket_cache_service: 将数据缓存至 redis 的 service
    :param rocket_search_service: 查询需要缓存到 redis 中数据的 service
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
        handle_input(input_val, results, service, callback, user, page,
                     rocket_search_service, rocket_cache_service, rocket_delete_service)
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
    while True:
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
            print(Message.common_msg["equal_error"])
        else:
            break
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


def get_id(results, error_mag, prompt_msg):
    """
    获取 id，判断用户输入的 id 是否在正确的范围
    :param results: 查询结果集
    :param error_mag: 错误提示信息
    :param prompt_msg: 提示信息
    :return: 正确的 id
    """
    input_val = input(prompt_msg)
    id_range = [i[0] for i in results]
    if not input_val:
        input_val = input_cycle(input_val, error_mag, prompt_msg)
    while is_number(input_val) not in id_range:
        print(error_mag)
        input_val = input_cycle(input_val, error_mag, prompt_msg)
        if is_number(input_val) in id_range:
            break
    return is_number(input_val)


def handle_save(service, *args):
    """
    处理用户操作后是否保存操作
    :param service: 保存之后的 service 操作
    :param args: 不定参数，传递给 sql 语句做格式化字符串
    :return:
    """
    while True:
        input_vale = input(Message.common_msg["save"])
        if input_vale.lower() == "y":
            print(Message.common_msg["saved"])
            service(*args)
            break
        elif input_vale.lower() == "n":
            print(Message.common_msg["cancel"])
            break
        else:
            print(Message.common_msg["error"])


def get_is_top():
    """
    该函数专门用以处理 is_top 的输入值
    :return: is_top 的正确值
    """
    input_val = input(Message.edit_news["is_top"])
    is_top_range = [str(i) for i in range(0, 11)]
    if not input_val:
        input_val = input_cycle(input_val, Message.edit_news["is_top_error"], Message.edit_news["is_top"])
    while input_val not in is_top_range:
        print(Message.edit_news["is_top_error"])
        input_val = input_cycle(input_val, Message.edit_news["is_top_error"], Message.edit_news["is_top"])
        if input_val in is_top_range:
            break
    return is_number(input_val)


def edit_list_data(user, results, page, pages, prompt, error_msg,
                   input_callback, callback, upper_callback):
    """
    专门处理编辑用户或者编辑新闻
    :param user: 当前登录用户的身份信息
    :param results: 查询结果集
    :param page: 当前页码
    :param pages: 总页数
    :param prompt: 提示信息
    :param error_msg: 错误信息
    :param input_callback: 具体编辑输入函数
    :param callback: 回调，出现错误时重新执行当前函数
    :param upper_callback: 上一级函数
    :return: none
    """
    page = page
    list_results(page, results, pages)
    input_val = input(prompt)

    if is_number(input_val):
        index = is_number(input_val)
        if len(results) >= index >= 1:
            clear_screen()
            input_callback(user, results, index, page)
        else:
            handle_error(error_msg, callback, user, page)
    elif input_val == "back":
        clear_screen()
        upper_callback(user)
    elif input_val == "prev":
        page = prev_page(page, callback, user)
    elif input_val == "next":
        page = next_page(page, pages, callback, user)
    else:
        handle_error(Message.common_msg["error"], callback, user, page)


def get_file_path():
    input_val = input(Message.edit_news["file_path"])
    if not input_val:
        input_val = input_cycle(input_val, Message.edit_news["file_path_error"], Message.edit_news["file_path"])
    while input_val.rsplit(".", 1)[1] != "txt" or not os.path.isfile(input_val):
        print(Message.edit_news["file_path_error"])
        input_val = input_cycle(input_val, Message.edit_news["file_path_error"], Message.edit_news["file_path"])
        if input_val.rsplit('.', 1)[1] == "txt" and os.path.isfile(input_val):
            break
    return input_val


if __name__ == "__main__":
    a = get_file_path()
    print(a)
