from Foundation.Task.Task import Task

class TaskGetFtp(Task):
    def _onParams(self, params):
        super(TaskGetFtp, self)._onParams(params)
        def cb(number):
            pass
        self.cb = params.get('cb', cb)
        self.data = params.get('data', cb)
        pass

    def _onRun(self):
        def cb(number, status, data, code, bool):
            self.cb(data, code, self.data)
            self.complete()
            pass

        http = Menge.getConfigString('LoadTE', 'GetFTP', 'http://62.80.178.35:8888/ftp')
        Menge.getMessage(http, cb)
        return False
        pass