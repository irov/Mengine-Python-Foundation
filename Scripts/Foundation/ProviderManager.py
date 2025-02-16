class ProviderManager(object):
    s_providers = {}

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
    def onFinalize():
        for provider in ProviderManager.s_providers.values():
            provider.removeProvider()
        ProviderManager.s_providers = {}
