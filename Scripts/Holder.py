class Holder(object):
    __slots__ = "value"

    def __init__(self, value=None):
        self.value = value
        pass

    def set(self, value):
        self.value = value
        pass

    def get(self):
        return self.value
        pass
    pass