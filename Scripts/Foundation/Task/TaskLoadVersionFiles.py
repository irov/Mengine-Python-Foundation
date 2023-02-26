from Foundation.Task.Task import Task

class TaskLoadVersionFiles(Task):
    def _onParams(self, params):
        super(TaskLoadVersionFiles, self)._onParams(params)
        def cb(number):
            pass
        self.cb = params.get('cb', cb)
        self.type = params.get('ver', 'master')
        self.reload = params.get('reload', False)
        pass

    def _onRun(self):
        def cb(number, status, data, code, bool):
            self.cb(data, code, self.reload)
            self.complete()
            pass

        http = Mengine.getConfigString('LoadTE', 'url', 'http://62.80.178.35:8888/files/getcur?type={}')
        Mengine.getMessage(http.format(self.type), cb)
        return False
        pass