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
            print
            curl_request_msg
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
            print
            curl_response_msg
        response_handler(self, id, status, error, response, code, successful)
    return wrapper

# -------------------------------------------------------------------------

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

    @print_request  # debug
    def _onRun(self):
        if Menge.existFile(self.file_group, self.file_path):
            print
            'file {} {} is existFile'.format(self.file_group, self.file_path)
            if self.rewrite is False:
                return True

            Menge.removeFile(self.file_group, self.file_path)
            print
            'file {} {} has been removed'.format(self.file_group, self.file_path)

        self.id = Menge.downloadAsset(self.url, self.login, self.password, self.file_group, self.file_path, self.time_out, self.__onDownloadAsset)

        if self.id == 0:
            self.log("Fail to do Menge.downloadAsset with parameters: "
                     "url = {}, "
                     "login = {}, "
                     "password = {}, "
                     "file_group = {}, "
                     "file_path = {}"
                     "timeout = {}".format(self.url, self.login, self.password, self.file_group, self.file_path, self.timeout))
            self.setError(True)
            return True
        return False

    @print_response  # debug
    def __onDownloadAsset(self, id_, status, error, response, code, successful):
        if id_ != self.id:
            return

        if successful is False:
            self.log("{}".format(error))
            self.setError(True)
            pass

        if self.cb is not None:
            if self.cb(status, error, response, code, successful) is False:
                self.setError(True)
                pass
            pass

        self.id = None

        self.complete()