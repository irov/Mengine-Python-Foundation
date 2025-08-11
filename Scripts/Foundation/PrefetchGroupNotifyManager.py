from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager
from Notification import Notification


class PrefetchGroupNotifyManager(Manager):
    STATUS_NO = 0
    STATUS_START = 1
    STATUS_FINISHED = 2

    s_status = STATUS_NO
    s_prefetch_list = {}
    s_groups = []

    @staticmethod
    def _onInitialize(*args):
        PrefetchGroupNotifyManager.addObserver(Notificator.onInitializeRenderResources, PrefetchGroupNotifyManager.__onInitializeRenderResources)
        PrefetchGroupNotifyManager.addObserver(Notificator.onFinalizeRenderResources, PrefetchGroupNotifyManager.__onFinalizeRenderResources)
        pass

    @staticmethod
    def _onFinalize():
        for GroupName, Prefetch, Tag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)

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

        return True

    @staticmethod
    def __onInitializeRenderResources():
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_START
        PrefetchGroupNotifyManager.prefetchGroupsTagged(None)

        return True

    @staticmethod
    def __onFinalizeRenderResources():
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
        PrefetchGroupNotifyManager.unfetchGroupsTagged(None)

        return True

    @staticmethod
    def mergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)

        UnionGroups = PrefetchGroups.union(UnfetchGroups)
        UnfetchGroups.difference(UnionGroups)
        PrefetchGroups.difference(UnionGroups)

        for GroupName in UnfetchGroups:
            PrefetchGroupNotifyManager.unfetchGroup(GroupName)

        for GroupName in PrefetchGroups:
            PrefetchGroupNotifyManager.prefetchGroup(GroupName)

    @staticmethod
    def getMergeGroupsTagged(PrefetchTag, UnfetchTag):
        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)

        UnionGroups = PrefetchGroups.union(UnfetchGroups)
        UnfetchGroups.difference(UnionGroups)
        PrefetchGroups.difference(UnionGroups)

        return UnfetchGroups, PrefetchGroups

    @staticmethod
    def prefetchGroupsTagged(Tag):
        PrefetchGroupNotifyManager.s_prefetch_list[Tag] = []

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag != Tag:
                continue

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                print "PrefetchGroupNotifyManager: incrementing resources for group '%s'" % GroupName
                Mengine.incrementResources(GroupName)
            elif Prefetch == 2:
                def __cb(successful, tag, group_name):
                    if group_name in PrefetchGroupNotifyManager.s_prefetch_list[tag]:
                        PrefetchGroupNotifyManager.s_prefetch_list[tag].remove(group_name)
                        Notification.notify(Notificator.onPrefetchGroupsTaggedComplete, tag, group_name, successful)

                    if len(PrefetchGroupNotifyManager.s_prefetch_list[tag]) == 0:
                        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
                        Notification.notify(Notificator.onPrefetchGroupsTaggedFinished, tag)

                PrefetchGroupNotifyManager.s_prefetch_list[Tag].append(GroupName)
                if Mengine.prefetchResources(GroupName, __cb, Tag, GroupName) is False:
                    __cb(False, Tag, GroupName)

    @staticmethod
    def isPrefetchFinished():
        return PrefetchGroupNotifyManager.s_status is PrefetchGroupNotifyManager.STATUS_FINISHED

    @staticmethod
    def getPrefetchGroup(Tag):
        return PrefetchGroupNotifyManager.s_prefetch_list[Tag]

    @staticmethod
    def unfetchGroupsTagged(Tag):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag != Tag:
                continue

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)

    @staticmethod
    def prefetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                print "PrefetchGroupNotifyManager: incrementing resources for group '%s'" % GroupName
                Mengine.incrementResources(GroupName)
            elif Prefetch == 2:
                def __cb(successful, GroupName):
                    pass

                Mengine.prefetchResources(GroupName, __cb, GroupName)

    @staticmethod
    def unfetchGroup(GroupName):
        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)
