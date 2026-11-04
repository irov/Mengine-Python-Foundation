from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

class PrefetchGroupNotifyManager(Manager):
    STATUS_NO = 0
    STATUS_START = 1
    STATUS_FINISHED = 2

    s_status = STATUS_NO
    s_prefetch_list = {}
    s_groups = []
    s_active_groups = {}
    s_render_resources_initialized = False

    @staticmethod
    def _onInitialize(*args):
        PrefetchGroupNotifyManager.s_active_groups = {}
        PrefetchGroupNotifyManager.s_render_resources_initialized = False
        PrefetchGroupNotifyManager.addObserver(Notificator.onInitializeRenderResources, PrefetchGroupNotifyManager.__onInitializeRenderResources)
        PrefetchGroupNotifyManager.addObserver(Notificator.onFinalizeRenderResources, PrefetchGroupNotifyManager.__onFinalizeRenderResources)
        pass

    @staticmethod
    def _onFinalize():
        for (GroupName, Prefetch), count in PrefetchGroupNotifyManager.s_active_groups.items():
            for _ in xrange(count):
                PrefetchGroupNotifyManager.__unfetchGroup(GroupName, Prefetch)

        PrefetchGroupNotifyManager.s_render_resources_initialized = False
        PrefetchGroupNotifyManager.s_groups = []
        PrefetchGroupNotifyManager.s_prefetch_list = {}
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_NO
        pass

    @staticmethod
    def __prefetchGroup(GroupName, Prefetch, callback=None, *args):
        key = (GroupName, Prefetch)
        PrefetchGroupNotifyManager.s_active_groups[key] = PrefetchGroupNotifyManager.s_active_groups.get(key, 0) + 1

        if Prefetch == 1:
            print "PrefetchGroupNotifyManager: incrementing resources for group '%s'" % GroupName
            Mengine.incrementResources(GroupName)
            return True

        # False means no pending asynchronous work; resources may still be retained.
        return Mengine.prefetchResources(GroupName, callback, *args)

    @staticmethod
    def __unfetchGroup(GroupName, Prefetch):
        key = (GroupName, Prefetch)
        count = PrefetchGroupNotifyManager.s_active_groups.get(key, 0)

        if count == 0:
            return

        if count == 1:
            del PrefetchGroupNotifyManager.s_active_groups[key]
        else:
            PrefetchGroupNotifyManager.s_active_groups[key] = count - 1

        if Prefetch == 1:
            Mengine.decrementResources(GroupName)
        elif Prefetch == 2:
            Mengine.unfetchResources(GroupName)

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
        if PrefetchGroupNotifyManager.s_render_resources_initialized is True:
            return True

        PrefetchGroupNotifyManager.s_render_resources_initialized = True
        PrefetchGroupNotifyManager.s_status = PrefetchGroupNotifyManager.STATUS_START
        PrefetchGroupNotifyManager.prefetchGroupsTagged(None)

        return True

    @staticmethod
    def __onFinalizeRenderResources():
        if PrefetchGroupNotifyManager.s_render_resources_initialized is False:
            return True

        PrefetchGroupNotifyManager.s_render_resources_initialized = False
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
                PrefetchGroupNotifyManager.__prefetchGroup(GroupName, Prefetch)
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

                if PrefetchGroupNotifyManager.__prefetchGroup(GroupName, Prefetch, __cb, Tag, GroupName) is False:
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

            if Prefetch in (1, 2):
                PrefetchGroupNotifyManager.__unfetchGroup(GroupName, Prefetch)

    @staticmethod
    def prefetchGroup(GroupName):
        for group_name, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if group_name != GroupName:
                continue

            if Prefetch == 0:
                pass
            elif Prefetch == 1:
                PrefetchGroupNotifyManager.__prefetchGroup(GroupName, Prefetch)
            elif Prefetch == 2:
                def __cb(successful, GroupName):
                    pass

                PrefetchGroupNotifyManager.__prefetchGroup(GroupName, Prefetch, __cb, GroupName)

    @staticmethod
    def unfetchGroup(GroupName):
        for group_name, Prefetch, GroupTag in PrefetchGroupNotifyManager.s_groups:
            if group_name != GroupName:
                continue

            if Prefetch in (1, 2):
                PrefetchGroupNotifyManager.__unfetchGroup(GroupName, Prefetch)
