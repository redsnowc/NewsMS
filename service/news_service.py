from model.news_dao import NewsDao


class NewsService:
    def __init__(self):
        self.news_dao = NewsDao()

    def get_padding_news(self, page, page_size):
        results = self.news_dao.get_pending_news(page, page_size)
        return results

    def get_padding_pages(self):
        pages = self.news_dao.count_pending_pages()
        return int(pages[0][0])

    def approval_news(self, news_id):
        self.news_dao.approval_news(news_id)


if __name__ == "__main__":
    u = NewsService()
    a = u.get_padding_news(1, 10)
    b = u.get_padding_pages()
    print(a)
    print(b)
