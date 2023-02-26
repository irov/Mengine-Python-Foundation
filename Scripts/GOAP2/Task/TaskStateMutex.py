from GOAP2.StateManager import StateManager
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskStateMutex(MixinObserver, Task):
    def _onParams(self, params):
        super(TaskStateMutex, self)._onParams(params)

        self.ID = params.get("ID")
        self.Value = params.get("From")
        pass

    def _onInitialize(self):
        super(TaskStateMutex, self)._onInitialize()

        if _DEVELOPMENT is True:
            if StateManager.hasState(self.ID) is False:
                self.initializeFailed("State %s not found" % (self.ID))
                pass
            pass
        pass

    def _onCheck(self):
        state = StateManager.getState(self.ID)

        if state == self.Value:
            return False
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onStateChange, self._onStateValueFilter)

        return False
        pass

    def _onStateValueFilter(self, ID, newValue, *args):
        if self.ID != ID:
            return False
            pass

        if self.Value != newValue:
            return False
            pass

        Value = StateManager.getState(self.ID)

        if self.Value != Value:
            return False
            pass

        return True
        pass
    pass