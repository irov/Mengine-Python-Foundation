from Foundation.DatabaseManager import DatabaseManager
from Notification import Notification

class PrefetchGroupManager(object):
    s_groups = []
    s_onInitializeRenderResourcesComplete = False
    s_onInitializeRenderResourcesObserver = None

    @staticmethod
    def onInitialize():
        PrefetchGroupManager.s_onInitializeRenderResourcesComplete = False
        PrefetchGroupManager.s_onInitializeRenderResourcesObserver = Notification.addObserver(Notificator.onInitializeRenderResources, PrefetchGroupManager.__onInitializeRenderResources)
        PrefetchGroupManager.s_onFinalizeRenderResources = Notification.addObserver(Notificator.onFinalizeRenderResources, PrefetchGroupManager.__onFinalizeRenderResources)
        pass

    @staticmethod
    def onFinalize():
        Notification.removeObserver(PrefetchGroupManager.s_onInitializeRenderResourcesObserver)
        Notification.removeObserver(PrefetchGroupManager.s_onFinalizeRenderResources)
        PrefetchGroupManager.s_onInitializeRenderResourcesObserver = None
        PrefetchGroupManager.s_onFinalizeRenderResources = None

        PrefetchGroupManager.s_groups = []
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            GroupName = record.get("GroupName")
            Prefetch = record.get("Prefetch", 1)
            Tag = record.get("Tag")

            PrefetchGroupManager.s_groups.append((GroupName, Prefetch, Tag))
            pass

        return True
        pass

    @staticmethod
    def __onInitializeRenderResources():
        PrefetchGroupManager.s_onInitializeRenderResourcesComplete = True

        PrefetchGroupManager.prefetchGroupsTagged(None)

        return True
        pass

    @staticmethod
    def __onFinalizeRenderResources():
        PrefetchGroupManager.s_onInitializeRenderResourcesComplete = False

        PrefetchGroupManager.unfetchGroupsTagged(None)

        return True
        pass

    @staticmethod
    def mergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
                pass
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)
                pass
            pass

        UnionGroups = PrefetchGroups.union(UnfetchGroups)
        UnfetchGroups.difference(UnionGroups)
        PrefetchGroups.difference(UnionGroups)

        for GroupName in UnfetchGroups:
            PrefetchGroupManager.unfetchGroup(GroupName)
            pass

        for GroupName in PrefetchGroups:
            PrefetchGroupManager.prefetchGroup(GroupName)
            pass
        pass

    @staticmethod
    def getMergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
                pass
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)
                pass
            pass

        UnionGroups = PrefetchGroups.union(UnfetchGroups)
        UnfetchGroups.difference(UnionGroups)
        PrefetchGroups.difference(UnionGroups)

        return UnfetchGroups, PrefetchGroups
        pass

    @staticmethod
    def prefetchGroupsTagged(Tag):
        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if GroupTag != Tag:
                continue
                pass

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.incrementResources(GroupName)
                pass
            elif Prefetch == 2:
                def __cb(successful, GroupName):
                    pass

                Mengine.prefetchResources(GroupName, __cb, GroupName)
                pass
            pass
        pass

    @staticmethod
    def unfetchGroupsTagged(Tag):
        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if GroupTag != Tag:
                continue
                pass

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
                pass
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)
                pass
            pass
        pass

    @staticmethod
    def prefetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.incrementResources(GroupName)
                pass
            elif Prefetch == 2:
                def __cb(successful, GroupName):
                    pass

                Mengine.prefetchResources(GroupName, __cb, GroupName)
                pass
            pass
        pass

    @staticmethod
    def unfetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
                pass
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)
                pass
            pass
        pass
    pass