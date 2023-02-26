from GOAP2.DatabaseManager import DatabaseManager
from Notification import Notification

class PrefetchGroupNotifyManager(object):
    STATUS_NO = 0
    STATUS_START = 1
    STATUS_FINISHED = 2

    s_status = STATUS_NO
    s_prefetch_list = {}
    s_groups = []
    s_onInitializeRenderResourcesObserver = None

    @staticmethod
    def onInitialize():
        PrefetchGroupNotifyManager.s_onInitializeRenderResourcesObserver = Notification.addObserver(Notificator.onInitializeRenderResources, PrefetchGroupNotifyManager.__onInitializeRenderResources)
        PrefetchGroupNotifyManager.s_onFinalizeRenderResourcesObserver = Notification.addObserver(Notificator.onFinalizeRenderResources, PrefetchGroupNotifyManager.__onFinalizeRenderResources)
        pass

    @staticmethod
    def onFinalize():
        Notification.removeObserver(PrefetchGroupNotifyManager.s_onInitializeRenderResourcesObserver)
        Notification.removeObserver(PrefetchGroupManager.s_onFinalizeRenderResourcesObserver)
        PrefetchGroupNotifyManager.s_onInitializeRenderResourcesObserver = None
        PrefetchGroupNotifyManager.s_onFinalizeRenderResourcesObserver = None

        for GroupName, Prefetch, Tag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.decrementResources(GroupName)
                pass
            elif Prefetch == 2:
                Menge.unfetchResources(GroupName)
                pass
            pass

        PrefetchGroupNotifyManager.s_groups = []
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            GroupName = record.get("GroupName")
            Prefetch = record.get("Prefetch", 1)
            Tag = record.get("Tag")

            PrefetchGroupNotifyManager.s_groups.append((GroupName, Prefetch, Tag))
            pass

        return True
        pass

    @staticmethod
    def __onInitializeRenderResources():
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_START
        PrefetchGroupNotifyManager.prefetchGroupsTagged(None)
        return True
        pass

    @staticmethod
    def __onFinalizeRenderResources():
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
        PrefetchGroupNotifyManager.unfetchGroupsTagged(None)
        return True
        pass

    @staticmethod
    def mergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
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
            PrefetchGroupNotifyManager.unfetchGroup(GroupName)
            pass

        for GroupName in PrefetchGroups:
            PrefetchGroupNotifyManager.prefetchGroup(GroupName)
            pass
        pass

    @staticmethod
    def getMergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
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

        # for GroupName in UnfetchGroups:
        #     PrefetchGroupNotifyManager.unfetchGroup(GroupName)
        #     pass
        #
        # for GroupName in PrefetchGroups:
        #     PrefetchGroupNotifyManager.prefetchGroup(GroupName)
        #     pass

        return UnfetchGroups, PrefetchGroups
        pass

    @staticmethod
    def prefetchGroupsTagged(Tag):
        PrefetchGroupNotifyManager.s_prefetch_list[Tag] = []

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag != Tag:
                continue
                pass

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.incrementResources(GroupName)
                pass
            elif Prefetch == 2:
                def __cb(successful, Tag, GroupName):
                    if GroupName in PrefetchGroupNotifyManager.s_prefetch_list[Tag]:
                        PrefetchGroupNotifyManager.s_prefetch_list[Tag].remove(GroupName)
                        Notification.notify(Notificator.onPrefetchGroupsTaggedComplete, Tag, GroupName)
                        pass

                    if len(PrefetchGroupNotifyManager.s_prefetch_list[Tag]) == 0:
                        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
                        Notification.notify(Notificator.onPrefetchGroupsTaggedFinished, Tag)
                        pass
                    pass

                PrefetchGroupNotifyManager.s_prefetch_list[Tag].append(GroupName)
                if Menge.prefetchResources(GroupName, __cb, Tag, GroupName) is False:
                    PrefetchGroupNotifyManager.s_prefetch_list[Tag].remove(GroupName)
                    pass
                else:
                    pass
                pass
            pass
        pass

    @staticmethod
    def isPrefetchFinished():
        return PrefetchGroupNotifyManager.s_status is PrefetchGroupNotifyManager.STATUS_FINISHED
        pass

    @staticmethod
    def getPrefetchGroup(Tag):
        return PrefetchGroupNotifyManager.s_prefetch_list[Tag]
        pass

    @staticmethod
    def unfetchGroupsTagged(Tag):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag != Tag:
                continue
                pass

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.decrementResources(GroupName)
                pass
            elif Prefetch == 2:
                Menge.unfetchResources(GroupName)
                pass
            pass
        pass

    @staticmethod
    def prefetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.incrementResources(GroupName)
                pass
            elif Prefetch == 2:
                def __cb(successful, GroupName):
                    pass

                Menge.prefetchResources(GroupName, __cb, GroupName)
                pass
            pass
        pass

    @staticmethod
    def unfetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Menge.decrementResources(GroupName)
                pass
            elif Prefetch == 2:
                Menge.unfetchResources(GroupName)
                pass
            pass
        pass

    pass