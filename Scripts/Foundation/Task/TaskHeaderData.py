from Foundation.DefaultManager import DefaultManager
from Foundation.Task.Task import Task


_REDACTED_VALUE = "<redacted>"
_SENSITIVE_FIELD_MARKERS = (
    "authorization",
    "authcode",
    "customid",
    "gamecenterid",
    "password",
    "salt",
    "secret",
    "signature",
    "ticket",
    "token",
    "localsave",
    "playerdata",
    "email",
    "username",
)


def _is_sensitive_field(name):
    normalized_name = "{}".format(name).lower().replace("-", "").replace("_", "")

    for marker in _SENSITIVE_FIELD_MARKERS:
        if marker in normalized_name:
            return True

    return False


def _redact_value(value):
    if isinstance(value, dict):
        redacted_value = {}

        for key, item in value.items():
            if _is_sensitive_field(key) is True:
                redacted_value[key] = _REDACTED_VALUE
            else:
                redacted_value[key] = _redact_value(item)

        return redacted_value

    if isinstance(value, (list, tuple)):
        return [_redact_value(item) for item in value]

    return value


def _redact_headers(headers):
    redacted_headers = []

    for header in headers or []:
        header_parts = header.split(":", 1)

        if len(header_parts) == 2 and _is_sensitive_field(header_parts[0]) is True:
            redacted_headers.append("{}: {}".format(header_parts[0], _REDACTED_VALUE))
        else:
            redacted_headers.append(header)

    return redacted_headers


def _redact_payload(payload):
    if payload is None or payload == "":
        return payload

    try:
        payload_data = Mengine.decodeJSON(payload)
        redacted_payload_data = _redact_value(payload_data)

        return Mengine.encodeJSON(redacted_payload_data)
    except Exception:
        return _REDACTED_VALUE


def _redact_url(url):
    if url is None or "?" not in url:
        return url

    return "{}?{}".format(url.split("?", 1)[0], _REDACTED_VALUE)


def print_request(func):
    def wrapper(self):
        result = func(self)
        DefaultCurlPrintRequest = DefaultManager.getDefaultBool("DefaultCurlPrintRequest", False)
        if DefaultCurlPrintRequest and _DEVELOPMENT is True:
            curl_request_msg = " < < < C U R L  R E Q U E S T < < < " \
                               "[id] = {}, " \
                               "[url] = {}, " \
                               "[headers] = {}, " \
                               "[data] = {}".format(
                                    self.id,
                                    _redact_url(self.url),
                                    _redact_headers(self.headers),
                                    _redact_payload(self.data)
                               )
            Trace.msg(curl_request_msg)
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
                                "[response] = {}".format(
                                    id,
                                    status,
                                    error,
                                    code,
                                    successful,
                                    _redact_payload(response)
                                )
            Trace.msg(curl_response_msg)
        response_handler(self, id, status, error, response, code, successful)
    return wrapper


class TaskHeaderData(Task):

    __debug_force_response_code = None
    if _DEVELOPMENT and Mengine.hasOption("forceresponsecode"):
        __debug_force_response_code = int(Mengine.getOptionValue("forceresponsecode"))

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
                     "data = {}, ".format(
                         _redact_url(self.url),
                         _redact_headers(self.headers),
                         _redact_payload(self.data)
                     ))
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
            if self.__debug_force_response_code is not None:
                code = self.__debug_force_response_code
            self.cb(status, error, response, code, successful)

        self.id = None

        self.complete()

    def _onSkip(self):
        pass
