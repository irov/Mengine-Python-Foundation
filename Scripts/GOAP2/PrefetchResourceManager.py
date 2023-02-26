from GOAP2.DatabaseManager import DatabaseManager
from Notification import Notification

class PrefetchResourceManager(object):
    s_resources = []
    s_onInitializeRenderResourcesObserver = None

    @staticmethod
    def onInitialize():
        PrefetchResourceManager.s_onInitializeRenderResourcesObserver = Notification.addObserver(Notificator.onInitializeRenderResources, PrefetchResourceManager.__prefetchGroups)
        PrefetchResourceManager.s_onFinalizeRenderResourcesObserver = Notification.addObserver(Notificator.onFinalizeRenderResources, PrefetchResourceManager.__unfetchGroups)
        pass

    @staticmethod
    def onFinalize():
        Notification.removeObserver(PrefetchResourceManager.s_onInitializeRenderResourcesObserver)
        Notification.removeObserver(PrefetchResourceManager.s_onFinalizeRenderResourcesObserver)
        PrefetchResourceManager.s_onInitializeRenderResourcesObserver = None
        PrefetchResourceManager.s_onFinalizeRenderResourcesObserver = None

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
        pass

    @staticmethod
    def __prefetchGroups():
        for ResourceName, Prefetch in PrefetchResourceManager.s_resources:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.directResourceCompile(ResourceName)
                pass
            pass

        return True
        pass

    @staticmethod
    def __unfetchGroups():
        for ResourceName, Prefetch in PrefetchResourceManager.s_resources:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.directResourceRelease(ResourceName)
                pass
            pass

        return True
        pass
    pass