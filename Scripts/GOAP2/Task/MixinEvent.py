from GOAP2.Task.Task import Task

class MixinEvent(Task):
    __metaclass__ = baseslots("event", "eventFn", "eventSkip")

    def __init__(self):
        super(MixinEvent, self).__init__()

        self.event = None
        self.eventFn = None

        self.eventSkip = False
        pass

    def addEvent(self, event, fn):
        if self.event is not None:
            Trace.log("Task", 0, "MixinEvent.addEvent %s already add event %s" % (self.event, self.eventFn))
            return
            pass

        self.event = event
        self.eventFn = fn

        self.event += self.__eventComplete
        pass

    def removeEvent(self):
        if self.event is None:
            Trace.log("Task", 0, "MixinEvent.removeEvent %s already remove %s" % (self, self.eventFn))
            return
            pass

        self.event -= self.__eventComplete

        self.event = None
        self.eventFn = None
        pass

    def setEventSkip(self, skip):
        self.eventSkip = skip
        pass

    def __eventComplete(self, *args, **kwargs):
        try:
            result = self.eventFn(*args, **kwargs)
        except TypeError as ex:
            Trace.log("Task", 0, "MixinEvent.__eventComplete %s event fn %s:%s except %s" % (self.event.name, self.eventFn.__module__, self.eventFn.__name__, ex))
            return
            pass

        if isinstance(result, bool) is False:
            Trace.log("Task", 0, "MixinEvent.__eventComplete %s event fn %s mast return boolean[True|False] but return %s" % (self.event.name, self.eventFn, result))
            return
            pass

        if result is False:
            return
            pass

        self.removeEvent()

        self._onEventComplete()

        if self.eventSkip is False:
            self.complete()
            pass
        else:
            self.skip()
            pass
        pass

    def _onEventComplete(self):
        pass

    def _onFinally(self):
        super(MixinEvent, self)._onFinally()

        # Trace.log("Task", 0, "%s"%(self))

        if self.event is not None:
            self.removeEvent()
            pass
        pass
    pass