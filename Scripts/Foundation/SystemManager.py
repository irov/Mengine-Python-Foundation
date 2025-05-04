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
            system.onFinalize()

        SystemManager.systems = {}
        SystemManager.systemTypes = {}

    @staticmethod
    def addSystemType(name, systemType):
        if name in SystemManager.systemTypes:
            Trace.log("System", 0, "SystemManager.addSystemType: override system %s type %s [old type %s]" % (name, systemType, SystemManager.systemTypes[name]))

        SystemManager.systemTypes[name] = systemType

    @staticmethod
    def importSystem(module, name):
        Type = Utils.importType(module, name)

        if Type is None:
            Trace.log("System", 0, "SystemManager.importSystem: invalid import module '%s:%s'" % (module, name))
            return None

        SystemManager.addSystemType(name, Type)

        return Type

    @staticmethod
    def availableSystem(type, **params):
        if type not in SystemManager.systemTypes:
            Trace.log("System", 0, "SystemManager.availableSystem: not found system %s type %s" % (type, SystemManager.systemTypes))
            return False

        systemType = SystemManager.systemTypes[type]

        if systemType.available(params) is False:
            return False

        return True

    @staticmethod
    def createSystem(name, type, **params):
        if type not in SystemManager.systemTypes:
            Trace.log("System", 0, "SystemManager.createSystem: not found system %s type %s" % (name, type))
            return None
            pass

        Trace.msg_dev("SystemManager.createSystem [%s]" % (type))

        systemType = SystemManager.systemTypes[type]

        sys = systemType()
        sys.setName(name)
        sys.setType(type)
        sys.onParams(params)

        if sys.onInitialize() is False:
            Trace.log("System", 0, "SystemManager.createSystem %s:%s invalid initialize" % (name, type))
            return None

        SystemManager.systems[name] = sys

        return sys

    @staticmethod
    def runSystem(name, type, **params):
        sys = SystemManager.createSystem(name, type, **params)

        if sys is None:
            return False

        SystemManager.systems[name] = sys

        Trace.msg_dev("SystemManager.runSystem [%s]" % (type))

        if sys.run() is False:
            return False

        return sys

    @staticmethod
    def hasSystem(name):
        if name not in SystemManager.systems:
            return False
        return True

    @staticmethod
    def getSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.getSystem system %s not found" % (name))
            return None

        return SystemManager.systems[name]

    @staticmethod
    def stopSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.stopSystem not found system '%s'" % (name))
            return False

        sys = SystemManager.systems.get(name)
        sys.stop()

        Trace.msg_dev("SystemManager.stopSystem [%s]" % (sys.getType()))

        return True

    @staticmethod
    def getSystems():
        return SystemManager.systems

    @staticmethod
    def removeSystem(name):
        if name not in SystemManager.systems:
            Trace.log("System", 0, "SystemManager.removeSystem not found system '%s'" % (name))
            return False
            pass

        sys = SystemManager.systems.pop(name)
        sys.onFinalize()

        return True

    @staticmethod
    def _onSave():
        dict_save = {}
        for system in SystemManager.systems.itervalues():
            system.onSave(dict_save)

        return dict_save

    @staticmethod
    def _onLoad(dict_save):
        for system in SystemManager.systems.itervalues():
            system.onLoad(dict_save)
