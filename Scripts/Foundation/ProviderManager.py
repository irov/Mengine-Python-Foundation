from Foundation.Manager import Manager

class ProviderManager(Manager):
    s_providers = {}

    @staticmethod
    def __addTaskSourceInjections(Type):
        from Foundation.Task.TaskGenerator import TaskSource

        for MethodName, TaskTypeOrScope, Kwds in Type.getTaskSourceInjections():
            TaskSource.injectionTaskDesc(MethodName, TaskTypeOrScope, **Kwds)
            pass
        pass

    @staticmethod
    def __removeTaskSourceInjections(Type):
        from Foundation.Task.TaskGenerator import TaskSource

        for MethodName, TaskTypeOrScope, Kwds in Type.getTaskSourceInjections():
            TaskSource.removeInjectionTaskDesc(MethodName)
            pass
        pass

    @staticmethod
    def importProviders(module, names):
        for name in names:
            ProviderManager.importProvider(module, name)

    @staticmethod
    def importProvider(module, name):
        Type = Utils.importType(module, name)
        if Type is None:
            return False

        ProviderManager.addProvider(name, Type)

        return True

    @staticmethod
    def addProvider(name, Type):
        Type.setDevProvider()
        ProviderManager.__addTaskSourceInjections(Type)
        ProviderManager.s_providers[name] = Type

    @staticmethod
    def getProvider(name):
        return ProviderManager.s_providers.get(name)

    @staticmethod
    def hasProvider(name):
        return name in ProviderManager.s_providers

    @staticmethod
    def setProvider(name, provider_name, methods):
        provider = ProviderManager.getProvider(name)

        if provider is None:
            Trace.log("Manager", 0, "Not found provider {!r}".format(name))
            return False

        provider.setProvider(provider_name, methods)
        return True

    @staticmethod
    def removeProvider(name):
        provider = ProviderManager.getProvider(name)

        if provider is None:
            Trace.log("Manager", 0, "Not found provider {!r}".format(name))
            return False

        provider.removeProvider()
        return True

    @staticmethod
    def _onFinalize():
        for provider in ProviderManager.s_providers.values():
            ProviderManager.__removeTaskSourceInjections(provider)
            provider.removeProvider()
            pass

        ProviderManager.s_providers = {}
        pass
