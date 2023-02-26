class Bank(object):
    def __init__(self, Name):
        self.Name = Name

        self.resources = {}
        self.limited = {}

        self.reserves = []
        self.central = None

        self.inspectors = []
        pass

    def initialize(self, resources, limited={}):
        self.resources = resources
        self.limited = limited

        for key in self.resources:
            if key not in self.limited:
                self.limited[key] = -1
                pass
            pass

        for key in self.limited:
            if key not in self.resources:
                return False
                pass
            pass

        return True
        pass

    def addInspector(self, inspector):
        if inspector.valid(self) is False:
            return False
            pass

        self.inspectors.append(inspector)

        return True
        pass

    def removeInspector(self, inspector):
        self.inspectors.remove(inspector)
        pass

    def __setCentral(self, bank):
        self.central = bank
        pass

    def __getCentral(self):
        return self.central
        pass

    def addReserve(self, bank):
        reserve_central = bank.__getCentral()
        if reserve_central is not None:
            return False
            pass

        if bank.checkResources(self.resources) is False:
            return False
            pass

        bank.__setCentral(self)

        self.reserves.append(bank)

        self.__inspect()

        return True
        pass

    def removeReserve(self, bank):
        reserve_central = bank.__getCentral()

        if reserve_central is not self:
            return False
            pass

        if bank not in self.reserves:
            return False
            pass

        bank.__setCentral(None)

        self.reserves.remove(bank)

        self.__inspect()
        pass

    def viewResources(self):
        return self.resources
        pass

    def viewAllResources(self):
        all_resources = self.resources.copy()

        for reserve in self.reserves:
            reserve_resource = reserve.viewAllResources()

            for key, value in reserve_resource.iteritems():
                all_resources[key] += value
                pass
            pass

        return all_resources
        pass

    def incassate(self, bank):
        for key, value in self.resources.iteritems():
            test_value = bank.testResource(key, value)
            get_value = self.getResource(key, test_value)
            bank.addResource(key, get_value)
            pass
        pass

    def viewResourcesLimit(self):
        return self.limited
        pass

    def viewAllLimit(self):
        all_Limits = self.limited.copy()

        for reserve in self.reserves:
            reserve_Limit = reserve.viewAllLimit()

            for key, value in reserve_Limit.iteritems():
                all_Limits[key] += value
                pass
            pass

        return all_Limits
        pass

    def setResource(self, type, value):
        if type not in self.resources:
            return None
            pass

        if value < 0:
            return None
            pass

        change = 0

        if type in self.limited:
            lim = self.limited[type]

            if lim > 0 and value > lim:
                change = value - lim
                value = lim
                pass
            pass

        self.__setResource(type, value)

        return change
        pass

    def getLimit(self, type):
        if type not in self.limited:
            return None
            pass

        lim = self.limited[type]

        if lim < 0:
            return None
            pass

        return lim
        pass

    def viewResource(self, type):
        resources = self.viewAllResources()
        resource = resources[type]
        return resource
        pass

    def validResource(self, type, value):
        if type not in self.resources:
            return None
            pass

        testValue = self.viewResource(type)

        if testValue < value:
            return False
            pass

        return True
        pass

    def testResource(self, type, value):
        if type not in self.resources:
            return None
            pass

        lim = self.limited[type]

        resource = self.resources[type]

        if lim >= 0 and resource + value > lim:
            return lim - resource
            pass

        return value
        pass

    def isFull(self):
        resFullSelf = self.personalFull()
        resFullReserve = self.reservesFull()
        if resFullSelf is True and resFullReserve is True:
            return True
            pass
        return False
        pass

    def reservesFull(self):
        all_resources = self.viewAllResources()
        all_Limits = self.viewAllLimit()
        res = self.__resFull(all_resources, all_Limits)
        return res
        pass

    def personalFull(self):
        res = self.__resFull(self.resources, self.limited)
        return res
        pass

    def __resFull(self, DictRes, DictLimit):
        for key, value in DictRes.iteritems():
            lim = DictLimit[key]

            if lim < 0:
                return False
                pass

            if value != lim:
                return False
                pass
            pass

        return True
        pass

    def isEmpty(self):
        resEmptySelf = self.personalEmpty()
        resEmptyReserve = self.reservesEmpty()
        if resEmptySelf is True and resEmptyReserve is True:
            return True
            pass
        return False
        pass

    def reservesEmpty(self):
        all_resources = self.viewAllResources()
        res = self.__resEmpty(all_resources)
        return res
        pass

    def personalEmpty(self):
        res = self.__resEmpty(self.resources)
        return res
        pass

    def __resEmpty(self, DictRes):
        for value in DictRes.itervalues():
            if value > 0:
                return False
                pass
            pass
        return True
        pass

    def addResource(self, type, value):
        if type not in self.resources:
            Trace.trace()
            return None
            pass

        if value is None:
            Trace.trace()
            return None
            pass

        resource = self.resources[type]

        if resource is None:
            Trace.trace()
            return None
            pass

        if resource + value < 0:
            self.__setResource(type, 0)

            change = - (value + resource)

            return change
            pass

        if type in self.limited:
            lim = self.limited[type]

            if lim >= 0 and resource + value > lim:
                self.__setResource(type, lim)

                change = lim - resource

                return change
                pass
            pass

        self.__addResource(type, value)

        return 0
        pass

    def getResource(self, type, value):
        if type not in self.resources:
            return None
            pass

        resource = self.resources[type]

        if resource - value < 0:
            self.__setResource(type, 0)

            change = value - resource

            for reserve in self.reserves:
                reserve_change = reserve.getResource(type, change)

                if reserve_change is None:
                    return None
                    pass

                change -= reserve_change

                if change == 0:
                    break
                    pass
                pass

            return value - change
            pass

        self.__subResource(type, value)

        return value
        pass

    def checkResources(self, resources):
        for test_key, test_value in resources.iteritems():
            if test_key not in self.resources:
                return False
                pass
            pass

        return True
        pass

    def __setResource(self, type, value):
        self.resources[type] = value

        self.__inspect()
        pass

    def __addResource(self, type, value):
        self.resources[type] += value

        self.__inspect()
        pass

    def __subResource(self, type, value):
        self.resources[type] -= value

        self.__inspect()
        pass

    def __inspect(self):
        for inspector in self.inspectors[:]:
            if inspector.inspect(self) is False:
                self.inspectors.remove(inspector)
                pass
            pass

        if self.central is not None:
            self.central.__inspect()
            pass
        pass
    pass