from GOAP2.Identity import Identity

class Notification(object):
    notifies = {}

    class Observer(object):
        __slots__ = "identity", "fn", "filter", "cb"

        def __init__(self, identity, fn, args, kwargs, filter, cb):
            self.identity = identity
            self.fn = FunctorStore(fn, args, kwargs)
            self.filter = filter
            self.cb = cb
            pass

        def __del__(self):
            if self.fn is not None:
                Trace.log("Manager", 0, "Notification.Observer %s:%s not remove" % (self.identity, self.fn))
                pass
            pass

        def isValid(self):
            if self.fn is None:
                return False
                pass

            return True
            pass

        def release(self):
            self.fn = None
            self.filter = None
            self.cb = None
            pass
        pass

    @staticmethod
    def onFinalize():
        observers_bin = []
        for observers in Notification.notifies.itervalues():
            for observer in observers:
                observers_bin.append(observer)

        for observer in observers_bin:
            Notification.removeObserver(observer)

        Notification.notifies = {}
        pass

    @staticmethod
    def validateIdentity(identity):
        return isinstance(identity, Identity)
        pass

    @staticmethod
    def notify(identity, *args, **kwargs):
        if _DEVELOPMENT is True:
            if Notification.validateIdentity(identity) is False:
                Trace.log("Notification", 0, "Notification.notify not have identity %s" % (identity))
                return False
                pass
            pass

        if identity not in Notification.notifies:
            return False
            pass

        observers = Notification.notifies[identity]

        for observer in observers[:]:
            if observer.fn is None:
                continue
                pass

            if observer.filter is not None:
                if observer.filter(*args, **kwargs) is False:
                    continue
                    pass
                pass

            value = observer.fn(*args, **kwargs)

            if isinstance(value, bool) is False:
                Trace.log("Notification", 0, "Notification %s called function must return boolean value, but return %s in %s" % (identity.value, value, observer.fn))
                pass

            if value is True:
                cb = observer.cb
                Notification.removeObserver(observer)

                if cb is not None:
                    cb()
                    pass
                pass
            pass

        return True
        pass

    @staticmethod
    def addObserver(identity, fn, *args, **kwargs):
        if _DEVELOPMENT is True:
            if Notification.validateIdentity(identity) is False:
                Trace.log("Notification", 0, "Notification.addObserver not have identity %s" % (identity))
                return
                pass
            pass
        #
        if identity not in Notification.notifies:
            Notification.notifies[identity] = []
            pass

        observers = Notification.notifies[identity]

        if _DEVELOPMENT is True:
            if args is not None and isinstance(args, tuple) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s args is not tuple" % (identity))
                return
                pass

            if kwargs is not None and isinstance(kwargs, dict) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s kwargs is not dict" % (identity))
                return
                pass

            if callable(fn) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s fn is not callable" % (identity))
                return
                pass

            for observer in observers:
                if observer.fn is fn:
                    Trace.log("Notification", 0, "Notification.addObserver %s is already exist" % (identity))
                    return
                pass
            pass

        observer = Notification.Observer(identity, fn, args, kwargs, None, None)

        observers.append(observer)

        return observer
        pass

    @staticmethod
    def addObserverExt(identity, fn, args=(), kwargs={}, Filter=None, Cb=None):
        if _DEVELOPMENT is True:
            if Notification.validateIdentity(identity) is False:
                Trace.log("Notification", 0, "Notification.addObserver not have identity %s" % (identity))
                return
                pass
            pass
        #
        if identity not in Notification.notifies:
            Notification.notifies[identity] = []
            pass

        observers = Notification.notifies[identity]

        if _DEVELOPMENT is True:
            if args is not None and isinstance(args, tuple) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s args is not tuple" % (identity))
                return
                pass

            if kwargs is not None and isinstance(kwargs, dict) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s kwargs is not dict" % (identity))
                return
                pass

            if callable(fn) is False:
                Trace.log("Notification", 0, "Notification.addObserver %s fn is not callable" % (identity))
                return
                pass

            for observer in observers:
                if observer.fn is fn:
                    Trace.log("Notification", 0, "Notification.addObserver %s is already exist" % (identity))
                    return
                pass
            pass

        observer = Notification.Observer(identity, fn, args, kwargs, Filter, Cb)

        observers.append(observer)

        return observer
        pass

    @staticmethod
    def removeObserver(observer):
        if observer is None:
            return
            pass

        if observer.isValid() is False:
            return
            pass

        identity = observer.identity

        if _DEVELOPMENT is True:
            if Notification.validateIdentity(identity) is False:
                Trace.log("Notification", 0, "Notification.removeObserver not have identity %s" % (identity))
                return
                pass

            if identity not in Notification.notifies:
                Trace.log("Notification", 0, "Notification.removeObserver %s not found" % (identity.value))
                return
                pass
            pass

        observers = Notification.notifies[identity]

        try:
            observer.release()

            observers.remove(observer)
        except ValueError:
            Trace.log("Notification", 0, "Notification.unregObserver %s is already removed" % (identity))
            pass

        if len(observers) == 0:
            del Notification.notifies[identity]
            pass
        pass

    @staticmethod
    def hasObserver(identity, observer):
        if _DEVELOPMENT is True:
            if Notification.validateIdentity(identity) is False:
                Trace.log("Notification", 0, "Notification.hasObserver not have identity %s" % (identity))
                return False
                pass
            pass

        if identity not in Notification.notifies:
            return False
            pass

        observers = Notification.notifies[identity]

        return observer in observers
        pass
    pass