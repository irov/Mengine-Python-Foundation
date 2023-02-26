from Foundation.Task.Task import Task

class TaskPrefetchGroup(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskPrefetchGroup, self)._onParams(params)

        self.GroupName = params.get("GroupName")
        self.Prefetch = params.get("Prefetch", 0)
        pass

    def _onInitialize(self):
        super(TaskPrefetchGroup, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.GroupName is None:
                self.initializeFailed("Group name is None")
                pass
            pass
        pass

    def _onRun(self):
        if self.Prefetch == 0:
            pass
        elif self.Prefetch == 1:
            Mengine.incrementResources(self.GroupName)
            pass
        elif Prefetch == 2:
            def __cb(successful, GroupName):
                pass

            Mengine.prefetchResources(self.GroupName, __cb, self.GroupName)
            pass
        return True
        pass
    pass