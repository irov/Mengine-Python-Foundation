class Capture(object):
    __slots__ = "args", "kwargs"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        pass

    def setValue(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        pass

    def getArgs(self):
        return self.args

    def getKwargs(self):
        return self.kwargs
    pass