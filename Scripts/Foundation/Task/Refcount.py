class Refcount(object):
    __slots__ = "value", "event"

    def __init__(self, name):
        self.value = 0
        self.event = Event(name)
        pass

    def getValue(self):
        return self.value
        pass

    def getEvent(self):
        return self.event
        pass

    def incref(self):
        self.value += 1

        if self.value == 1:
            self.event(True)
            pass
        pass

    def decref(self):
        if self.value == 0:
            Trace.log("Task", 0, "Refcount %s invalid decref zero count!" % (self.event.getName()))

            return
            pass

        self.value -= 1

        if self.value == 0:
            self.event(False)
            pass
        pass

    def isKeep(self):
        return self.value != 0
        pass
    pass