from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

import Inspector

class InspectorManager(object):
    s_compares = {}

    @staticmethod
    def _onInitialize():
        return True

    @staticmethod
    def _onFinalize():
        InspectorManager.s_compares = {}
        pass

    @staticmethod
    def addCompare(name, compare):
        if name in InspectorManager.s_compares:
            Trace.log("Manager", 0, "InspectorManager.addCompare %s already exist" % (name))
            return
            pass

        InspectorManager.s_compares[name] = compare
        pass

    @staticmethod
    def getCompare(name):
        if name not in InspectorManager.s_compares:
            Trace.log("Manager", 0, "InspectorManager.getCompare %s not exist" % (name))
            return None
            pass

        compare = InspectorManager.s_compares[name]

        return compare
        pass

    @staticmethod
    def loadParams(module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        for ORM in ORMs:
            InspectorManager.addCompare(ORM.Name, ORM)
            pass

        return True
        pass

    @staticmethod
    def createInspector(name, cb):
        compare = InspectorManager.getCompare(name)
        if compare is None:
            Trace.log("Manager", 0, "InspectorManager.createInspector %s not exist" % (name))
            return
            pass

        inspector = Inspector.InspectorResource()
        if inspector.initialize(compare.Comp, cb) is False:
            return None
            pass

        return inspector
        pass

    @staticmethod
    def createInspectorEmpty(cb):
        inspector = Inspector.InspectorEmpty()

        if inspector.initialize(cb) is False:
            return None
            pass

        return inspector
        pass

    @staticmethod
    def createInspectorFull(cb):
        inspector = Inspector.InspectorFull()

        if inspector.initialize(cb) is False:
            return None
            pass

        return inspector
        pass

    @staticmethod
    def createInspectorChange(cb):
        inspector = Inspector.InspectorChange()

        if inspector.initialize(cb) is False:
            return None
            pass

        return inspector
        pass
    pass