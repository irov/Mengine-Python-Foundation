class Capture(object):
    __slots__ = "type", "args", "kwargs"

    def __init__(self, type, *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs
        pass

    def setValue(self, type, *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs
        pass

    def getType(self):
        return self.type

    def getArgs(self):
        return self.args

    def getKwargs(self):
        return self.kwargs
    pass