from Foundation.Manager import Manager

class SystemManager(Manager):
    systemTypes = {}
    systems = {}

    @staticmethod
    def _onInitialize():
        pass

    @staticmethod
    def _onFinalize():
        for system in SystemManager.systems.itervalues():
            if system.isRun() is True:
                system.stop()
                pass

            system.onFinalize()
            pass

        SystemManager.systems = {}
        SystemManager.systemTypes = {}
        pass

    @staticmethod
    def addSystemType(name, systemType):
        if name in SystemManager.systemTypes:
            Trace.log("System", 0, "SystemManager.addSystemType: override system %s type %s [old type %s]" % (name, systemType, SystemManager.systemTypes[name]))
            pass

        SystemManager.systemTypes[name] = systemType
        pass

    @staticmethod
    def importSystem(module, name):
        Type = Utils.importType(module, name)

        if Type is None:
            Trace.log("System", 0, "SystemManager.importSystem: invalid import module '%s:%s'" % (module, name))

            return None
            pass

        SystemManager.addSystemType(name, Type)

        return Type
        pass

    @staticmethod
    def createSystem(name, type, **params):
        if type not in SystemManager.systemTypes:
            Trace.log("System", 0, "SystemManager.createSystem: not found system %s type %s" % (name, type))
            return None
            pass

        if _DEVELOPMENT is True:
            print
            "SystemManager.createSystem [%s]" % (type)
            pass

        systemType = SystemManager.systemTypes[type]

        sys = systemType()
        sys.setName(name)
        sys.setType(type)
        sys.onParams(params)

        if sys.onInitialize() is False:
            Trace.log("System", 0, "SystemManager.createSystem %s:%s invalid initialize" % (name, type))
            return None
            pass

        SystemManager.systems[name] = sys

        return sys
        pass

    @staticmethod
    def runSystem(name, type, **params):
        sys = SystemManager.createSystem(name, type, **params)

        if sys is None:
            return None
            pass

        SystemManager.systems[name] = sys

        if _DEVELOPMENT is True:
            print
            "SystemManager.runSystem [%s]" % (type)
            pass

        if sys.run() is False:
            return None
            pass

        return sys
        pass

    @staticmethod
    def hasSystem(name):
        if name not in SystemManager.systems:
            return False
            pass

        return True
        pass

    @staticmethod
    def getSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.getSystem system %s not found" % (name))

            return None
            pass

        return SystemManager.systems[name]
        pass

    @staticmethod
    def stopSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.stopSystem not found system '%s'" % (name))
            return False
            pass

        sys = SystemManager.systems.get(name)

        sys.stop()

        if _DEVELOPMENT is True:
            print
            "SystemManager.stopSystem [%s]" % (sys.getType())
            pass

        return True
        pass

    @staticmethod
    def removeSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.removeSystem not found system '%s'" % (name))
            return False
            pass

        sys = SystemManager.systems.pop(name)
        sys.onFinalize()

        return True
        pass

    @staticmethod
    def _onSave():
        dict_save = {}
        for system in SystemManager.systems.itervalues():
            system.onSave(dict_save)
            pass

        return dict_save
        pass

    @staticmethod
    def _onLoad(dict_save):
        for system in SystemManager.systems.itervalues():
            system.onLoad(dict_save)
            pass
        pass
    pass