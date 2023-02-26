from GOAP2.StateManager import StateManager
from GOAP2.Task.Task import Task

class TaskStateChange(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskStateChange, self)._onParams(params)
        self.ID = params.get("ID")
        self.Value = params.get("Value")
        self.From = params.get("From", None)
        pass

    def _onInitialize(self):
        super(TaskStateChange, self)._onInitialize()

        if _DEVELOPMENT is True:
            if StateManager.hasState(self.ID) is False:
                self.initializeFailed("State %s not found" % (self.ID))
                pass
            pass
        pass

    def _onCheck(self):
        if self.From is None:
            return True
            pass

        if StateManager.getState(self.ID) != self.From:
            return False
            pass

        return True
        pass

    def _onRun(self):
        StateManager.changeState(self.ID, self.Value)

        return True
        pass

    pass