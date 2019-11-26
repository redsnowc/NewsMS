from libs.helper import execute_select_sql


class TypeDao:
    def __init__(self):
        self.get_all_type_sql = """
            SELECT id, type FROM t_type
            ORDER BY id
        """

    # 获取全部 type 表数据
    def get_all_type(self):
        results = execute_select_sql(self.get_all_type_sql)
        return results


if __name__ == "__main__":
    t = TypeDao()
    a = t.get_all_type()
    print(a)
