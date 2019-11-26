from model.type_dao import TypeDao


class TypeService:
    def __init__(self):
        self.type_dao = TypeDao()

    def get_all_type(self):
        results = self.type_dao.get_all_type()
        return results
