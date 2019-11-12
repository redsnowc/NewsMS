"""
处理所有的命令行提示信息
"""
from colorama import Fore, Back, Style


class Message:
    common_msg = {
        "exit": "\nGoodbye!\n",
        "error": Fore.RED + "\n!WARING: 输入有误，请重新重新输入",
        "logout": Fore.GREEN + "已登出！",
        "prompt": Style.RESET_ALL + "请输入指令: ",
        "prev_error": Fore.RED + "!WARING: 已经是第一页！",
        "next_error": Fore.RED + "!WARING: 已经是最后一页",
             }

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
    }

    login_msg = {
        "username": Style.RESET_ALL + "请输入用户名: ",
        "username_error": Fore.RED + "!WARING: 用户名不能为空\n",
        "password": Style.RESET_ALL + "请输入密码: ",
        "pwd_error":  Fore.RED + "!WARING: 密码不能为空\n",
        "login_error": Fore.RED + "!WARING: 登陆失败",
    }

    manage_msg = {
        "option_admin": Fore.GREEN + """
1. 新闻管理

2. 用户管理
        """,
        "option_editor": Fore.GREEN + """
1. 新闻编辑
            """,
        "leave": Fore.RED + """
---------------------

back. 退出登录

exit. 退出系统

---------------------
        """
    }

    manage_news_msg = {
        "option": Fore.GREEN + """
1. 审批新闻

2. 删除信息
        """,
        "leave": Fore.RED + """
---------------------

back. 返回上一层
        """
    }

    approval_news_msg = {
        "leave": Fore.RED + """
back. 返回上一层

prev. 上一页

next. 下一页
        """,
        "approval_success": Fore.GREEN + "审核成功！",
        "news_id_error": Fore.RED + "!WARING: 新闻编号输入有误！",
        "prompt": Style.RESET_ALL + "请输入新闻编号: ",
    }
