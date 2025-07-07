from Foundation.PolicyManager import PolicyManager
from Foundation.Task.Wrapper import Wrapper
from Foundation.Task.TaskBase import TaskBase
from Foundation.TaskManager import TaskManager


class TaskGeneratorException(Exception):
    def __init__(self, value, *args):
        assert type(value) == str

        self.value = value % (args)
        pass

    def __str__(self):
        return str(self.value)
        pass
    pass

class TaskSourceTg(object):
    __slots__ = "tg"

    def __init__(self, tg):
        self.tg = tg
        pass

    def __enter__(self):
        return self.tg
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        if _DEVELOPMENT is True:
            self.tg.end()
            pass

        return True
        pass
    pass

class TaskSourceTgIter(object):
    __slots__ = "tg", "it"

    def __init__(self, it, tg):
        self.it = it
        self.tg = tg
        pass

    def __enter__(self):
        return self.it, self.tg
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        if _DEVELOPMENT is True:
            self.tg.end()
            pass

        return True
        pass
    pass

class TaskSourceTgs(object):
    __slots__ = "tgs"

    def __init__(self, tgs):
        self.tgs = tgs
        pass

    def __enter__(self):
        return self.tgs
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        if _DEVELOPMENT is True:
            for tg in self.tgs:
                tg.end()
                pass
            pass

        return True
        pass

    def __iter__(self):
        for tg in self.tgs:
            yield tg
            pass
        pass
    pass

class TaskSourceTgsList(object):
    __slots__ = "tgs"

    def __init__(self, tgs):
        self.tgs = tgs
        pass

    def __enter__(self):
        return self.tgs
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        if _DEVELOPMENT is True:
            for o, tg in self.tgs:
                tg.end()
                pass
            pass

        return True
        pass

    def __iter__(self):
        for o, tg in self.tgs:
            yield o, tg
            pass
        pass
    pass

class TaskSourceTgw(object):
    __slots__ = "tgw"

    def __init__(self, tgw):
        self.tgw = tgw
        pass

    def __enter__(self):
        return self.tgw
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        if _DEVELOPMENT is True:
            for tg in self.tgw.itervalues():
                tg.end()
                pass
            pass

        return True
        pass

    def __iter__(self):
        for tg in self.tgw.itervalues():
            yield tg
            pass
        pass

class TaskDescBase(object):
    __slots__ = "caller_info"

    DEFAULT_CALLER = (None, None, None)

    def __init__(self):
        self.caller_info = TaskDescBase.DEFAULT_CALLER
        pass

    def setupCaller(self, deep, doc):
        self.caller_info = Trace.caller(deep) + (doc,)
        pass
    pass

class TaskDesc(TaskDescBase):
    __slots__ = "type", "params"

    def __init__(self, type, params):
        TaskDescBase.__init__(self)

        self.type = type
        self.params = params
        pass
    pass

class TaskGuardDesc(TaskDescBase):
    __slots__ = "guard_source", "guard_check", "enable", "guard", "args"

    def __init__(self, guard_source, guard_check, enable, guard, args):
        TaskDescBase.__init__(self)

        self.guard_source = guard_source
        self.guard_check = guard_check

        self.enable = enable
        self.guard = guard
        self.args = args
        pass
    pass

class TaskSwitchDesc(TaskDescBase):
    __slots__ = "switch", "cb", "args", "kwargs"

    def __init__(self, switch, cb, args, kwargs):
        TaskDescBase.__init__(self)

        self.switch = switch
        self.cb = cb
        self.args = args
        self.kwargs = kwargs
        pass
    pass

class TaskDictDesc(TaskDescBase):
    __slots__ = "switch", "cb", "args", "kwargs"

    def __init__(self, switch, cb, args, kwargs):
        TaskDescBase.__init__(self)

        self.switch = switch
        self.cb = cb
        self.args = args
        self.kwargs = kwargs
        pass
    pass

