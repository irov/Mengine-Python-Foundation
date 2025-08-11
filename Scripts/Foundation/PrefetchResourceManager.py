from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

class PrefetchResourceManager(Manager):
    s_resources = []

    @staticmethod
    def _onInitialize():
        PrefetchResourceManager.addObserver(Notificator.onInitializeRenderResources, PrefetchResourceManager.__prefetchGroups)
        PrefetchResourceManager.addObserver(Notificator.onFinalizeRenderResources, PrefetchResourceManager.__unfetchGroups)
        pass

    @staticmethod
    def _onFinalize():
        PrefetchResourceManager.s_resources = []
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            ResourceName = record.get("ResourceName")
            Prefetch = record.get("Prefetch", 1)

            PrefetchResourceManager.s_resources.append((ResourceName, Prefetch))
            pass

        return True

    @staticmethod
    def __prefetchGroups():
        for ResourceName, Prefetch in PrefetchResourceManager.s_resources:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.directResourceCompile(ResourceName)
                pass
            pass

        return True

    @staticmethod
    def __unfetchGroups():
        for ResourceName, Prefetch in PrefetchResourceManager.s_resources:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.directResourceRelease(ResourceName)
                pass
            pass

        return True
    pass