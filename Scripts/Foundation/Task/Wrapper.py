class Wrapper(object):
    __slots__ = "value"

    def __init__(self, value):
        self.value = value
        pass

    def setValue(self, value):
        self.value = value
        pass

    def getValue(self):
        return self.value
        pass
    pass