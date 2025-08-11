from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

from Bank import Bank

class BankManager(Manager):
    s_wealthes = {}

    @staticmethod
    def _onInitialize():
        return True

    @staticmethod
    def _onFinalize():
        BankManager.s_wealthes = {}
        pass

    @staticmethod
    def addWealth(name, wealth):
        if name in BankManager.s_wealthes:
            Trace.log("Manager", 0, "BankManager.addWealth %s already exist" % (name))
            return

        BankManager.s_wealthes[name] = wealth
        pass

    @staticmethod
    def getWealth(name):
        if name not in BankManager.s_wealthes:
            Trace.log("Manager", 0, "BankManager.getWealth %s not exist" % (name))
            return None

        wealth = BankManager.s_wealthes[name]

        return wealth

    @staticmethod
    def loadParams(module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        if ORMs is None:
            return False

        for ORM in ORMs:
            BankManager.addWealth(ORM.Name, ORM)
            pass

        return True

    @staticmethod
    def createBank(name):
        wealth = BankManager.getWealth(name)
        if wealth is None:
            Trace.log("Manager", 0, "BankManager.createBank %s not exist" % (name))
            return None

        bank = Bank(name)

        if hasattr(wealth, "Resource") is False:
            Trace.log("Manager", 0, "BankManager.createBank %s wealth resource not exist" % (name))
            return None

        resource = wealth.Resource.copy()

        limit = {}
        if hasattr(wealth, "Limit") is True:
            limit = wealth.Limit.copy()
            pass

        if bank.initialize(resource, limit) is False:
            return None

        return bank
    pass