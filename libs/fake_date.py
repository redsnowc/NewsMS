from faker import Faker

from model.connection_pool import pool
from service.user_service import UserService

f_cn = Faker("zh-cn")
sql = """
    INSERT INTO t_news(title, editor_id, type_id, content_id, is_top, create_time, update_time, state)
    values(%s, %s, %s, %s, %s, %s, %s, %s)
"""


def fake_news():
    try:
        con = pool.get_connection()
        con.start_transaction()
        cursor = con.cursor()
        for i in range(0, 20):
            date = f_cn.date()
            cursor.execute(sql, ("新闻标题" + str(i + 1), 2, 1, i + 1, 1, date, date, "待审批"))
        con.commit()
    except Exception as e:
        if "con" in dir():
            con.rollback()
        print(e)
    finally:
        if "con" in dir():
            con.close()


def fake_other():
    s = UserService()
    s.add_user("admin", "1234", "admin@admin.com", 1)
    s.add_user("editor", "1234", "editor@editor.com", 1)
    try:
        con = pool.get_connection()
        con.start_transaction()
        cursor = con.cursor()
        cursor.execute("INSERT INTO `t_role` VALUES ('2', '新闻编辑');")
        cursor.execute("INSERT INTO `t_role` VALUES ('1', '管理员');")
        cursor.execute("INSERT INTO `t_type` VALUES ('2', '体育');")
        cursor.execute("INSERT INTO `t_type` VALUES ('5', '历史');")
        cursor.execute("INSERT INTO `t_type` VALUES ('4', '娱乐');")
        cursor.execute("INSERT INTO `t_type` VALUES ('3', '科技');")
        cursor.execute("INSERT INTO `t_type` VALUES ('1', '要闻');")
        con.commit()
    except Exception as e:
        if "con" in dir():
            con.rollback()
        print(e)
    finally:
        if "con" in dir():
            con.close()


def create_table():
    con = pool.get_connection()

    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS `t_news`")
    cursor.execute("""
        CREATE TABLE `t_news` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `title` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
            `editor_id` int(10) unsigned NOT NULL,
            `type_id` int(10) unsigned NOT NULL,
            `content_id` char(12) COLLATE utf8mb4_general_ci NOT NULL,
            `is_top` tinyint(3) unsigned NOT NULL,
            `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `state` enum('草稿','待审批','已审批','隐藏') COLLATE utf8mb4_general_ci NOT NULL,
            PRIMARY KEY (`id`),
            KEY `editor_id` (`editor_id`),
            KEY `type_id` (`type_id`),
            KEY `state` (`state`),
            KEY `create_time` (`create_time`),
            KEY `is_top` (`is_top`)
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS `t_type`;")
    cursor.execute("""
        CREATE TABLE `t_type` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `type` varchar(20) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `type` (`type`)
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS `t_user`;")
    cursor.execute("""
        CREATE TABLE `t_user` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `username` varchar(20) NOT NULL,
            `password` varchar(500) NOT NULL,
            `email` varchar(100) NOT NULL,
            `role_id` int(10) unsigned NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `username` (`username`),
            KEY `username_2` (`username`)
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS `t_role`;")
    cursor.execute("""
       CREATE TABLE `t_role` (
            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
            `role` varchar(20) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `role` (`role`)
        );  
    """)


if __name__ == "__main__":
    # fake_news()
    create_table()
    fake_news()
    fake_other()