class TaskIfDesc(TaskDescBase):
    __slots__ = "fn", "args", "source_true", "source_false"

    def __init__(self, source_true, source_false, fn, args):
        TaskDescBase.__init__(self)

        self.fn = fn
        self.args = args
        self.source_true = source_true
        self.source_false = source_false
        pass
    pass

class TaskTryDesc(TaskDescBase):
    __slots__ = "type", "params", "source_true", "source_false"

    def __init__(self, source_true, source_false, type, params):
        TaskDescBase.__init__(self)

        self.type = type
        self.params = params
        self.source_true = source_true
        self.source_false = source_false
        pass
    pass

class TaskParallelDesc(TaskDescBase):
    __slots__ = "parallel"

    def __init__(self, parallel):
        TaskDescBase.__init__(self)

        self.parallel = parallel
        pass
    pass

class TaskRaceDesc(TaskDescBase):
    __slots__ = "race", "NoSkip", "RaceSkip"

    def __init__(self, race, NoSkip, RaceSkip):
        TaskDescBase.__init__(self)

        self.race = race
        self.NoSkip = NoSkip
        self.RaceSkip = RaceSkip
        pass
    pass

class TaskShiftCollectDesc(TaskDescBase):
    __slots__ = "index", "shiftCollect"

    def __init__(self, index, shiftCollect):
        TaskDescBase.__init__(self)

        self.index = index
        self.shiftCollect = shiftCollect
        pass
    pass

class TaskForDesc(TaskDescBase):
    __slots__ = "source", "iterator", "count"

    def __init__(self, source, iterator, count):
        TaskDescBase.__init__(self)

        self.source = source
        self.iterator = iterator
        self.count = count
        pass
    pass

class TaskRepeatDesc(TaskDescBase):
    __slots__ = "repeat", "until", "hasUntil"

    def __init__(self, repeat, until, hasUntil):
        TaskDescBase.__init__(self)

        self.repeat = repeat
        self.until = until
        self.hasUntil = hasUntil
        pass
    pass

class TaskForkDesc(TaskDescBase):
    __slots__ = "source"

    def __init__(self, source):
        TaskDescBase.__init__(self)

        self.source = source
        pass
    pass

