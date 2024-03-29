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
        "leave": Fore.RED + """
back. 返回上一层

prev. 上一页

next. 下一页
            """,
        "success": Fore.GREEN + "操作成功！",
        "id_error": Fore.RED + "\n!WARING: 编号输入有误！",
        "username_error": Fore.RED + "\n!WARING: 用户名不能为空！",
        "pwd_error": Fore.RED + "\n!WARING: 密码不能为空！",
        "email_error": Fore.RED + "\n!WARING: 邮箱不能为空！",
        "email_invalid": Fore.RED + "\n!WARING: 不是有效邮箱！",
        "pwd_repeat": Style.RESET_ALL + "\n请再次输入密码: ",
        "equal_error": Fore.RED + "\n!WARING: 两次密码输入不一致！",
        "role_id": Style.RESET_ALL + "\n输入角色编号: ",
        "role_error": Fore.RED + "\n!WARING: 用户编号输入有误！",
        "save": Style.RESET_ALL + "\n是否保存？(Y/N): ",
        "saved": Style.RESET_ALL + "\n保存成功",
        "cancel": Style.RESET_ALL + "\n取消成功",
        "username": Style.RESET_ALL + "\n请输入用户名: ",
        "password": Style.RESET_ALL + "\n请输入密码: ",
        "username_duplicate": Fore.RED + "\n!WARING: 用户名已存在！",
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
        """,
        "child_leave": Fore.RED + """
---------------------

back. 返回上一层
        """,
    }

    manage_news_msg = {
        "option": Fore.GREEN + """
1. 审批新闻

2. 删除新闻
        """,
        "prompt": Style.RESET_ALL + "请输入新闻编号: "
    }

    manage_users = {
        "option": Fore.GREEN + """
1. 添加用户

2. 修改用户

3. 删除用户
        """,
        "prompt": Style.RESET_ALL + "请输入用户编号: "
    }

    edit_user = {
        "old_username": Style.RESET_ALL + "\n原用户名: %s",
        "new_username": Style.RESET_ALL + "\n新用户名: ",
        "new_pwd": Style.RESET_ALL + "\n请输入新密码: ",
        "old_email": Style.RESET_ALL + "\n原邮箱: %s",
        "new_email": Style.RESET_ALL + "\n新邮箱: ",
    }

    add_user = {
        "email": Style.RESET_ALL + "\n请输入邮箱: ",
    }

    edit_news = {
        "option": Fore.GREEN + """
1. 发表新闻

2. 编辑新闻
    """,
        "title": Style.RESET_ALL + "\n新闻标题: ",
        "type_id": Style.RESET_ALL + "\n新闻类型编号: ",
        "content_id": Style.RESET_ALL + "\n新闻内容编号: ",
        "is_top": Style.RESET_ALL + "\n新闻置顶级别(0-10): ",
        "title_error": Fore.RED + "\n!WARING: 新闻标题不能为空！",
        "type_id_error": Fore.RED + "\n!WARING: 新闻类型输入有误！",
        "is_top_error": Fore.RED + "\n!WARING: 置顶即便输入有误！",
        "news_id": Style.RESET_ALL + "\n请输入新闻编号: ",
        "news_id_error": Fore.RED + "\n!WARING: 新闻编号输入有误！",
        "old_news_title": Style.RESET_ALL + "\n原新闻标题: %s",
        "old_news_type": Style.RESET_ALL + "\n原新闻类型: %s",
        "old_news_top": Style.RESET_ALL + "\n原新闻置顶级别: %s",
        "new_news_title": Style.RESET_ALL + "\n新新闻标题: ",
        "new_news_type": Style.RESET_ALL + "\n新新闻类型: ",
        "new_news_top": Style.RESET_ALL + "\n新新闻置顶级别: ",
        "file_path": Style.RESET_ALL + "\n新闻文档路径: ",
        "file_path_error": Fore.RED + "\n!WARING: 新闻文档路径输入有误！",
    }

