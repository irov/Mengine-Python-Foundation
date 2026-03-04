from Foundation.Manager import Manager

class Managers(object):
    s_managers = {}
    s_manager_lists = []

    @staticmethod
    def onInitialize():
        return True

    @staticmethod
    def onFinalize():
        if _DEVELOPMENT is True:
            for name, manager in Managers.s_managers.iteritems():
                Trace.log("Manager", 0, "Managers.onFinalize: manager '%s' finalize..." % name)
                pass

        Managers.s_managers = {}
        pass

    @staticmethod
    def getManager(module, name):
        manager = Managers.s_managers.get((module, name))

        return manager

    @staticmethod
    def importManager(module, name):
        manager = Managers.s_managers.get(name)

        if manager is not None:
            return manager

        new_manager = Utils.importType(module, name)

        if new_manager is None:
            Trace.log("Manager", 0, "Bootstrapper.importManager: invalid import %s:%s" % (module, name))

            return None

        if _DEVELOPMENT is True:
            if issubclass(new_manager, Manager) is False:
                Trace.log("Manager", 0, "Bootstrapper.importManager: manager '%s' is not subclass of Manager" % name)

                return None

        Manager.s__allowInitialize = True

        if new_manager.onInitialize() is False:
            Trace.log("Manager", 0, "Bootstrapper.importManager: manager '%s' invalid initialize" % name)

            return None

        Manager.s__allowInitialize = False

        Managers.s_managers[(module, name)] = new_manager

        return new_manager

    @staticmethod
    def removeManager(module, name):
        print "Managers.removeManager: module %s name %s" % name

        manager = Managers.s_managers.get((module, name))

        if manager is None:
            Trace.log("Manager", 0, "Managers.removeManager: manager '%s' not found" % name)
            return False

        manager.onFinalize()

        del Managers.s_managers[name]

        return True