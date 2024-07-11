import sys
import traceback
from TraceManager import TraceManager


def msg(text, *args):
    assert type(text) == str, "Message must be string, not %s" % type(text)

    message = __tryFormatMessage(text, *args)
    Mengine.logWarning(message)


def msg_err(text, *args):
    assert type(text) == str, "Message must be string, not %s" % type(text)

    message = __tryFormatMessage(text, *args)
    Mengine.logError(message)


def msg_dev(text, *args):
    if _DEVELOPMENT is True:
        msg(text, *args)


def msg_dev_err(text, *args):
    if _DEVELOPMENT is True:
        msg_err(text, *args)


def log(category, level, text, *args):
    assert type(text) == str, "Message must be string, not %s" % type(text)

    if TraceManager.existIn(category) is False:
        Mengine.logWarning("trace log unknown category '%s'" % category)
        return

    if level <= TraceManager.getLevel(category):
        message = "\n-----------------------------------------------"
        message += "\nError:"
        message += "\n-----------------------------------------------"
        message += "\n" + __tryFormatMessage(text, *args)

        if level == 0:
            message += __getTraceback()

        Mengine.logError(message)


def trace():
    message = __getTraceback()
    Mengine.logError(message)


def caller(deep=0):
    frame = sys._getframe()  # fixme

    for index in range(2 + deep):
        frame = frame.f_back

    code = frame.f_code
    info = (code.co_filename, frame.f_lineno)

    return info


def __getTraceback():
    message = "\n-----------------------------------------------"
    message += "\nTrace:"
    message += "\n-----------------------------------------------"
    message += "\nTraceback (most recent call last):"
    for (filename, line_number, function_name, text) in traceback.extract_stack()[:-2]:
        message += "\n  File \"%s\", line %s in %s" % (filename, line_number, function_name)
    return message


def __tryFormatMessage(text, *args):
    try:
        # message = text % args
        message = Mengine.logError(text % args)    # fixme: engine crash repr for @irov
    except Exception as ex:
        message = "{} % {}, Exception: {}".format(text, args, ex)
    return message
