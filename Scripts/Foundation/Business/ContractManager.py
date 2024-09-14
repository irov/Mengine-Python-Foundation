from Foundation.DatabaseManager import DatabaseManager

from Contract import Contract

class ContractManager(object):
    s_contracts = {}

    s_scheduler = None

    @staticmethod
    def onInitialize():
        ContractManager.s_scheduler = Mengine.createScheduler()

        return True
        pass

    @staticmethod
    def onFinalize():
        if ContractManager.s_scheduler is not None:
            Mengine.destroyScheduler(ContractManager.s_scheduler)
            ContractManager.s_scheduler = None
        pass

    @staticmethod
    def createContract(name, bank_from, bank_to):
        terms = ContractManager.s_contracts.get(name)

        if terms is None:
            return None

        contract = Contract()

        if contract.initialize(name, ContractManager.s_scheduler, terms.Time, terms.Term, bank_from, bank_to) is False:
            Trace.log("Manager", 0, "ContractManager.createContract %s invalid initialize" % (name))
            return None
            pass

        return contract
        pass

    @staticmethod
    def loadParams(module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        if ORMs is None:
            return False
            pass

        for ORM in ORMs:
            ContractManager.s_contracts[ORM.Name] = ORM
            pass

        return True
        pass
        pass