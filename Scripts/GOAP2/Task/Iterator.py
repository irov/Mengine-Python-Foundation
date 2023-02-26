class Iterator(object):
    __slots__ = "value"

    def __init__(self, value):
        self.value = value
        pass

    def getValue(self):
        return self.value
        pass

    def setValue(self, value):
        self.value = value
        pass

    def incref(self, value):
        self.value += value
        pass

    def isEqual(self, value):
        return self.value == value
        pass
    pass