from GOAP2.Task.Task import Task

class TaskSpinnerCheck(Task):

    def _onParams(self, params):
        super(TaskSpinnerCheck, self)._onParams(params)

        self.state = params.get("State")
        self.notificator = params.get("Notificator")
        pass

    def _onRun(self):
        super(TaskSpinnerCheck, self)._onRun()

        """myTask = TaskManager.createTaskChain()
        with myTask as tc:
            tc.addListener(self.notificator, self.__check)
            pass"""
        return True
        pass

    def __check(self, card, state):
        return state == self.state
    pass