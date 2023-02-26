def make_enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    pass

class enum_metaclass(type):
    def __call__(self, key):
        for k in self.__dict__:
            v = self.__dict__[k]
            if v == key: return k
            pass

        return None
        pass

    def __getitem__(self, key):
        return getattr(self, key)
        pass

    pass

class Enum(object):
    __metaclass__ = enum_metaclass
    pass