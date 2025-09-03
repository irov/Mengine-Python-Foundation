from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

import Inspector

class InspectorManager(Manager):
    s_compares = {}

    @staticmethod
    def _onInitialize(*args):
        pass

    @staticmethod
    def _onFinalize():
        InspectorManager.s_compares = {}
        pass

    @staticmethod
    def addCompare(name, compare):
        if name in InspectorManager.s_compares:
            Trace.log("Manager", 0, "InspectorManager.addCompare %s already exist" % (name))
            return

        InspectorManager.s_compares[name] = compare
        pass

    @staticmethod
    def getCompare(name):
        if name not in InspectorManager.s_compares:
            Trace.log("Manager", 0, "InspectorManager.getCompare %s not exist" % (name))
            return None

        compare = InspectorManager.s_compares[name]

        return compare

    @staticmethod
    def loadParams(module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        for ORM in ORMs:
            InspectorManager.addCompare(ORM.Name, ORM)
            pass

        return True

    @staticmethod
    def createInspector(name, cb):
        compare = InspectorManager.getCompare(name)
        if compare is None:
            Trace.log("Manager", 0, "InspectorManager.createInspector %s not exist" % (name))
            return

        inspector = Inspector.InspectorResource()
        if inspector.initialize(compare.Comp, cb) is False:
            return None

        return inspector

    @staticmethod
    def createInspectorEmpty(cb):
        inspector = Inspector.InspectorEmpty()

        if inspector.initialize(cb) is False:
            return None

        return inspector

    @staticmethod
    def createInspectorFull(cb):
        inspector = Inspector.InspectorFull()

        if inspector.initialize(cb) is False:
            return None

        return inspector

    @staticmethod
    def createInspectorChange(cb):
        inspector = Inspector.InspectorChange()

        if inspector.initialize(cb) is False:
            return None

        return inspector
    pass