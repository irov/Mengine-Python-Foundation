from sys import _getframe

debug_error = 0
debug_warning = 0
debug_trace = 0
debug_todo = 0
debug_timer = 0

timersMap = {}

def getTimestamp():
    t = Mengine.getTime()

    return "%d" % t

def setLevelError(flag):
    global debug_error
    debug_error = flag
    pass

def setLevelWarning(flag):
    global debug_warning
    debug_warning = flag
    pass

def setLevelTrace(flag):
    global debug_trace
    debug_trace = flag
    pass

def setLevelTimer(flag):
    global debug_timer
    debug_timer = flag
    pass

def doError(level, *format):
    global debug_error
    doPrint("ERROR", debug_error, level, *format)
    pass

def doWarning(level, *format):
    global debug_warning
    doPrint("WARNING", debug_warning, level, *format)
    pass

def doTrace(level, *format):
    global debug_trace
    doPrint("TRACE", debug_trace, level, *format)
    pass

def doTodo(level, *format):
    global debug_todo
    doPrint("TODO", debug_todo, level, *format)
    pass

def doTimer(timerKey, *format):
    global debug_timer
    global debug_trace

    curType = type(timerKey)
    if curType != str and curType != unicode:
        timerKey = "default"

    curTime = Mengine.getTime()
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
        try:
            message = "%s%s " % (message, s)
        except UnicodeDecodeError:
            message = "%s%s " % (message.encode("UTF-8"), s)

    if curLevel >= level or curLevel == -1:
        if (level < 0) and (curLevel != level):
            return

        print(message)
        pass
    pass

def _trace(*format):
    doTrace(0, *format)

def _warning(*format):
    doWarning(0, *format)

def _error(*format):
    doError(0, *format)

def _todo(*format):
    doTodo(0, *format)

def _timer(timerKey, *format):
    doTimer(timerKey, *format)