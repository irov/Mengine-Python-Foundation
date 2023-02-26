from GOAP2.Task.Task import Task

class TaskSendAnalytics(Task):

    def _onParams(self, params):
        super(TaskSendAnalytics, self)._onParams(params)
        self.params = params
        pass

    def _onRun(self):
        super(TaskSendAnalytics, self)._onRun()
        GoogleAnalytics.send_analytics(self.params)
        return True
        pass
    pass