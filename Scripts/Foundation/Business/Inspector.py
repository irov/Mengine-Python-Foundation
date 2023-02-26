class Inspector(object):
    def valid(self, bank):
        return True
        pass

    def inspect(self, bank):
        pass
    pass

class InspectorChange(Inspector):
    def __init__(self):
        self.cb = None
        pass

    def initialize(self, cb):
        self.cb = cb
        pass

    def inspect(self, bank):
        self.cb(bank)

        return True
        pass
    pass

class InspectorEmpty(Inspector):
    def __init__(self):
        self.cb = None
        pass

    def initialize(self, cb):
        self.cb = cb
        pass

    def inspect(self, bank):
        if bank.isEmpty() is False:
            return
            pass

        self.cb(bank)

        return False
        pass
    pass

class InspectorFull(Inspector):
    def __init__(self):
        self.cb = None
        pass

    def initialize(self, cb):
        self.cb = cb
        pass

    def inspect(self, bank):
        if bank.isFull() is False:
            return
            pass

        self.cb(bank)

        return False
        pass
    pass

class InspectorResource(Inspector):
    def __init__(self):
        self.compares_LT = {}
        self.compares_LE = {}
        self.compares_EQ = {}
        self.compares_NE = {}
        self.compares_GT = {}
        self.compares_GE = {}

        self.cb = None
        pass

    def initialize(self, compares, cb):
        self.compares_LT = compares.get("LT", {})  # <
        self.compares_LE = compares.get("LE", {})  # <=
        self.compares_EQ = compares.get("EQ", {})  # ==
        self.compares_NE = compares.get("NE", {})  # !=
        self.compares_GT = compares.get("GT", {})  # >
        self.compares_GE = compares.get("GE", {})  # >=

        self.cb = cb
        pass

    def valid(self, bank):
        if bank.checkResources(self.compares_LT) is False:
            return False
            pass

        if bank.checkResources(self.compares_LE) is False:
            return False
            pass

        if bank.checkResources(self.compares_EQ) is False:
            return False
            pass

        if bank.checkResources(self.compares_NE) is False:
            return False
            pass

        if bank.checkResources(self.compares_GT) is False:
            return False
            pass

        if bank.checkResources(self.compares_GE) is False:
            return False
            pass

        return True
        pass

    def inspect(self, bank):
        resources = bank.viewResources()

        for key, value in self.compares_LT.iteritems():
            resource = resources[key]

            if resource >= value:
                return
                pass
            pass

        for key, value in self.compares_LE.iteritems():
            resource = resources[key]

            if resource > value:
                return
                pass
            pass

        for key, value in self.compares_EQ.iteritems():
            resource = resources[key]

            if resource != value:
                return
                pass
            pass

        for key, value in self.compares_NE.iteritems():
            resource = resources[key]

            if resource == value:
                return
                pass
            pass

        for key, value in self.compares_GT.iteritems():
            resource = resources[key]

            if resource <= value:
                return
                pass
            pass

        for key, value in self.compares_GE.iteritems():
            resource = resources[key]

            if resource < value:
                return
                pass
            pass

        self.cb(bank)

        return False
        pass
    pass