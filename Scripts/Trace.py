import sys
import traceback
from TraceManager import TraceManager


def msg(text, *args):
    assert type(text) == str, "Message must be string, not %s" % type(text)

    try:
        Mengine.logWarning(text % args)
    except Exception as ex:
        Mengine.logWarning("'{} % {}' | Exception = {}".format(text, args, ex))


def msg_err(text, *args):
    assert type(text) == str, "Message must be string, not %s" % type(text)

    try:
        Mengine.logError(text % args)
    except Exception as ex:
        Mengine.logError("'{} % {}' | Exception = {}".format(text, args, ex))


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
        error_msg = "\n-----------------------------------------------"
        error_msg += "\nError:"
        try:
            error_msg += "\n" + (text % args)
        except Exception as ex:
            error_msg += "\n" + "'{} % {}' | Exception = {}".format(text, args, ex)
        error_msg += "\n-----------------------------------------------"

        Mengine.logError(error_msg)

        if level == 0:
            pass# __print_traceback()


def trace():
    __print_traceback()


def caller(deep=0):
    frame = sys._getframe()

    for index in range(2 + deep):
        frame = frame.f_back

    code = frame.f_code
    info = (code.co_filename, frame.f_lineno)

    return info


def __print_traceback():
    trace_msg = "\n-----------------------------------------------"
    trace_msg += "\nTrace:"
    trace_msg += "\n-----------------------------------------------"
    trace_msg += "\nTraceback (most recent call last):"
    for (filename, line_number, function_name, text) in traceback.extract_stack():
        trace_msg += "\n  File \"%s\", line %s in %s" % (filename, line_number, function_name)
    Mengine.logError(trace_msg)
