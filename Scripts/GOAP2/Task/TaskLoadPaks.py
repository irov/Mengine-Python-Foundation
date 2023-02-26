from GOAP2.Task.Task import Task

class TaskLoadPaks(Task):
    def _onParams(self, params):
        super(TaskLoadPaks, self)._onParams(params)
        def cb(number):
            pass
        self.cb = params.get('cb', cb)
        self.id = params.get('id', '1')
        self.reload = params.get('reload', True)
        pass

    def _onRun(self):
        def cb(number, status, data, code, bool):
            self.cb(data, code, self.reload)
            self.complete()
            pass

        http = Menge.getConfigString('LoadTE', 'loadPak', 'http://62.80.178.35:8888/files/get?id={}')
        Menge.getMessage(http.format(self.id), cb)
        return False
        pass