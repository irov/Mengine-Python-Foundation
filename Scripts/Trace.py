import sys
from TraceManager import TraceManager

def msg(text, *args):
    __validateMessage(text)

    message = __tryPrintMessage(text, *args)
    Mengine.logMessage(message)

def fmsg(text, *args):
    __validateMessage(text)

    message = __tryFormatMessage(text, *args)
    Mengine.logMessage(message)

def msg_err(text, *args):
    __validateMessage(text)

    message = __tryPrintMessage(text, *args)
    Mengine.logError(message)

def msg_warn(text, *args):
    __validateMessage(text)

    message = __tryPrintMessage(text, *args)
    Mengine.logWarning(message)

def msg_dev(text, *args):
    if _DEVELOPMENT is True:
        msg(text, *args)


def msg_dev_err(text, *args):
    if _DEVELOPMENT is True:
        msg_err(text, *args)


def msg_release(text, *args):
    __validateMessage(text)

    message = __tryPrintMessage(text, *args)
    Mengine.logMessageRelease(message)


def log(category, level, text, *args):
    __validateMessage(text)

    if TraceManager.existIn(category) is False:
        Mengine.logError("trace log unknown category '%s'" % category)
        return

    if level > TraceManager.getLevel(category):
        return

    message =  "-----------------------------------------------"
    message += "\nError: " + __tryPrintMessage(text, *args) + ""
    message += "\n-----------------------------------------------"

    if level == 0:
        message += __getTraceback()
        message += "\n-----------------------------------------------"

    Mengine.logError(message)
    pass

def log_exception(category, level, text, *args):
    __validateMessage(text)

    if TraceManager.existIn(category) is False:
        Mengine.logError("trace log unknown category '%s'" % category)
        return

    if level > TraceManager.getLevel(category):
        return

    message = "-----------------------------------------------"
    message += "\nException: " + __tryPrintMessage(text, *args) + ""
    message += "\n-----------------------------------------------"
    message += traceback.format_exc()
    message += "\n-----------------------------------------------"

    Mengine.logError(message)

def log_dev_err(category, level, text, *args):
    if _DEVELOPMENT is True:
        log(category, level, text, *args)

def trace():
    message = "-----------------------------------------------"
    message += "\nTrace:"
    message += "\n-----------------------------------------------"
    message += __getTraceback()
    Mengine.logMessage(message)

def caller(deep=0):
    frame = sys._getframe()  # fixme

    for index in range(2 + deep):
        frame = frame.f_back

    code = frame.f_code
    info = (code.co_filename, frame.f_lineno)

    return info

def __getTraceback():
    message = "\nTraceback (most recent call last):"
    for (filename, line_number, function_name, text) in traceback.extract_stack()[2:]:
        message += "\n  File \"%s\", line %s in %s" % (filename, line_number, function_name)
    return message

def __tryPrintMessage(text, *args):
    try:
        message = text % args
    except Exception as ex:
        message = "{} % {}, Exception: {}".format(text, args, ex)
    return message

def __tryFormatMessage(text, *args):
    try:
        message = text.format(*args)
    except Exception as ex:
        message = "{} .format({}), Exception: {}".format(text, args, ex)
    return message

def __validateMessage(text):
    assert type(text) == str, "Message must be string, not %s" % type(text)
