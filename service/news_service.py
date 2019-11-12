from model.news_dao import NewsDao


class NewsService:
    def __init__(self):
        self.news_dao = NewsDao()

    def get_padding_news(self, page):
        results = self.news_dao.get_pending_news(page)
        return results

    def count_padding_pages(self):
        pages = self.news_dao.count_pending_pages()
        return int(pages[0][0])

    def approval_news(self, news_id):
        self.news_dao.approval_news(news_id)

    def get_all_news(self, page):
        results = self.news_dao.get_all_news(page)
        return results

    def count_all_pages(self):
        pages = self.news_dao.count_all_pages()
        return int(pages[0][0])

    def delete_news(self, news_id):
        self.news_dao.delete_news(news_id)


if __name__ == "__main__":
    u = NewsService()
    # a = u.get_padding_news(1)
    # b = u.count_padding_pages()
    a = u.count_all_pages()
    b = u.get_all_news(1)
    print(a)
    print(len(b))
