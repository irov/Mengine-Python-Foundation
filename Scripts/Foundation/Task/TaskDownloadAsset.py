from Foundation.DefaultManager import DefaultManager
from Foundation.Task.Task import Task

def print_request(func):
    def wrapper(self):
        result = func(self)

        if _DEVELOPMENT is True:
            curl_request_msg = " < < < D O W N L O A D  A S S E T  R E Q U E S T < < < " \
                               "[id] = {}, " \
                               "[url] = {}, " \
                               "[login] = {}, " \
                               "[password] = {}, " \
                               "[file_group] = {}, " \
                               "[file_path] = {}, ".format(self.id, self.url, self.login, self.password, self.file_group, self.file_path)
            print(curl_request_msg)
        return result
    return wrapper

def print_response(response_handler):
    def wrapper(self, id, status, error, response, code, successful):
        if _DEVELOPMENT is True:
            curl_response_msg = " > > > D O W N L O A D  A S S E T  R E S P O N S E > > > " \
                                "[id] = {}, " \
                                "[status] = {}, " \
                                "[error] = {}, " \
                                "[code] = {}, " \
                                "[successful] = {}, " \
                                "[response] = {}".format(id, status, error, code, successful, response)
            print(curl_response_msg)
        response_handler(self, id, status, error, response, code, successful)
    return wrapper

Task

class TaskDownloadAsset(Task):
    def _onParams(self, params):
        super(TaskDownloadAsset, self)._onParams(params)

        self.url = params.get("Url")
        self.login = params.get("Login", "")
        self.password = params.get("Password", "")
        self.file_group = params.get("FileGroup", "user")
        self.file_path = params.get("FilePath")

        default_time_out = DefaultManager.getDefaultInt("DefaultHeaderDataTimeOut", -1)
        self.time_out = params.get("TimeOut", default_time_out)

        self.rewrite = params.get("Rewrite", False)

        self.cb = Utils.make_functor(params, "Cb")

        self.id = None

    def __cancelRequest(self):
        request_id = self.id
        self.id = None
        self.cb = None

        if request_id is None:
            return

        if request_id == 0:
            return

        Mengine.cancelRequest(request_id)

    def _onFinalize(self):
        super(TaskDownloadAsset, self)._onFinalize()

        self.__cancelRequest()

    @print_request  # debug
    def _onRun(self):
        if Mengine.existFile(self.file_group, self.file_path):
            print('file {} {} is existFile'.format(self.file_group, self.file_path))
            if self.rewrite is False:
                return True

            Mengine.removeFile(self.file_group, self.file_path)
            print('file {} {} has been removed'.format(self.file_group, self.file_path))

        self.id = Mengine.downloadAsset(self.url, self.login, self.password, self.file_group, self.file_path, self.time_out, self.__onDownloadAsset)

        if self.id == 0:
            self.log("Fail to do Mengine.downloadAsset with parameters: "
                     "url = {}, "
                     "login = {}, "
                     "password = {}, "
                     "file_group = {}, "
                     "file_path = {}"
                     "timeout = {}".format(self.url, self.login, self.password, self.file_group, self.file_path, self.time_out))
            self.setError(True)
            return True
        return False

    @print_response  # debug
    def __onDownloadAsset(self, id_, status, error, response, code, successful):
        if id_ != self.id:
            return

        self.id = None
        cb = self.cb
        self.cb = None

        if successful is False:
            if error:
                self.log("{}".format(error))
            self.setError(True)
            pass

        if cb is not None:
            base = self.base
            result = cb(status, error, response, code, successful)
            if result is False:
                base.setError(True)
            pass

        self.complete()

    def _onSkip(self):
        self.__cancelRequest()
