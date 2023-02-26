from Foundation.Task.Task import Task

from Notification import Notification

class TaskNotify(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNotify, self)._onParams(params)

        self.ID = params.get("ID")
        self.Args = params.get("Args", ())
        self.Kwds = params.get("Kwds", {})
        pass

    def _onInitialize(self):
        super(TaskNotify, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.ID is None:
                self.initializeFailed("NotifyID is None")
                pass
            pass
        pass

    def _onRun(self):
        Notification.notify(self.ID, *self.Args, **self.Kwds)

        return True
        pass
    pass