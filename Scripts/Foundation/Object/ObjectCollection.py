class ObjectCollection(object):
    __slot__ = "__list", "__dict"

    def __init__(self):
        self.__list = []
        self.__dict = {}
        pass

    def append(self, key, obj):
        self.__dict[key] = obj
        self.__list.append(obj)
        pass

    def get(self, key):
        obj = self.__dict.get(key)

        return obj

    def remove(self, key):
        value = self.__dict.pop(key)
        self.__list.remove(value)
        pass

    def getList(self):
        return self.__list

    def getDict(self):
        return self.__dict

    def length(self):
        return len(self.__list)

    def __contains__(self, key):
        return key in self.__dict

    def __iter__(self):
        return self.__list.__iter__()

    def __repr__(self):
        return self.__list.__repr__()

    def __add__(self, object_collection_addition):
        object_collection = ObjectCollection()
        object_collection.__list = self.getList() + object_collection_addition.getList()
        object_collection.__dict.update(self.getDict())
        object_collection.__dict.update(object_collection_addition.getDict())
        return object_collection
    pass