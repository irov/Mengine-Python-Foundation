from Foundation.Task.Task import Task

class MixinObserver(Task):
    __slots__ = "observer", "observerWait", "observerSkip"

    def __init__(self):
        super(MixinObserver, self).__init__()

        self.observer = None
        self.observerWait = True
        self.observerSkip = False
        pass

    def addObserver(self, identity, fn, wait=True):
        if self.observer is not None:
            Trace.log("Object", 0, "MixinObserver.addObserver '%s' already add" % (identity))
            return

        self.observerWait = wait
        self.observer = Notification.addObserverExt(identity, fn, Cb=Functor(self.__onObserverComplete, None))
        pass

    def addObserverFilter(self, identity, fn, obj_filter, wait=True):
        if self.observer is not None:
            Trace.log("Object", 0, "MixinObserver.addObserverFilter '%s' already add" % (identity))
            return

        def __filter(obj, *args, **kwargs):
            if obj is not obj_filter:
                return False

            return True

        self.observerWait = wait
        self.observer = Notification.addObserverExt(identity, fn, Cb=Functor(self.__onObserverComplete, obj_filter), Filter=__filter)
        pass

    def removeObserver(self):
        if self.observer is None:
            Trace.log("Task", 0, "MixinObserver.removeObserver invalid remove observer %s" % (self))
            return

        Notification.removeObserver(self.observer)

        self.observer = None
        pass

    def setObserverSkip(self, skip):
        self.observerSkip = skip
        pass

    def __onObserverComplete(self, obj_filter):
        self.observer = None

        self._onObserverComplete(obj_filter)

        if self.observerWait is True:
            if self.observerSkip is False:
                self.complete()
                pass
            else:
                self.skip()
                pass
            pass

        return True

    def _onObserverComplete(self, obj_filter):
        pass

    def _onFinally(self):
        super(MixinObserver, self)._onFinally()

        if self.observerWait is True and self.observer is not None:
            self.removeObserver()
            pass
        pass
    pass