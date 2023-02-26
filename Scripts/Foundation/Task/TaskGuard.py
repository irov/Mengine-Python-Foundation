from Foundation.Notificator import Notificator
from Foundation.Task.Task import Task
from Notification import Notification

class TaskGuard(Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskGuard, self)._onParams(params)

        self.Enable = params.get("Enable", True)

        self.Guard = Utils.make_functor(params, "Guard")

    def _onRun(self):
        if self.Enable is True:
            self.Guard(True)
            Notification.notify(Notificator.onTaskGuardUpdate, True)

        return False

    def _onSkip(self):
        if self.Enable is True:
            self.Guard(False)
            Notification.notify(Notificator.onTaskGuardUpdate, False)