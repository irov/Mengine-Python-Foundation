class MetaSealed(type):
    def __init__(cls, name, bases, dict):
        cls.__sealedMethods = set()
        super(MetaSealed, cls).__init__(name, bases, dict)
        for key, val in dict.iteritems():
            if isinstance(val, sealed):
                setattr(cls, key, val.method)
                cls.__sealedMethods.add(key)
            for b in bases:
                try:
                    if key in b.__sealedMethods:
                        raise TypeError("*%s.%s* is *sealed* and therefore may not be overriden in descendants" % (b.__name__, key))
                except AttributeError:
                    continue
                pass
            pass
        pass
    pass

class sealed(object):
    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):
        raise AssertionError("you may use *sealed* decorator only within *MetaClass* instances")
        pass
    pass