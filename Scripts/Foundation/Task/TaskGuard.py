from Foundation.Notificator import Notificator
from Foundation.Task.Task import Task

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
        guard = self.Guard
        self.Guard = None

        if self.Enable is not True:
            return
        if guard is None:
            return

        guard(False)
        Notification.notify(Notificator.onTaskGuardUpdate, False)

    def _onFinally(self):
        super(TaskGuard, self)._onFinally()

        self._onSkip()