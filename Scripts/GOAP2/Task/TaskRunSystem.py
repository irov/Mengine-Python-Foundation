from GOAP2.SystemManager import SystemManager
from GOAP2.Task.Task import Task

class TaskRunSystem(Task):
    def _onParams(self, params):
        super(TaskRunSystem, self)._onParams(params)

        self.systemType = params.get("SystemType")
        self.systemName = params.get("SystemName")
        self.systemParams = params.get("Params", {})
        pass

    def _onInitialize(self):
        super(TaskRunSystem, self)._onInitialize()

        if _DEVELOPMENT is True:
            if SystemManager.hasSystem(self.systemName) is False:
                self.initializeFailed("not found system %s" % (self.systemName))
                pass
            pass
        pass

    def _onRun(self):
        SystemManager.runSystem(self.systemName, self.systemType, **self.systemParams)

        return True
        pass
    pass