class TaskSource(object):
    __slots__ = "source", "complete", "skiped", "doc"

    def __init__(self, source, skiped=False):
        super(TaskSource, self).__init__()

        self.source = source
        self.complete = False
        self.skiped = skiped
        self.doc = None
        pass

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source
        pass

    def extendSource(self, source):
        self.source.extend(source)
        pass

    def setSkiped(self, skiped):
        self.skiped = skiped
        pass

    def setDocument(self, doc):
        self.doc = doc
        pass

    def getDocument(self):
        return self.doc

    def isSkiped(self):
        return self.skiped

    def getSize(self):
        return len(self.source)

    def __addDesc(self, typeName, params):
        self.checkComplete()

        taskType = TaskManager.getTaskType(typeName)

        if taskType is None:
            raise TaskGeneratorException("invalid generate source [__addDesc] not found task '%s' with params: %s", typeName, params)
            pass

        self.__addDescType(taskType, params)
        pass

    def __addDescType(self, taskType, params):
        self.checkComplete()

        desc = TaskDesc(taskType, params)

        if _DEVELOPMENT is True:
            desc.setupCaller(3, self.doc)
            pass

        self.source.append(desc)
        pass

    def addTask(self, type, **params):
        self.__addDesc(type, params)
        pass

    def addWrapper(self, Wrapper, value):
        self.__addDesc("TaskSetWrapper", dict(Wrapper=Wrapper, Value=value))
        pass

    def addNotify(self, ID, *Args, **Kwds):
        self.__addDesc("TaskNotify", dict(ID=ID, Args=Args, Kwds=Kwds))
        pass

    def addListener(self, ID, Filter=None, *Args, **Kwds):
        self.__addDesc("TaskListener", dict(ID=ID, Filter=Filter, Args=Args, Kwds=Kwds))
        pass

    def addScopeListener(self, ID, Scope, *Args, **Kwds):
        self.__addDesc("TaskScopeListener", dict(ID=ID, Scope=Scope, Args=Args, Kwds=Kwds))
        pass

    def addWaitListener(self, Time, ID, Filter=None, Scheduler=None, *Args, **Kwds):
        winner = Wrapper(-1)

        with self.addRaceTask(2) as (source_wait, source_listener):
            source_wait.addDelay(Time, Scheduler=Scheduler)
            source_wait.addWrapper(winner, 0)
            source_listener.addListener(ID, Filter=Filter, *Args, **Kwds)
            source_listener.addWrapper(winner, 1)

        def __winned():
            value = winner.getValue()
            if value == 0:
                return False
            elif value == 1:
                return True
            else:
                raise TaskGeneratorException("invalid generate source [addWaitListener] winner value %s", value)

        return self.addIfTask(__winned)

    def addEvent(self, Event, Filter=None, *Args, **Kwds):
        self.__addDesc("TaskEvent", dict(Event=Event, Filter=Filter, Args=Args, Kwds=Kwds))
        pass

    def addScopeEvent(self, Event, Scope, *Args, **Kwds):
        self.__addDesc("TaskScopeEvent", dict(Event=Event, Scope=Scope, Args=Args, Kwds=Kwds))
        pass

    def addParam(self, object, param, value):
        self.__addDesc("TaskSetParam", dict(Object=object, Param=param, Value=value))
        pass

    def addPrint(self, msg, *args):
        if _DEVELOPMENT is True:
            self.__addDesc("TaskPrint", dict(Value=msg, Args=args))
        pass

    def addPrintFormat(self, msg, *args, **kwds):
        if _DEVELOPMENT is True:
            self.__addDesc("TaskPrintFormat", dict(Value=msg, Args=args, Kwds=kwds))
        pass

    def addDelay(self, Time, Scheduler=None):
        self.__addDesc("TaskDelay", dict(Time=Time, Scheduler=Scheduler))
        pass

    def addPlay(self, Object, **Kwds):
        self.__addDesc("TaskObjectPlay", dict(Object=Object, **Kwds))
        pass

    def addInterrupt(self, Object, **Kwds):
        self.__addDesc("TaskObjectInterrupt", dict(Object=Object, **Kwds))
        pass

    def addEnable(self, object, check=True):
        if check is False:
            if object is None:
                return
                pass
            pass

        self.__addDesc("TaskEnable", dict(Object=object, Value=True))
        pass

    def addDisable(self, object, check=True):
        if check is False:
            if object is None:
                return
                pass
            pass

        self.__addDesc("TaskEnable", dict(Object=object, Value=False))
        pass

    def addReturn(self, object):
        self.__addDesc("TaskObjectReturn", dict(Object=object))
        pass

    def addDummy(self, **kwrds):
        self.__addDesc("TaskDummy", dict(**kwrds))
        pass

    def addFunction(self, fn, *args, **kwds):
        self.__addDesc("TaskFunction", dict(Fn=fn, Args=args, Kwds=kwds))
        pass

    def addCallback(self, cb, *args, **kwds):
        self.__addDesc("TaskCallback", dict(Cb=cb, Args=args, Kwds=kwds))
        pass

    def addScope(self, scope, *args, **kwds):
        self.__addDesc("TaskScope", dict(Scope=scope, Args=args, Kwds=kwds))
        pass

    def addFork(self):
        self.checkComplete()

        desc = TaskForkDesc([])

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tg = TaskSource(desc.source, self.skiped)

        self.source.append(desc)

        return TaskSourceTg(tg)

    def addForkScope(self, scope=None, *args, **kwds):
        self.__addDesc("TaskFork", dict(Scope=scope, Args=args, Kwds=kwds))
        pass

    def addSemaphore(self, Semaphore, From=None, Less=None, To=None, Change=False):
        self.__addDesc("TaskSemaphore", dict(Semaphore=Semaphore, From=From, Less=Less, To=To, Change=Change))
        pass

    def increfSemaphore(self, Semaphore, Increment=None):
        self.__addDesc('TaskSemaphoreIncrement', dict(Semaphore=Semaphore, Increment=Increment))
        pass

    def lockSemaphore(self, Semaphore):
        self.__addDesc('TaskSemaphoreIncrement', dict(Semaphore=Semaphore, Increment=1))
        pass

    def unlockSemaphore(self, Semaphore):
        self.__addDesc('TaskSemaphoreIncrement', dict(Semaphore=Semaphore, Increment=-1))
        pass

    def trySemaphore(self, Semaphore):
        self.__addDesc("TaskSemaphore", dict(Semaphore=Semaphore, From=0))
        pass

    def addRefcount(self, Refcount, Increase=None):
        self.__addDesc("TaskRefcount", dict(Refcount=Refcount, Increase=Increase))
        pass

    def addBlock(self):
        self.__addDesc("TaskDeadLock", {})
        pass

    def addNoSkip(self):
        self.__addDesc("TaskNoSkip", {})
        pass

    def makeGuardSource(self, enable, guard, *args):
        self.checkComplete()

        desc = TaskGuardDesc([], [], enable, guard, args)

        if _DEVELOPMENT is True:
            desc.setupCaller(1, self.doc)
            pass

        tg_guard_source = TaskSource(desc.guard_source, self.skiped)

        tg_guard_check = TaskSource(desc.guard_check, self.skiped)
        tg_guard_check.addTask("TaskGuard", Enable=desc.enable, Guard=desc.guard, Args=desc.args)

        self.source.append(desc)

        return tg_guard_source

    def addGuardTask(self, enable, guard, *args):
        source = self.makeGuardSource(enable, guard, args)

        return TaskSourceTg(source)

    def addSwitchTask(self, count, cb, *args, **kwargs):
        self.checkComplete()

        desc = TaskSwitchDesc([], cb, args, kwargs)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        for i in xrange(count):
            source = []
            desc.switch.append(source)

            tg = TaskSource(source, self.skiped)
            tgs.append(tg)
            pass

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addScopeSwitch(self, scopes, cb, *args, **kwds):
        self.__addDesc("TaskScopeSwitch", dict(Scopes=scopes, Cb=cb, Args=args, Kwds=kwds))
        pass

    def addDictTask(self, Dict, cb, *args, **kwargs):
        self.checkComplete()

        desc = TaskDictDesc({}, cb, args, kwargs)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgw = {}

        for key in Dict:
            source = []
            desc.switch[key] = source

            tg = TaskSource(source, self.skiped)
            tgw[key] = tg
            pass

        self.source.append(desc)

        return TaskSourceTgw(tgw)

    def addTryTask(self, typeName, **params):
        self.checkComplete()

        taskType = TaskManager.getTaskType(typeName)

        if taskType is None:
            raise TaskGeneratorException("invalid generate source [addTryTask] not found task '%s' with params: %s", typeName, params)
            pass

        desc = TaskTryDesc([], [], taskType, params)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        tg_true = TaskSource(desc.source_true, self.skiped)
        tgs.append(tg_true)

        tg_false = TaskSource(desc.source_false, self.skiped)
        tgs.append(tg_false)

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addIfTask(self, fn, *args):
        self.checkComplete()

        desc = TaskIfDesc([], [], fn, args)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        tg_true = TaskSource(desc.source_true, self.skiped)
        tgs.append(tg_true)

        tg_false = TaskSource(desc.source_false, self.skiped)
        tgs.append(tg_false)

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addIfSemaphore(self, semaphore, value):
        self.checkComplete()

        desc = TaskIfDesc([], [], lambda: semaphore.equalValue(value), ())

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        tg_true = TaskSource(desc.source_true, self.skiped)
        tgs.append(tg_true)

        tg_false = TaskSource(desc.source_false, self.skiped)
        tgs.append(tg_false)

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addForTask(self, count):
        self.checkComplete()

        it = Iterator(0)

        desc = TaskForDesc([], it, count)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tg = TaskSource(desc.source, self.skiped)

        self.source.append(desc)

        return TaskSourceTgIter(it, tg)

    def addRepeatTask(self):
        self.checkComplete()

        desc = TaskRepeatDesc([], [], True)

        if _DEVELOPMENT is True:
            desc.setupCaller(1, self.doc)
            pass

        tgs = []

        repeat_tg = TaskSource(desc.repeat, self.skiped)
        tgs.append(repeat_tg)

        until_tg = TaskSource(desc.until, self.skiped)
        tgs.append(until_tg)

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addRepeatTaskScope(self, scope, *args, **kwds):
        self.checkComplete()

        desc = TaskRepeatDesc([], [], True)

        if _DEVELOPMENT is True:
            desc.setupCaller(1, self.doc)
            pass

        repeat_tg = TaskSource(desc.repeat, self.skiped)

        repeat_tg.addScope(scope, *args, **kwds)

        until_tg = TaskSource(desc.until, self.skiped)

        self.source.append(desc)

        return until_tg

    def addWhileTask(self):
        self.checkComplete()

        desc = TaskRepeatDesc([], [], False)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tg = TaskSource(desc.repeat, self.skiped)

        self.source.append(desc)

        return TaskSourceTg(tg)

    def addParallelTask(self, count):
        self.checkComplete()

        desc = TaskParallelDesc([])

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        for i in xrange(count):
            source = []
            desc.parallel.append(source)

            tg = TaskSource(source, self.skiped)
            tgs.append(tg)
            pass

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addParallelTaskList(self, objects):
        self.checkComplete()

        desc = TaskParallelDesc([])

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        for obj in objects:
            source = []
            desc.parallel.append(source)

            tg = TaskSource(source, self.skiped)
            tgs.append((obj, tg))
            pass

        self.source.append(desc)

        return TaskSourceTgsList(tgs)

    def addParallelTaskZip(self, *objects):
        return self.addParallelTaskList(list(zip(*objects)))

    def addRaceTask(self, count, NoSkip=False, RaceSkip=False):
        self.checkComplete()

        desc = TaskRaceDesc([], NoSkip, RaceSkip)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        for i in xrange(count):
            source = []
            desc.race.append(source)

            tg = TaskSource(source, self.skiped)
            tgs.append(tg)
            pass

        self.source.append(desc)

        return TaskSourceTgs(tgs)

    def addRaceTaskList(self, objects, NoSkip=False, RaceSkip=False):
        self.checkComplete()

        desc = TaskRaceDesc([], NoSkip, RaceSkip)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        tgs = []

        for obj in objects:
            source = []
            desc.race.append(source)

            tg = TaskSource(source, self.skiped)
            tgs.append((obj, tg))
            pass

        self.source.append(desc)

        return TaskSourceTgsList(tgs)

    def addRaceTaskZip(self, *objects, **Kwds):
        return self.addRaceTaskList(list(zip(*objects)), **Kwds)

    def addNotifyRequest(self, ID, Count, *Args, **Kwds):
        with self.addParallelTask(2) as (source_request, source_notify):
            source_notify.addNotify(ID, *Args, **Kwds)
            return source_request.addRaceTask(Count)
            pass
        pass

    def addShiftCollect(self, index, shiftCollect):
        self.checkComplete()

        desc = TaskShiftCollectDesc(index, shiftCollect)

        if _DEVELOPMENT is True:
            desc.setupCaller(0, self.doc)
            pass

        self.source.append(desc)
        pass

    def checkComplete(self):
        if self.complete is True:
            Trace.log("Task", 0, "TaskSource.checkComplete: error is end!")
            pass
        pass

    def end(self):
        self.complete = True
        pass
    pass

