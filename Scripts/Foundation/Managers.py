from Foundation.Manager import Manager

class Managers(object):
    s_managers = {}

    @staticmethod
    def onInitialize():
        return True

    @staticmethod
    def onFinalize():
        for name, manager in Managers.s_managers.iteritems():
            manager.onFinalize()

        Managers.s_managers = {}
        pass

    @staticmethod
    def importManager(module, name):
        manager = Managers.s_managers.get(name)

        if manager is not None:
            return manager

        new_manager = Utils.importType(module, name)

        if new_manager is None:
            Trace.log("Manager", 0, "Bootstrapper.importManager: invalid import %s:%s" % (module, name))

            return None

        if issubclass(new_manager, Manager) is False:
            Trace.log("Manager", 0, "Bootstrapper.importManager: manager '%s' is not subclass of Manager" % name)

            return None

        Manager.s__allowInitialize = True

        if new_manager.onInitialize() is False:
            Trace.log("Manager", 0, "Bootstrapper.importManager: manager '%s' invalid initialize" % name)

            return None

        Manager.s__allowInitialize = False

        Managers.s_managers[name] = new_manager

        return new_manager

    @staticmethod
    def removeManager(name):
        manager = Managers.s_managers.get(name)

        if manager is None:
            Trace.log("Manager", 0, "Managers.removeManager: manager '%s' not found" % name)
            return False

        if issubclass(manager, Manager) is True:
            manager.onFinalize()

        del Managers.s_managers[name]

        return True