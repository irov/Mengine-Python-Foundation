from Foundation.Task.MixinObjectTemplate import MixinText

from Task import Task

class TaskTextSetTextID(MixinText, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskTextSetTextID, self)._onParams(params)
        self.Value = params.get("Value")
        pass

    def _onRun(self):
        if self.Value is None:
            self.Text.removeTextId()
            return
            pass

        self.Text.setTextId(self.Value)

        return True
        pass
    pass