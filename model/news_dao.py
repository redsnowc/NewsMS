from datetime import datetime

from settings.settings import Config
from libs.helper import execute_select_sql, execute_other_sql


class NewsDao:
    def __init__(self):
        self.get_news_sql = """
            SELECT n.id, n.title, u.username, t.type
            FROM t_news n 
            JOIN t_type t 
            ON n.type_id = t.id
            JOIN t_user u 
            ON n.editor_id = u.id
            WHERE n.state = %s
            ORDER BY n.create_time DESC
            LIMIT %s, %s
        """
        self.count_pages_sql = """
            SELECT CEIL(COUNT(*) / %s) 
            FROM t_news
            WHERE state = %s
        """
        self.approval_news_sql = """
            UPDATE t_news
            SET state = "已审批"
            WHERE id = %s
        """
        self.delete_news_sql = """
            DELETE FROM t_news
            WHERE id = %s
        """
        self.insert_news_sql = """
            INSERT INTO t_news (title, editor_id, type_id, content_id, is_top, create_time, update_time, state)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.get_news_detail_sql = """
            SELECT n.title, u.username, t.type, n.content_id, n.is_top, n.create_time
            FROM t_news n
            JOIN t_type t 
            ON n.type_id = t.id
            JOIN t_user u 
            ON n.editor_id = u.id
            WHERE n.id = %s
        """
        self.get_news_for_edit_sql = """
            SELECT n.title, t.type, n.is_top
            FROM t_news n
            JOIN t_type t 
            ON n.type_id = t.id 
            WHERE n.id = %s 
        """
        self.edit_news_sql = """
            UPDATE t_news
            SET title = %s, type_id = %s, content_id = %s, is_top = %s, update_time = %s, state = %s
            WHERE id = %s
        """
        self.get_news_mongo_id = """
            SELECT content_id
            FROM t_news
            WHERE id = %s
        """

    # 获取所有待审批新闻
    def get_pending_news(self, page):
        results = execute_select_sql(self.get_news_sql, "待审批", (page - 1) * Config.page_size, Config.page_size)
        return results

    # 获取待审批新闻页数
    def count_pending_pages(self):
        pages = execute_select_sql(self.count_pages_sql, Config.page_size, "待审批")
        return pages

    # 执行审批新闻操作
    def approval_news(self, news_id):
        execute_other_sql(self.approval_news_sql, news_id)

    # 获取全部新闻
    def get_all_news(self, page):
        results = execute_select_sql(
            self.get_news_sql.replace("WHERE n.state = %s", ""), (page - 1) * Config.page_size, Config.page_size
        )
        return results

    # 计算全部新闻页数
    def count_all_pages(self):
        pages = execute_select_sql(
            self.count_pages_sql.replace("WHERE state = %s", ""), Config.page_size
        )
        return pages

    # 删除新闻
    def delete_news(self, news_id):
        execute_other_sql(self.delete_news_sql, news_id)

    # 插入新闻
    def insert_news(self, title, editor_id, type_id, content_id, is_top):
        now = datetime.now()
        execute_other_sql(self.insert_news_sql, title, editor_id, type_id, content_id, is_top, now, now, "待审批")

    # 查找新闻详细记录
    def get_news_detail(self, news_id):
        result = execute_select_sql(self.get_news_detail_sql, news_id)
        return result

    # 根据需要修改的新闻 id 查询新闻纪录
    def get_news_for_edit(self, news_id):
        result = execute_select_sql(self.get_news_for_edit_sql, news_id)
        return result

    # 修改新闻
    def edit_news(self, title, type_id, content_id, is_top, news_id):
        now = datetime.now()
        execute_other_sql(self.edit_news_sql, title, type_id, content_id, is_top, now, "待审批", news_id)

    # 搜索新闻内容 id 值
    def search_mongo_id(self, news_id):
        mongo_id = execute_select_sql(self.get_news_mongo_id, news_id)[0][0]
        return mongo_id


if __name__ == "__main__":
    a = NewsDao()
    r = a.search_mongo_id(24)
    print(r)
