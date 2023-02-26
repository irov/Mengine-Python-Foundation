from Foundation.Task.Task import Task
from Foundation.TaskManager import TaskManager

class TaskFacebookAuthentication(Task):
    def _onParams(self, params):
        super(TaskFacebookAuthentication, self)._onParams(params)
        self.data = params.get('data', {})
        def def_cb(one, two, three, four):
            pass
        self.cb = params.get('cb', def_cb)
        self.IPSemaphore = Semaphore(False, 'IP')
        pass

    def _onRun(self):
        super(TaskFacebookAuthentication, self)._onRun()
        def cb(number, data, code, bool):
            if len(data) != 0:
                Facebook.setUser(data)
                self.IPSemaphore.setValue(False)
                if data == 'access_denied':
                    pass

        with TaskManager.createTaskChain() as tc:
            tc.addFunction(self.__get_ip)
            tc.addSemaphore(self.IPSemaphore, From=True)
            tc.addFunction(Facebook.auth_user, self.data)
            with tc.addRepeatTask() as (tc_repeat, tc_until):
                tc_repeat.addDelay(100)
                tc_repeat.addFunction(Menge.getMessage, 'http://localhost:8888/get_token?ip={}'.format(Facebook.client_ip), cb)
                with tc_until.addRaceTask(2) as (tc_normal, tc_cancel):
                    tc_normal.addSemaphore(self.IPSemaphore, From=False)
                    tc_cancel.addListener(Notificator.onFacebookAuthEscape)

        return True
        pass

    def __remove_from_data(self, data):
        return data.replace(':', '')

    def __get_ip(self):
        def cb(number, status, data, code, bool):
            Facebook.client_ip = self.__remove_from_data(data)
            self.IPSemaphore.setValue(True)
            pass

        Menge.getMessage('http://localhost:8888/ip', cb)
        pass