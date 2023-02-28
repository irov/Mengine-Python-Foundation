from Foundation.Task.Task import Task


class TaskHeaderDataBase(Task):

    def _onParams(self, params):
        super(Task, self)._onParams(params)

        self.url = params.get("Url")
        self.headers = params.get("Headers")
        self.data = params.get("Data")

        self.cb = Utils.make_functor(params, "Cb")

        self.requestId = None

    def _onRun(self):
        json_data = json.dumps(self.data)
        self.requestId = Mengine.headerData(self.url, self.headers, json_data, self.__onHeaderData)
        return False

    def __onHeaderData(self, requestId, status, error, response, code, successful):
        if _DEVELOPMENT is True:
            Trace.msg(""" [TaskHeaderData:_onHeaderData] self.requestId = '{}' | requestId = '{}' | 
                   status = '{}' | error = '{}' | code = '{}' | successful = '{}' response = '{}'""".format(
                self.requestId, requestId, status, error, code, successful, response))

        if self.requestId != requestId:
            return

        if code != 200:
            self.log("{}".format(error))
            self._onFailed(error, response)
        else:
            self._onSuccess(response)

        self.requestId = None

        self.complete()

    def _onSuccess(self, response):
        pass

    def _onFailed(self, error, response):
        pass
