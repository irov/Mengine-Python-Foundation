from Foundation.Task.Task import Task

from Foundation.GoogleAnalytics import GoogleAnalytics

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