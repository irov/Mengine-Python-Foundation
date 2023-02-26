class Semaphore(object):
    __slots__ = "value", "event"

    def __init__(self, value, name):
        self.value = value
        self.event = Event(name)
        pass

    def getValue(self):
        return self.value
        pass

    def getEvent(self):
        return self.event
        pass

    def setValue(self, value):
        self.value = value

        self.event()
        pass

    def increfValue(self, value):
        self.value += value

        self.event()
        pass

    def equalValue(self, value):
        return self.value == value
        pass
    pass