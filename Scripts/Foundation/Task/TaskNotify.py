from Foundation.Task.Task import Task

class TaskNotify(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNotify, self)._onParams(params)

        self.ID = params.get("ID")
        self.Args = params.get("Args", ())
        self.Kwargs = params.get("Kwargs", {})
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
        try:
            Notification.notify(self.ID, *self.Args, **self.Kwargs)
        except Exception as ex:
            self.log("Error notify '%s' args: %s exception: %s" % (self.ID, ex, self.Args))
            pass

        return True
        pass
    pass