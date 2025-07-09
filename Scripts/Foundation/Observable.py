from Foundation.Initializer import Initializer

class Observable(Initializer):
    __metaclass__ = baseslots("__observers", "__events")

    def __init__(self):
        super(Observable, self).__init__()

        self.__observers = []
        self.__events = []
        pass

    def addObserver(self, identity, fn, *args, **kwargs):
        observer = Notification.addObserver(identity, fn, *args, **kwargs)

        if observer is None:
            return

        self.__observers.append(observer)

        return observer
        pass

    def removeObserver(self, observer):
        if observer not in self.__observers:
            Trace.log("Base", 0, "{}.removeObserver - observer not found in {}".format(self.__class__.__name__, self))
            return

        Notification.removeObserver(observer)

        self.__observers.remove(observer)
        pass

    def addEvent(self, ev, fn, *args, **kwargs):
        observer = ev.addObserver(fn, *args, **kwargs)

        desc = (ev, observer)
        self.__events.append(desc)

        return desc

    def removeEvent(self, desc):
        if desc not in self.__events:
            Trace.log("System", 0, "{}.removeEventObserver - observer not found in {}".format(self.__class__.__name__, self))
            return

        ev, observer = desc

        ev.removeObserver(observer)
        self.__events.remove((ev, observer))
        pass

    def _onInitialize(self, obj):
        super(Observable, self)._onInitialize(obj)
        pass

    def _onFinalize(self):
        super(Observable, self)._onFinalize()

        for observer in self.__observers:
            Notification.removeObserver(observer)

        self.__observers = []

        for event, observer in self.__events:
            event.removeObserver(observer)

        self.__events = []
        pass
    pass