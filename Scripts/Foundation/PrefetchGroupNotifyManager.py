from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

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
        PrefetchGroupNotifyManager.s_prefetch_list = {}
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_NO
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
        if PrefetchTag == UnfetchTag:
            return

        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)

        CommonGroups = PrefetchGroups.intersection(UnfetchGroups)
        UnfetchGroups.difference_update(CommonGroups)
        PrefetchGroups.difference_update(CommonGroups)

        for GroupName in UnfetchGroups:
            PrefetchGroupNotifyManager.unfetchGroup(GroupName)

        for GroupName in PrefetchGroups:
            PrefetchGroupNotifyManager.prefetchGroup(GroupName)

    @staticmethod
    def getMergeGroupsTagged(PrefetchTag, UnfetchTag):
        if PrefetchTag == UnfetchTag:
            return set(), set()

        PrefetchGroups = set()
        UnfetchGroups = set()

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag == PrefetchTag:
                PrefetchGroups.add(GroupName)
            elif GroupTag == UnfetchTag:
                UnfetchGroups.add(GroupName)

        CommonGroups = PrefetchGroups.intersection(UnfetchGroups)
        UnfetchGroups.difference_update(CommonGroups)
        PrefetchGroups.difference_update(CommonGroups)

        return UnfetchGroups, PrefetchGroups

    @staticmethod
    def prefetchGroupsTagged(Tag):
        pending_groups = []

        for GroupName, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if GroupTag != Tag:
                continue

            if Prefetch != 2:
                continue

            pending_groups.append(GroupName)

        has_pending_groups = len(pending_groups) != 0
        PrefetchGroupNotifyManager.s_prefetch_list[Tag] = pending_groups

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
                    groups = PrefetchGroupNotifyManager.s_prefetch_list.get(tag)

                    if groups is None:
                        return

                    if group_name not in groups:
                        return

                    groups.remove(group_name)
                    Notification.notify(Notificator.onPrefetchGroupsTaggedComplete, tag, group_name, successful)

                    if len(groups) != 0:
                        return

                    PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
                    Notification.notify(Notificator.onPrefetchGroupsTaggedFinished, tag)

                if Mengine.prefetchResources(GroupName, __cb, Tag, GroupName) is False:
                    __cb(False, Tag, GroupName)

        if has_pending_groups is True:
            return

        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_FINISHED
        Notification.notify(Notificator.onPrefetchGroupsTaggedFinished, Tag)

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
        for group_name, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if group_name != GroupName:
                continue

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
        for group_name, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if group_name != GroupName:
                continue

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                Mengine.decrementResources(GroupName)
            elif Prefetch == 2:
                Mengine.unfetchResources(GroupName)
