from model.news_dao import NewsDao
from model.redis_news_dao import RedisNewsDao
from model.mongo_news_dao import MongoNewsDao


class NewsService:

    def __init__(self):
        self.news_dao = NewsDao()
        self.redis_news_dao = RedisNewsDao()
        self.mongo_news_dao = MongoNewsDao()

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

    # 添加新闻
    def insert_news(self, title, editor_id, type_id, content, is_top):
        document = self.mongo_news_dao.insert(title, content)
        content_id = str(document.inserted_id)
        self.news_dao.insert_news(title, editor_id, type_id, content_id, is_top)

    # 查找新闻详细记录
    def get_news_detail(self, news_id):
        result = self.news_dao.get_news_detail(news_id)
        return result

    # 将新闻缓存至 redis
    def cache_news(self, news_id, title, username, type_name, content, is_top, create_time):
        self.redis_news_dao.insert_news(news_id, title, username, type_name, content,
                                        is_top, create_time)

    # 从缓存中删除新闻
    def delete_news_redis(self, news_id):
        self.redis_news_dao.delete_news(news_id)

    # 根据需要修改的新闻 id 查询新闻纪录
    def get_news_for_edit(self, news_id):
        result = self.news_dao.get_news_for_edit(news_id)
        return result

    # 修改新闻
    def edit_news(self, title, type_id, content_id, is_top, news_id):
        self.news_dao.edit_news(title, type_id, content_id, is_top, news_id)
        # 修改新闻后，需要将新闻从缓存中删除
        self.delete_news_redis(news_id)


if __name__ == "__main__":
    n = NewsService()
    a = n.get_news_for_edit(10)
    print(a)
