class Collector(object):
    def __init__(self, provider):
        self.provider = provider
        pass

    def __getattr__(self, name):
        value = self.provider(name)
        setattr(self, name, value)
        return value
        pass

    pass