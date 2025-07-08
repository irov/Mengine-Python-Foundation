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

    def __iter__(self):
        return iter(self.args)

    def __len__(self):
        return len(self.args)

    def __getitem__(self, idx):
        return self.args[idx]
    pass