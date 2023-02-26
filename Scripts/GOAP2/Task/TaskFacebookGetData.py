from GOAP2.Task.Task import Task

class TaskFacebookGetData(Task):
    def _onParams(self, params):
        super(TaskFacebookGetData, self)._onParams(params)
        self.data = params.get('data', {})
        def def_cb(data):
            pass
        self.cb = params.get('cb', def_cb)
        pass

    def _onRun(self):
        super(TaskFacebookGetData, self)._onRun()
        def sec_cb(number, status, data, code, bool):
            self.cb(data)
            pass
        Facebook.get_users_data(self.data, sec_cb)
        return True
        pass