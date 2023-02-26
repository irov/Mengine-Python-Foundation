class Identity(object):
    __slots__ = "value"

    def __init__(self, value):
        self.value = value
        pass

    def __repr__(self):
        return self.value
        pass
    pass