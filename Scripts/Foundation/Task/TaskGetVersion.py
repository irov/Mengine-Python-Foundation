from Foundation.Task.Task import Task

class TaskGetVersion(Task):
    def _onParams(self, params):
        super(TaskGetVersion, self)._onParams(params)
        def cb(number):
            pass
        self.cb = params.get('cb', cb)
        self.type = params.get('ver', 'master')
        self.reload = params.get('reload', False)
        pass

    def _onRun(self):
        def cb(number, status, data, code, bool):
            self.cb(data, code, self.type, self.reload)
            self.complete()
            pass

        http = Mengine.getConfigString('LoadTE', 'GetVersion', 'http://62.80.178.35:8888/version?type={}')
        Mengine.getMessage(http.format(self.type), cb)
        return False
        pass