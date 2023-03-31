from Foundation.Task.Task import Task
from Foundation.TaskManager import TaskManager
from Foundation.Facebook import Facebook


class TaskFacebookAuthentication(Task):

    def _onParams(self, params):
        super(TaskFacebookAuthentication, self)._onParams(params)

        self.data = params.get('data', {})
        self.host = params.get('host', 'http://localhost:8888')
        self.IPSemaphore = Semaphore(False, 'IP')

        def def_cb(*args, **kwargs):
            pass

        self.cb = params.get('cb', def_cb)

    def _onRun(self):
        with TaskManager.createTaskChain() as tc:
            tc.addFunction(self._getIP)
            tc.addSemaphore(self.IPSemaphore, From=True)
            tc.addFunction(Facebook.auth_user, self.data)

            with tc.addRepeatTask() as (tc_repeat, tc_until):
                tc_repeat.addFunction(self._getToken)
                tc_repeat.addDelay(100)

                with tc_until.addRaceTask(2) as (tc_normal, tc_cancel):
                    tc_normal.addSemaphore(self.IPSemaphore, From=False)
                    tc_cancel.addListener(Notificator.onFacebookAuthEscape)

        return True

    def __remove_from_data(self, data):
        return data.replace(':', '')

    def _getToken(self):
        url = '{}/get_token?ip={}'.format(self.host, Facebook.client_ip)
        Mengine.getMessage(url, self._cbGetToken)

    def _getIP(self):
        Mengine.getMessage('{}/ip'.format(self.host), self._cbGetIP)

    def _cbGetToken(self, number, data, code, bool):
        if _DEVELOPMENT is True:
            Trace.msg("_cbGetToken: {} {} {} {}".format(number, data, code, bool))

        if len(data) == 0:
            return

        Facebook.setUser(data)
        self.IPSemaphore.setValue(False)
        if data == 'access_denied':
            pass

    def _cbGetIP(self, number, status, data, code, bool):
        if _DEVELOPMENT is True:
            Trace.msg("_cbGetIP {} {} {} {} {}".format(number, status, data, code, bool))

        Facebook.client_ip = self.__remove_from_data(data)
        self.IPSemaphore.setValue(True)
