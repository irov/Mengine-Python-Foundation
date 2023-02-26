class Event(object):
    __slots__ = "name", "observers"

    def __init__(self, name):
        self.name = name
        self.observers = []

    def getName(self):
        return self.name

    def addObserver(self, fn, *args, **kwargs):
        observer = FunctorStore(fn, args, kwargs)

        if observer in self.observers:
            Trace.log("Manager", 0, "Event: already exist observer %s" % self.name)
            return None

        self.observers.append(observer)

        return observer

    def removeObserver(self, observer):
        if observer not in self.observers:
            Trace.log("Manager", 0, "Event: observer %s doesn't exist" % self.name)
            return

        self.observers.remove(observer)

    def removeObservers(self):
        self.observers = []

    def __iadd__(self, observer):
        if observer in self.observers:
            Trace.log("Manager", 0, "Event: already exist observer %s" % self.name)
            return self

        self.observers.append(observer)

        return self

    def __isub__(self, observer):
        if observer not in self.observers:
            Trace.log("Manager", 0, "Event: observer %s doesn't exist " % self.name)
            return self

        self.observers.remove(observer)

        return self

    def __call__(self, *args, **kwargs):
        for observer in self.observers[:]:
            if observer not in self.observers:
                continue

            observer(*args, **kwargs)