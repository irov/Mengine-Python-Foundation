from Foundation.Task.Task import Task

class TaskSendAnalyticsScreenView(Task):

    def _onParams(self, params):
        super(TaskSendAnalyticsScreenView, self)._onParams(params)
        self.type = params.get('type', 'screenview')
        self.cid = params.get('clientID', None)
        self.screenName = params.get('screenName', None)
        self.appName = params.get('appName', None)
        self.appVersion = params.get('appVersion', None)
        pass

    def _onRun(self):
        super(TaskSendAnalyticsScreenView, self)._onRun()
        data = dict(cid=self.cid, t=self.type, cd=self.screenName, an=self.appName, av=self.appVersion)
        GoogleAnalytics.send_analytics(data)
        return True
        pass

    pass