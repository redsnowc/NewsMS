from faker import Faker

from model.connection_pool import pool


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


if __name__ == "__main__":
    fake_news()
