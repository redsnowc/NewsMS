from settings.settings import Config
from libs.helper import execute_select_sql


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

    def get_pending_news(self, page, page_size):
        results = execute_select_sql(self.get_news_sql, "待审批", (page - 1) * page_size, page_size)
        return results

    def count_pending_pages(self):
        pages = execute_select_sql(self.count_pages_sql, Config.page_size, "待审批")
        return pages


if __name__ == "__main__":
    a = NewsDao()
    a.get_pending_news(1, 10)
    a.count_pending_pages()