class TaskGenerator(object):
    __slots__ = "chain", "group", "source", "lastTask"

    def __init__(self, chain, group, source, lastTask):
        super(TaskGenerator, self).__init__()

        self.chain = chain
        self.group = group
        self.source = source

        self.lastTask = lastTask
        pass

    def parse(self):
        if self.chain is None:
            Trace.log("Task", 0, "TaskGenerator.parse chain is None")

            return None
            pass

        if isinstance(self.lastTask, TaskBase) is False:
            Trace.log("Task", 0, "TaskGenerator.parse lastTask is not TaskBase [%s]" % (self.lastTask))

            return None
            pass

        for element in self.source:
            if isinstance(element, TaskDesc) is True:
                task = self.chain.createTaskBaseTypeParams(element.type, self.group, element.caller_info, element.params)

                if task is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskDesc %s" % (element.type))

                    return None
                    pass

                self._addTask(task)
                pass
            elif isinstance(element, TaskGuardDesc) is True:
                tasks = []

                tg_guard_check = TaskGenerator(self.chain, self.group, element.guard_check, self.lastTask)
                tg_guard_check_lastTask = tg_guard_check.parse()

                if tg_guard_check_lastTask is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskGuardDesc source_check")

                    return None
                    pass

                tasks.append(tg_guard_check_lastTask)

                tg_guard_source = TaskGenerator(self.chain, self.group, element.guard_source, self.lastTask)
                tg_guard_source_lastTask = tg_guard_source.parse()

                if tg_guard_source_lastTask is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskGuardDesc")

                    return None
                    pass

                tasks.append(tg_guard_source_lastTask)

                self._addGuard(tasks, element)
                pass
            elif isinstance(element, TaskSwitchDesc) is True:
                tasks = []
                lasts = []
                for i, switch_source in enumerate(element.switch):
                    tci = self.chain.createTaskBaseParams("TaskDummy", self.group, element.caller_info, {})

                    if tci is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskDummy")

                        return None
                        pass

                    tasks.append(tci)

                    tg = TaskGenerator(self.chain, self.group, switch_source, tci)
                    lastTask = tg.parse()

                    if lastTask is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskSwitchDesc (%d)" % (i))

                        return None
                        pass

                    lasts.append(lastTask)
                    pass

                self._addSwitch(element, tasks, lasts)
                pass
            elif isinstance(element, TaskDictDesc) is True:
                tasks = {}
                lasts = {}
                for i, (switch_key, switch_source) in enumerate(element.switch.iteritems()):
                    tci = self.chain.createTaskBaseParams("TaskDummy", self.group, element.caller_info, {})

                    if tci is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskDummy")

                        return None
                        pass

                    tasks[switch_key] = tci

                    tg = TaskGenerator(self.chain, self.group, switch_source, tci)
                    lastTask = tg.parse()

                    if lastTask is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskSwitchDesc (%d)" % (i))

                        return None
                        pass

                    lasts[switch_key] = lastTask
                    pass

                self._addSwitch(element, tasks, lasts)
                pass
            elif isinstance(element, TaskIfDesc) is True:
                task = self.chain.createTaskBase("TaskIf", self.group, Caller=element.caller_info, Fn=element.fn, Args=element.args, Source_True=element.source_true, Source_False=element.source_false)

                if task is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskDesc %s" % ("TaskIf"))

                    return None
                    pass

                self._addTask(task)
                pass
            elif isinstance(element, TaskTryDesc) is True:
                task_type = self.chain.createTaskBaseTypeParams(element.type, self.group, element.caller_info, element.params)

                if task_type is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskDesc %s" % ("TaskTryDesc"))

                    return None
                    pass

                self._addTask(task_type)

                def __check_task_error(task_type):
                    if task_type.getError() is True:
                        return False
                        pass

                    return True
                    pass

                task_if = self.chain.createTaskBase("TaskIf", self.group, Caller=element.caller_info, Fn=__check_task_error, Args=(task_type,), Source_True=element.source_true, Source_False=element.source_false)

                if task_if is None:
                    Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskIf %s" % ("TaskTryDesc"))

                    return None
                    pass

                self._addTask(task_if)
                pass
            elif isinstance(element, TaskForDesc) is True:
                self._addFor(element)
                pass
            elif isinstance(element, TaskRepeatDesc) is True:
                self._addRepeat(element)
                pass
            elif isinstance(element, TaskForkDesc) is True:
                self._addFork(element)
                pass
            elif isinstance(element, TaskParallelDesc) is True:
                tasks = []
                for parallel_source in element.parallel:
                    tg = TaskGenerator(self.chain, self.group, parallel_source, self.lastTask)
                    lastTask = tg.parse()

                    if lastTask is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskParallelDesc")

                        return None
                        pass

                    tasks.append(lastTask)
                    pass

                self._addParallel(tasks, element)
                pass
            elif isinstance(element, TaskRaceDesc) is True:
                tasks = []
                for race_source in element.race:
                    tg = TaskGenerator(self.chain, self.group, race_source, self.lastTask)
                    lastTask = tg.parse()

                    if lastTask is None:
                        Trace.log("Task", 0, "TaskGenerator.parse invalid create task TaskRaceDesc")

                        return None
                        pass

                    tasks.append(lastTask)
                    pass

                self._addRace(tasks, element)
                pass
            elif isinstance(element, TaskShiftCollectDesc) is True:
                self._addShiftCollect(element)
                pass
            else:
                Trace.log("Task", 0, "TaskGenerator.parse invalid element type %s" % (element))

                return None
                pass
            pass

        lastTask = self.lastTask

        self.chain = None
        self.group = None
        self.source = None
        self.lastTask = None

        return lastTask
        pass

    def _addTask(self, task):
        if self.lastTask is not None:
            self.lastTask.addNext(task)
            pass

        self.lastTask = task
        pass

    def _addFor(self, element):
        task = self.chain.createTaskBase("TaskFor", self.group, Caller=element.caller_info, Source=element.source, Iterator=element.iterator, Count=element.count)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addFor invalid create task TaskFor")

            return
            pass

        self._addTask(task)
        pass

    def _addRepeat(self, element):
        task = self.chain.createTaskBase("TaskRepeat", self.group, Caller=element.caller_info, RepeatSource=element.repeat, UntilSource=element.until, HasUntil=element.hasUntil)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addRepeat invalid create task TaskRepeat")

            return
            pass

        self._addTask(task)
        pass

    def _addFork(self, element):
        task = self.chain.createTaskBase("TaskFork", self.group, Caller=element.caller_info, Source=element.source)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addFork invalid create task TaskFork")

            return
            pass

        self._addTask(task)
        pass

    def _addGuard(self, tasks, element):
        if len(tasks) == 0:
            return
            pass

        task = self.chain.createTaskBaseRace(self.group, False, True, element.caller_info)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addGuard invalid create task TaskRaceNeck")

            return
            pass

        for next in tasks:
            next.addNext(task)
            pass

        self.lastTask = task
        pass

    def _addSwitch(self, element, tasks, lasts):
        if len(tasks) == 0:
            return
            pass

        task = self.chain.createTaskBase("TaskSwitch", self.group, Caller=element.caller_info, Cb=element.cb, CbArgs=element.args, CbKwds=element.kwargs, Tasks=tasks, Lasts=lasts)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addSwitch invalid create task TaskSwitch")

            return
            pass

        self._addTask(task)
        pass

    def _addShiftCollect(self, element):
        PolicyShiftCollect = PolicyManager.getPolicy("ShiftCollect", "PolicySocketShiftCollect")
        task = self.chain.createTaskBase(PolicyShiftCollect, self.group, Caller=element.caller_info, Index=element.index, Collects=element.shiftCollect)

        self._addTask(task)
        pass

    def _addParallel(self, tasks, element):
        if len(tasks) == 0:
            return
            pass

        task = self.chain.createTaskBase("TaskParallelNeck", self.group, Caller=element.caller_info)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addParallel invalid create task TaskParallelNeck")

            return
            pass

        for next in tasks:
            next.addNext(task)
            pass

        self.lastTask = task
        pass

    def _addRace(self, tasks, element):
        if len(tasks) == 0:
            return
            pass

        task = self.chain.createTaskBaseRace(self.group, element.NoSkip, element.RaceSkip, element.caller_info)

        if task is None:
            Trace.log("Task", 0, "TaskGenerator._addRace invalid create task TaskRaceNeck")

            return
            pass

        for next in tasks:
            next.addNext(task)
            pass

        self.lastTask = task
        pass
    pass