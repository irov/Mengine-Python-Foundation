from Foundation.Task.Task import Task

class TaskSpinnerCheck(Task):

    def _onParams(self, params):
        super(TaskSpinnerCheck, self)._onParams(params)

        self.state = params.get("State")
        self.notificator = params.get("Notificator")
        pass

    def _onRun(self):
        super(TaskSpinnerCheck, self)._onRun()
        return True

    def __check(self, card, state):
        return state == self.state