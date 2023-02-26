# ------------------------------------------------------------------------------
# Module: Debug
# Creating: 30.08.2007 12:18
# Description:
# - 
# ------------------------------------------------------------------------------
from sys import _getframe
# from inspect import getmodulename
# from time import clock
# import datetime

debug_error = 0
debug_warning = 0
debug_trace = 0
debug_todo = 0
debug_timer = 0

timersMap = {}

def getTimestamp():
    t = Menge.getTime()

    return "%d" % t

# def getTimestamp():
# t = datetime.datetime.now()
# return "%04d-%02d-%02d %02d:%02d:%02d.%03d" % \
# ( t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond / 1000 )

# ----------------------------------------------------------------------------
# Metod: setLevelError
# Description:
# - 
# ----------------------------------------------------------------------------
def setLevelError(flag):
    global debug_error
    debug_error = flag
    pass

# ----------------------------------------------------------------------------
# Metod: setLevelWarning
# Description:
# - 
# ----------------------------------------------------------------------------
def setLevelWarning(flag):
    global debug_warning
    debug_warning = flag
    pass

# ----------------------------------------------------------------------------
# Metod: setLevelTrace
# Description:
# - 
# ----------------------------------------------------------------------------
def setLevelTrace(flag):
    global debug_trace
    debug_trace = flag
    pass

# ----------------------------------------------------------------------------
# Metod: setLevelTimer
# Description:
# - 
# ----------------------------------------------------------------------------
def setLevelTimer(flag):
    global debug_timer
    debug_timer = flag
    pass

# ----------------------------------------------------------------------------
# Metod: doError
# Description:
# - 
# ----------------------------------------------------------------------------
def doError(level, *format):
    global debug_error
    doPrint("ERROR", debug_error, level, *format)
    pass

# ----------------------------------------------------------------------------
# Metod: doWarning
# Description:
# - 
# ----------------------------------------------------------------------------
def doWarning(level, *format):
    global debug_warning
    doPrint("WARNING", debug_warning, level, *format)
    pass

# ----------------------------------------------------------------------------
# Metod: doTrace
# Description:
# - 
# ----------------------------------------------------------------------------
def doTrace(level, *format):
    global debug_trace
    doPrint("TRACE", debug_trace, level, *format)
    pass

# ----------------------------------------------------------------------------
# Metod: doTodo
# Description:
# - 
# ----------------------------------------------------------------------------
def doTodo(level, *format):
    global debug_todo
    doPrint("TODO", debug_todo, level, *format)
    pass

# ----------------------------------------------------------------------------
# Metod: doTimer
# Description:
# - 
# ----------------------------------------------------------------------------
def doTimer(timerKey, *format):
    global debug_timer
    global debug_trace

    curType = type(timerKey)
    if curType != str and curType != unicode:
        timerKey = "default"

    curTime = Menge.getTime()
    try:
        firstTime, lastTime = timersMap[timerKey]
        allInterval = curTime - firstTime
        curInterval = curTime - lastTime
        timersMap[timerKey] = (firstTime, curTime)
        doPrint("%s TIMER(%s): %.3fs/%.3fs" % (getTimestamp(), timerKey, curInterval, allInterval), debug_trace, debug_timer, *format)
    except:
        timersMap[timerKey] = (curTime, curTime)
        doPrint("%s TIMER(%s): INIT(time_since_last_call/time_since_first_call)" % (getTimestamp(), timerKey), debug_trace, debug_timer, *format)
    pass

# ----------------------------------------------------------------------------
# Metod: __print
# Description:
# - WARNING: don't use this method directly! Use error/warning/trace instead!
# ----------------------------------------------------------------------------
def doPrint(msgType, curLevel, level, *format):
    frame = _getframe().f_back.f_back.f_back
    code = frame.f_code
    if format:
        endl = ": "
    else:
        endl = "."

    fname = code.co_filename
    div = fname.rfind('\\')
    if div != -1:
        modulename = fname[fname.rfind('\\') + 1:fname.rfind('.')]
    else:
        modulename = fname[fname.rfind('.') + 1:]
    message = "%s: %s.%s(line %d)%s" % (msgType, modulename, code.co_name, frame.f_lineno, endl)

    for s in format:
        try:                        message = "%s%s " % (message, s)
        except UnicodeDecodeError:    message = "%s%s " % (message.encode("UTF-8"), s)

    if curLevel >= level or curLevel == -1:
        if (level < 0) and (curLevel != level):
            return

        print(message)
        pass
    pass

# def trace	( level, *format ):	doTrace		( level, *format )
# def warning	( level, *format ):	doWarning	( level, *format )
# def error	( level, *format ):	doError		( level, *format )
# def timer	( timerKey, *format ):	doTimer		( timerKey, *format )

def _trace(*format):    doTrace(0, *format)

def _warning(*format):    doWarning(0, *format)

def _error(*format):    doError(0, *format)

def _todo(*format):    doTodo(0, *format)

def _timer(timerKey, *format):    doTimer(timerKey, *format)