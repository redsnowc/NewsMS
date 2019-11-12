from model.news_dao import NewsDao


class NewsService:

    def __init__(self):
        self.news_dao = NewsDao()

    # 获取待审核新闻
    def get_padding_news(self, page):
        results = self.news_dao.get_pending_news(page)
        return results

    # 获取待审核新闻的总页数
    def count_padding_pages(self):
        pages = self.news_dao.count_pending_pages()
        return int(pages[0][0])

    # 执行审核新闻操作
    def approval_news(self, news_id):
        self.news_dao.approval_news(news_id)

    # 获取所有新闻
    def get_all_news(self, page):
        results = self.news_dao.get_all_news(page)
        return results

    # 获取所有新闻页数
    def count_all_pages(self):
        pages = self.news_dao.count_all_pages()
        return int(pages[0][0])

    # 删除新闻
    def delete_news(self, news_id):
        self.news_dao.delete_news(news_id)


if __name__ == "__main__":
    n = NewsService()
