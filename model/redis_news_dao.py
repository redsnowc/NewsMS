from .connection_pool import redis_pool
import redis


class RedisNewsDao:

    # 将新闻缓存至 redis
    def insert_news(self, news_id, title, username, type_name, content, is_top, create_time):
        r = redis.Redis(
            connection_pool=redis_pool
        )
        try:
            r.hmset(news_id, {
                "title": title,
                "author": username,
                "type": type_name,
                "content": content,
                "is_top": is_top,
                "create_time": create_time
            })
            if is_top == 0:
                r.expire(news_id, 24 * 60 * 60)
        except Exception as e:
            print(e)
        finally:
            del r

    # 从缓存中删除新闻
    def delete_news(self, news_id):
        r = redis.Redis(
            connection_pool=redis_pool
        )
        try:
            r.delete(news_id)
        except Exception as e:
            print(e)
        finally:
            del r
