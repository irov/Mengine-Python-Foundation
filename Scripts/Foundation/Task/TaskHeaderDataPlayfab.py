import json

from Task import Task

class TaskHeaderDataPlayfab(Task):

    def _onParams(self, params):
        super(Task, self)._onParams(params)

        self.url = params.get("Url")
        self.headers = params.get("Headers")
        self.data = params.get("Data")

        self.cb = Utils.make_functor(params, "Cb")

        self.requestId = None

    def _onRun(self):
        json_data = json.dumps(self.data)

        self.requestId = Mengine.headerData(self.url, self.headers, json_data, self._onHeaderData)

        return False

    def _onHeaderData(self, requestId, status, error, response, code, successful):
        if self.requestId != requestId:
            return

        response_data = None

        if status == 0:
            decoded_response = json.loads(response)
            response_data = decoded_response.get('data', {})
        else:
            self.log("{}".format(error))

        if self.cb is not None:
            self.cb(status, response_data)

        self.requestId = None

        self.complete()