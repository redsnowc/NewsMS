"""
处理所有的命令行提示信息
"""
from colorama import Fore, Back, Style


class Message:
    start_msg = {
        "welcome": Fore.CYAN +
                   """
=======================

你好，欢迎进入新闻管理系统

=======================
""" + Fore.GREEN +
                   """
1. 登录系统
2. 退出系统
    """,
        "prompt": Style.RESET_ALL + "请输入指令: ",
        "exit": "Goodbye!",
        "error": Fore.RED + "\n!WARING: 输入有误，请重新重新输入"
    }

    login_msg = {
        "username": Style.RESET_ALL + "请输入用户名: ",
        "username_error": Fore.RED + "!WARING: 用户名不能为空\n",
        "password": Style.RESET_ALL + "请输入密码: ",
        "pwd_error":  Fore.RED + "!WARING: 密码不能为空\n",
        "login_error": Fore.RED + "!WARING: 登陆失败",
    }
