from GOAP2.Task.Task import Task

class TaskUnfetchGroup(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskUnfetchGroup, self)._onParams(params)

        self.GroupName = params.get("GroupName")
        self.Prefetch = params.get("Prefetch", 0)
        pass

    def _onInitialize(self):
        super(TaskUnfetchGroup, self)._onInitialize()

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
            Menge.decrementResources(self.GroupName)
            pass
        elif self.Prefetch == 2:
            Menge.unfetchResources(self.GroupName)
            pass
        return True
        pass
    pass