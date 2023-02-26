# - debug decorators ------------------------------------------------------
from Foundation.DefaultManager import DefaultManager

from Task import Task

def print_request(func):
    def wrapper(self):
        result = func(self)
        DefaultCurlPrintResponse = DefaultManager.getDefaultBool("DefaultCurlPrintRequest", False)
        if DefaultCurlPrintResponse and _DEVELOPMENT is True:
            curl_request_msg = " < < < C U R L  R E Q U E S T < < < " \
                               "[id] = {}, " \
                               "[url] = {}, " \
                               "[headers] = {}, " \
                               "[data] = {}".format(self.id, self.url, self.headers, self.data)
            print
            curl_request_msg
        return result
    return wrapper

def print_response(response_handler):
    def wrapper(self, id, status, error, response, code, successful):
        DefaultCurlPrintResponse = DefaultManager.getDefaultBool("DefaultCurlPrintResponse", False)
        if DefaultCurlPrintResponse and _DEVELOPMENT is True:
            curl_response_msg = " > > > C U R L  R E S P O N S E > > > " \
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


class TaskHeaderData(Task):

    def _onParams(self, params):
        super(TaskHeaderData, self)._onParams(params)

        self.url = params.get("Url")
        self.headers = params.get("Headers")
        self.data = params.get("Data")

        default_time_out = DefaultManager.getDefaultInt("DefaultHeaderDataTimeOut", -1)
        self.time_out = params.get("TimeOut", default_time_out)

        self.cb = Utils.make_functor(params, "Cb")

        self.id = None

    @print_request  # debug
    def _onRun(self):
        # print "[TaskHeaderData|_onRun] BEFORE " \
        #       "url={}, " \
        #       "headers={}, " \
        #       "data={}, " \
        #       "time_out={}".format(self.url, self.headers, self.data, self.time_out)

        self.id = Mengine.headerData(self.url, self.headers, self.data, self.time_out, self._onHeaderData)

        # print "[TaskHeaderData|_onRun] AFTER " \
        #       "id={}, " \
        #       "url={}, " \
        #       "headers={}, " \
        #       "data={}, " \
        #       "time_out={}".format(self.id, self.url, self.headers, self.data, self.time_out)

        if self.id == 0:
            self.log("Fail to do Mengine.headerData with parameters: "
                     "url = {}, "
                     "headers = {}, "
                     "data = {}, ".format(self.url, self.headers, self.data))
            return True
        return False

    @print_response  # debug
    def _onHeaderData(self, id, status, error, response, code, successful):
        if self.id != id:
            # print "#####################################"
            # print "#####################################"
            # print "#####################################"
            # print "TaskHeaderData._onHeaderData self.id != id, {} != {}".format(self.id, id)
            return

        if successful is False:
            self.log("{}".format(error))

        if self.cb is not None:
            self.cb(status, error, response, code, successful)

        self.id = None

        self.complete()

    def _onSkip(self):
        # print "****************************************"
        # print "****************************************"
        # print "****************************************"
        # print "****************************************"
        # print "****************************************"
        # print "****************************************"
        # print " TASK HEADER DATA SKIP"
        pass