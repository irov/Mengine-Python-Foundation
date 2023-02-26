from GOAP2.DatabaseManager import DatabaseManager

from Bank import Bank

class BankManager(object):
    s_wealthes = {}

    @staticmethod
    def onInitialize():
        return True
        pass

    @staticmethod
    def onFinalize():
        pass

    @staticmethod
    def addWealth(name, wealth):
        if name in BankManager.s_wealthes:
            Trace.log("Manager", 0, "BankManager.addWealth %s already exist" % (name))
            return
            pass

        BankManager.s_wealthes[name] = wealth
        pass

    @staticmethod
    def getWealth(name):
        if name not in BankManager.s_wealthes:
            Trace.log("Manager", 0, "BankManager.getWealth %s not exist" % (name))
            return None
            pass

        wealth = BankManager.s_wealthes[name]

        return wealth
        pass

    @staticmethod
    def loadParams(module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        if ORMs is None:
            return False
            pass

        for ORM in ORMs:
            BankManager.addWealth(ORM.Name, ORM)
            pass

        return True
        pass

    @staticmethod
    def createBank(name):
        wealth = BankManager.getWealth(name)
        if wealth is None:
            Trace.log("Manager", 0, "BankManager.createBank %s not exist" % (name))
            return None
            pass

        bank = Bank(name)

        if hasattr(wealth, "Resource") is False:
            Trace.log("Manager", 0, "BankManager.createBank %s wealth resource not exist" % (name))
            return None
            pass

        resource = wealth.Resource.copy()

        limit = {}
        if hasattr(wealth, "Limit") is True:
            limit = wealth.Limit.copy()
            pass

        if bank.initialize(resource, limit) is False:
            return None
            pass

        return bank
        pass
    pass