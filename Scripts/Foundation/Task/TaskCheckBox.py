from Foundation.Task.MixinObjectTemplate import MixinCheckBox
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskCheckBox(MixinCheckBox, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskCheckBox, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onCheckBox, self._onCheckBoxFilter, self.CheckBox)

        return False
        pass

    def _onCheckBoxFilter(self, checkBox, value):
        if value is not self.Value:
            return False
            pass

        return True
        pass
    pass