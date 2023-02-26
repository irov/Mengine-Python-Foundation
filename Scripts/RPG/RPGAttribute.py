class RPGAttribute(object):
    def __init__(self, value):
        self.value = value
        self.bases = {}
        self.multiply = {}
        self.power = {}
        self.pure = {}

        self.total = value
        self.invalidate = False
        self.event = Event("Attribute")
        pass

    def calcTotal(self):
        if self.invalidate is True:
            self.__updateTotal()
            pass

        return self.total
        pass

    def __updateTotal(self):
        self.invalidate = False

        total_base = 0.0
        for value in self.bases.itervalues():
            if isinstance(value, RPGAttribute) is True:
                value = value.calcTotal()
                pass

            total_base += value
            pass

        total_multiply = 0.0
        for value in self.multiply.itervalues():
            if isinstance(value, RPGAttribute) is True:
                value = value.calcTotal()
                pass

            total_multiply += value
            pass

        if total_multiply >= 0.0:
            total_multiply = 1.0 + total_multiply
            pass
        else:
            total_multiply = 1.0 / (1.0 - total_multiply)
            pass

        total_power = 1.0
        for value in self.power.itervalues():
            if isinstance(value, RPGAttribute) is True:
                value = value.calcTotal()
                pass

            total_power *= value
            pass

        total_pure = 0.0
        for value in self.pure.itervalues():
            if isinstance(value, RPGAttribute) is True:
                value = value.calcTotal()
                pass

            total_pure += value
            pass

        self.total = (self.value + total_base) * total_multiply * total_power + total_pure
        pass

    def setValue(self, value):
        self.value = value

        self.invalidate = True
        self.event(self)
        pass

    def getValue(self):
        return self.value
        pass

    def setBase(self, tag, value):
        self.bases[tag] = value

        self.invalidate = True
        self.event(self)
        pass

    def setMultiply(self, tag, value):
        self.multiply[tag] = value

        self.invalidate = True
        self.event(self)
        pass

    def setPower(self, tag, value):
        self.power[tag] = value

        self.invalidate = True
        self.event(self)
        pass

    def setPure(self, tag, value):
        self.pure[tag] = value

        self.invalidate = True
        self.event(self)
        pass

    def getBase(self, tag):
        value = self.bases[tag]

        return value
        pass

    def getMultiply(self, tag):
        value = self.multiply[tag]

        return value
        pass

    def getPower(self, tag):
        value = self.power[tag]

        return value
        pass

    def getPure(self, tag):
        value = self.pure[tag]

        return value
        pass

    def removeBase(self, tag):
        if tag not in self.bases:
            return False
            pass

        del self.bases[tag]

        self.invalidate = True
        self.event(self)

        return True
        pass

    def removeMultiply(self, tag):
        if tag not in self.multiply:
            return False
            pass

        del self.multiply[tag]

        self.invalidate = True
        self.event(self)

        return True
        pass

    def removePower(self, tag):
        if tag not in self.power:
            return False
            pass

        del self.power[tag]

        self.invalidate = True
        self.event(self)

        return True
        pass

    def removePure(self, tag):
        if tag not in self.pure:
            return False
            pass

        del self.pure[tag]

        self.invalidate = True
        self.event(self)

        return True
        pass

    def addObserver(self, fn, *args):
        observer = self.event.addObserver(fn, *args)

        return observer
        pass

    def removeObserver(self, observer):
        self.event.removeObserver(observer)
        pass

    def getStringValue(self):
        return "(%s + %s) * %s * %s + %s" % (self.value, [value for value in self.bases.itervalues()], [value for value in self.multiply.itervalues()], [value for value in self.power.itervalues()], [value for value in self.pure.itervalues()])
        pass
    pass