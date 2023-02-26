from GOAP2.Task.MixinObjectTemplate import MixinMovie2CheckBox
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMovie2CheckBox(MixinMovie2CheckBox, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovie2CheckBox, self)._onParams(params)
        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovie2CheckBox, self._onMovie2CheckBoxFilter, self.Movie2CheckBox)
        return False
        pass

    def _onMovie2CheckBoxFilter(self, checkBox, value):
        if value is not self.Value:
            return False
            pass

        return True
        pass
    pass