import sys
import traceback
from TraceManager import TraceManager


def msg(text, *args):
    assert type(text) == str

    try:
        print(text % args)
    except Exception as ex:
        print(text, args, ex)


def msg_err(text, *args):
    assert type(text) == str

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


def msg_dev(text, *args):
    if _DEVELOPMENT is True:
        msg(text, *args)


def log(category, level, text, *args):
    assert type(text) == str

    if TraceManager.existIn(category) is False:
        print("trace log no category %s" % (category))
        return

    if level <= TraceManager.getLevel(category):
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
