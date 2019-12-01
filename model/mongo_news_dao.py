from model.connection_pool import client
from bson.objectid import ObjectId


class MongoNewsDao:
    def insert(self, title, content):
        try:
            document = client.vega.news.insert_one({"title": title, "content": content})
            return document
        except Exception as e:
            print(e)

    def update(self, mongo_id, title, content):
        try:
            client.vega.news.update_one(
                {"_id": ObjectId(mongo_id)},
                {"$set": {"title": title, "content": content}}
            )
        except Exception as e:
            print(e)

    def search_content_by_id(self, mongo_id):
        try:
            return client.vega.news.find_one({"_id": ObjectId(mongo_id)})["content"]
        except Exception as e:
            print(e)

    def delete_by_id(self, mongo_id):
        try:
            client.vega.news.delete_one({"_id": ObjectId(mongo_id)})
        except Exception as e:
            print(e)


if __name__ == "__main__":
    a = MongoNewsDao()
    r = a.search_content_by_id("5de38d9782d00988a78b1822")
    print(r)
