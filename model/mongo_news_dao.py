from model.connection_pool import client


class MongoNewsDao:
    def insert(self, title, content):
        try:
            document = client.vega.news.insert_one({"title": title, "content": content})
            return document
        except Exception as e:
            print(e)

