import sys
import traceback
from TraceManager import TraceManager


def msg(text, *args):
    try:
        print(text % args)
    except Exception as ex:
        print(text, args, ex)


def msg_err(text, *args):
    if _PYTHON_VERSION < 300:
        try:
            print >> sys.stderr, text % args
        except Exception as ex:
            print >> sys.stderr, text, args, ex
    else:
        try:
            print(text % args)
        except Exception as ex:
            print(text, args, ex)


def log(type, level, text, *args):
    if TraceManager.existIn(type) is False:
        print("trace log no type %s" % (type))
        return

    if level <= TraceManager.getLevel(type):
        if _PYTHON_VERSION < 300:
            print >> sys.stderr, "-----------------------------------------------"
            print >> sys.stderr, "Error:"
            print >> sys.stderr, "-----------------------------------------------"

            try:
                print >> sys.stderr, text % args
            except Exception as ex:
                print >> sys.stderr, text, args, ex
        else:
            try:
                print(text % args)
            except Exception as ex:
                print(text, args, ex)

        if level == 0:
            if _PYTHON_VERSION < 300:
                print >> sys.stderr, "-----------------------------------------------"
                print >> sys.stderr, "Trace:"
                print >> sys.stderr, "-----------------------------------------------"

            traceback.print_stack()


def trace():
    print >> sys.stderr, "-----------------------------------------------"
    print >> sys.stderr, "Trace:"
    print >> sys.stderr, "-----------------------------------------------"
    traceback.print_stack()


def caller(deep=0):
    frame = sys._getframe()

    for index in range(2 + deep):
        frame = frame.f_back

    code = frame.f_code
    info = (code.co_filename, frame.f_lineno)

    return info
