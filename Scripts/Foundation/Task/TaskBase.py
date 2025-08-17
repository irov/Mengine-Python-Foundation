from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from Foundation.Task.Task import TaskException

class TaskBase(Initializer):
    __metaclass__ = finalslots("taskType", "taskGroup", "taskParams", "taskSkiped", "chain", "task", "nexts", "prevs", "state", "caller", "skiped", "error")

    DEFAULT_CALLER = (None, None, None)

    if _DEVELOPMENT is True:
        IDLE = "IDLE"
        INVALID = "INVALID"
        RUN = "RUN"
        SKIP = "SKIP"
        STOP = "STOP"
        CANCEL = "CANCEL"
        COMPLETE = "COMPLETE"
        END = "END"
        __task_validation = Mengine.hasOption("notaskvalidation") is False
    else:
        IDLE = 0
        INVALID = 1
        RUN = 3
        SKIP = 4
        STOP = 5
        CANCEL = 6
        COMPLETE = 7
        END = 8
        __task_validation = False
        pass

    def __init__(self):
        super(TaskBase, self).__init__()

        self.taskType = None
        self.taskGroup = None
        self.taskParams = None
        self.taskSkiped = None

        self.chain = None

        self.task = None

        self.nexts = []
        self.prevs = []

        self.state = TaskBase.INVALID

        self.caller = TaskBase.DEFAULT_CALLER

        self.skiped = False
        self.error = False
        pass

    def __repr__(self):
        return "{} caller '{}:{}' doc '{}'".format(self.taskType.__name__, self.caller[0], self.caller[1], self.caller[2])

    def setTaskType(self, taskType):
        self.taskType = taskType
        pass

    def setTaskGroup(self, taskGroup):
        self.taskGroup = taskGroup
        pass

    def setTaskParams(self, taskParams):
        self.taskParams = taskParams
        pass

    def setTaskSkiped(self, skiped):
        self.taskSkiped = skiped
        pass

    def setCaller(self, caller):
        self.caller = caller
        pass

    def setError(self, error):
        self.error = error
        pass

    def getError(self):
        return self.error

    def setChain(self, chain):
        self.chain = chain
        pass

    def getChain(self):
        return self.chain

    def addNext(self, task):
        if task is None:
            Trace.log("Task", 0, "TaskBase.addNext %s invalid add 'None'" % (self))
            return

        self.nexts.append(task)
        task._addPrev(self)
        pass

    def getNexts(self):
        return self.nexts

    def _addPrev(self, task):
        self.prevs.append(task)
        pass

    def popNexts(self):
        nexts = self.nexts

        for next in self.nexts:
            next.prevs.remove(self)
            pass

        self.nexts = []

        return nexts

    def isIdle(self):
        return self.state is TaskBase.IDLE

    def isRunning(self):
        return self.state is TaskBase.RUN

    def isEnd(self):
        return self.state is TaskBase.END

    def __createTask(self, Skiped):
        if self.task is not None:
            return True

        task = TaskManager.createTask(self.taskType, self, self.chain, self.taskGroup, self.taskParams)

        if task is None:
            Trace.log("Task", 0, "invalid create %s" % (self))

            return False

        if self.taskSkiped is not None:
            task.Skiped = self.taskSkiped
            pass

        if task.onInitialize() is False:
            Trace.log("Task", 0, "invalid initialize %s" % (self))

            return False

        if self.__task_validation is True:
            if Skiped is False:
                if task.onValidate() is False:
                    Trace.log("Task", 0, "invalid validate %s" % (self))

                    return False
                pass
            pass

        self.task = task

        return True

    def __checkTask(self):
        try:
            isCheck = self.task._onCheck()
        except Exception as ex:
            self._onTaskCheckFailed("%s\n%s" % (ex, traceback.format_exc()))

            return False

        if _DEVELOPMENT is True:
            if isinstance(isCheck, bool) is False:
                Trace.log("Task", 0, "TaskBase.run: %s _onCheck must return [True|False] but return %s" % (self, isCheck))

                return False
                pass
            pass

        return isCheck

    def __checkSkipTask(self):
        if self.task is None:
            return

        try:
            self.task._onCheckSkip()
        except Exception as ex:
            self._onTaskCheckSkipFailed("%s\n%s" % (ex, traceback.format_exc()))

            return

    def __onTaskRun(self, task):
        try:
            isComplete = task._onRun()
        except TaskException as ex:
            self._onTaskRunFailed("%s\n%s" % (ex, traceback.format_exc()))

            return False, False

        if _DEVELOPMENT is True:
            if isinstance(isComplete, bool) is False:
                Trace.log("Task", 0, "TaskBase.run: %s _onRun must return [True|False] but return %s" % (self, isComplete))

                return False, False
            pass

        return True, isComplete

    def __onTaskSkip(self, task):
        try:
            task._onSkip()
        except Exception as ex:
            self._onTaskSkipFailed("%s\n%s" % (ex, traceback.format_exc()))

            return False

        return True

    def run(self, checkSkipedFalse=False):
        if self.state is not TaskBase.IDLE:
            Trace.log("Task", 0, "TaskBase.run: %s invalid run [state %s]" % (self, self.state))
            return False

        self.state = TaskBase.RUN

        self.chain.runTask(self)

        if self.__createTask(False) is False:
            self._traceError("TaskBase run create task '%s'" % (self))

            return False

        isCheck = self.__checkTask()

        if isCheck is False:
            self.__checkSkipTask()

            self.complete(isRunning=False)

            return True

        result, isComplete = self.__onTaskRun(self.task)

        if result is False:
            return False

        if self.state is not TaskBase.RUN:
            return True

        if isComplete is True:
            if checkSkipedFalse is True:
                if self.task.SkipBlock is True:
                    if self.task._onSkipBlock() is True:
                        self.complete()
                        pass

                    return True

                if self.task.Skiped is False:
                    self._traceError("TaskBase.run: %s checkSkipedFalse from skip _onRun return [True] and Skiped is False" % (self))

                    return False
                pass

            self.complete()
            pass

        return True

    def _traceException(self, err):
        msg = err
        msg += "\n"
        msg += "create '%s:%s' doc ('%s')" % (self.caller[0], self.caller[1], self.caller[2])

        if self.chain is not None:
            chain_caller = self.chain.getCaller()
            if chain_caller is not None:
                msg += "\n"
                msg += "in task chain name '%s' group '%s' created '%s:%s' doc ('%s')" % (self.chain.name, self.chain.GroupName, chain_caller[0], chain_caller[1], chain_caller[2])
                pass
            pass

        msg += '\n'
        msg += traceback.format_exc()

        Trace.log("Task", 0, msg)

    def _traceError(self, err):
        msg = err
        msg += "\n"
        msg += "create '%s:%s' doc ('%s')" % (self.caller[0], self.caller[1], self.caller[2])

        if self.chain is not None:
            chain_caller = self.chain.getCaller()
            if chain_caller is not None:
                msg += "\n"
                msg += "in task chain name '%s' group '%s' created '%s:%s' doc ('%s')" % (self.chain.name, self.chain.GroupName, chain_caller[0], chain_caller[1], chain_caller[2])
                pass
            pass

        Trace.log("Task", 0, msg)
        pass

    def _onTaskRunFailed(self, msg):
        self._traceError("TaskBase run '%s' is except '%s'" % (self, msg))
        pass

    def _onTaskCheckFailed(self, msg):
        self._traceError("TaskBase check '%s' is except '%s'" % (self, msg))
        pass

    def _onTaskCheckSkipFailed(self, msg):
        self._traceError("TaskBase check skip '%s' is except '%s'" % (self, msg))
        pass

    def _onTaskSkipFailed(self, msg):
        self._traceError("TaskBase skip '%s' is except '%s'" % (self, msg))
        pass

    def _onInitialize(self):
        super(TaskBase, self)._onInitialize()

        self.state = TaskBase.IDLE
        pass

    def _onInitializeFailed(self, msg):
        self.state = TaskBase.INVALID

        self._traceError("TaskBase '%s' is not initialized '%s'" % (self, msg))
        pass

    def _onFinalizeFailed(self, msg):
        self.state = TaskBase.INVALID

        self._traceError("TaskBase '%s' is not finalized '%s'" % (self, msg))
        pass

    def _onFinalize(self):
        super(TaskBase, self)._onFinalize()

        if self.task is not None:
            self.task.onFinalize()
            self.task = None
            pass

        self.nexts = None
        self.prevs = None

        self.chain = None

        self.state = TaskBase.END

        self.caller = TaskBase.DEFAULT_CALLER
        pass

    def isSkiped(self):
        return self.skiped

    def skip(self):
        if self.state is TaskBase.SKIP:
            return True

        if self.state is TaskBase.END:
            return True

        #print("TaskBase.skip %s [%s] chain: %s:%s state: %s group: %s [%d]" % (self, id(self), id(self.chain), self.chain.name, self.state, self.taskGroup, self.taskGroup.getEnable() if self.taskGroup is not None else -1))

        if self.skiped is True:
            Trace.log("Task", 0, "TaskBase.skip %s skip already %d" % (self, id(self)))

            return False

        if self.__createTask(True) is False:
            self._traceError("TaskBase skip create task '%s'" % (self))
            # Trace.log("Task", 0, "TaskBase.skip invalid create task %s"%(self))
            return False

        if self.task.Skiped is False:
            if self.state is TaskBase.IDLE:
                if self.run(True) is False:
                    return False
                pass
            else:
                self.task._onSkipNoSkiped()
                pass

            return True

        self.skiped = True

        if self.state is TaskBase.IDLE:
            self.chain.runTask(self)

            self.state = TaskBase.RUN

            isCheck = self.__checkTask()

            if isCheck is True:
                if self.task._onFastSkip() is True:
                    self.state = TaskBase.SKIP
                else:
                    result, isCompleted = self.__onTaskRun(self.task)

                    if result is False:
                        return False

                    if self.state is TaskBase.END:
                        return True

                    self.state = TaskBase.SKIP

                    if isCompleted is False:
                        self.__onTaskSkip(self.task)
                        pass
                    pass
                pass

            self.task._onFinally()

            self._taskSkip()
            pass
        elif self.state is TaskBase.RUN:
            self.state = TaskBase.SKIP

            self.__onTaskSkip(self.task)

            self.task._onFinally()

            self._taskSkip()
            pass

        if self.state is not TaskBase.END:
            self.onFinalize()
            pass

        return True

    def cancel(self):
        if self.state is TaskBase.END:
            return

        self.skiped = True

        if self.state is TaskBase.RUN:
            self.state = TaskBase.CANCEL

            if self.task is not None:
                self.__onTaskSkip(self.task)
                self.task._onCancel()
                self.task._onFinally()
                pass

            self.chain.completeTask(self)
            pass

        self.onFinalize()
        pass

    def _taskSkip(self):
        if self.state is TaskBase.END:
            return

        self.chain.completeTask(self)

        for next in self.nexts[:]:
            if next._prevSkip(self) is True:
                self.chain.processTask(next, True)
                # next.skip()
                pass
            pass
        pass

    def complete(self, isRunning=True, isSkiped=False):
        if self.state is TaskBase.SKIP:
            return

        if self.state is TaskBase.END:
            return

        if self.state is TaskBase.CANCEL:
            return

        if self.state is not TaskBase.RUN:
            Trace.log("Task", 0, "TaskBase.complete %s invalid state - %s" % (self, self.state))
            return

        if isSkiped is True:
            self.skiped = True
            self.state = TaskBase.SKIP
            pass
        else:
            self.state = TaskBase.COMPLETE
            pass

        if isRunning is True:
            self.task._onComplete()
            self.task._onFinally()
            pass

        self.state = TaskBase.END

        self.chain.completeTask(self)

        if self.skiped is False:
            for next in self.nexts[:]:
                if next._prevComplete(self) is True:
                    self.chain.processTask(next, False)
                    # next.run()
                    pass
                pass
            pass
        else:
            for next in self.nexts[:]:
                if next._prevSkip(self) is True:
                    self.chain.processTask(next, True)
                    # next.skip()
                    pass
                pass
            pass

        self.onFinalize()
        pass

    def _prevSkip(self, task):
        if self.state is TaskBase.END:
            return False

        if self.isInitialized() is False:
            Trace.log("Task", 0, "TaskBase._prevSkip %s skip prev %s invalid initialize state %s" % (self, task, self.state))
            return False

        if task not in self.prevs:
            Trace.log("Task", 0, "TaskBase._prevSkip %s  invalid prev task %s" % (self, task))
            return False

        self.prevs.remove(task)

        if self._checkSkip() is False:
            return False

        self._cancelPrev()

        if self.state is TaskBase.END:
            return False

        return True

    def _skipPrev(self):
        for prev in self.prevs[:]:
            if prev.state is TaskBase.RUN:
                prev.skip()
                prev.cancel()
            elif prev.state is TaskBase.IDLE:
                prev._skipPrev()
                prev._cancelPrev()
                pass
            pass
        pass

    def _cancelPrev(self):
        cancelPrevQueue = []

        for prev in self.prevs[:]:
            if prev.state is TaskBase.RUN:
                prev.cancel()
                pass
            elif prev.state is TaskBase.IDLE:
                cancelPrevQueue.append(prev)
                pass
            pass

        while len(cancelPrevQueue) != 0:
            element = cancelPrevQueue.pop(0)

            if element.state is not TaskBase.IDLE:
                continue

            for prev in element.prevs[:]:
                if prev.state is TaskBase.RUN:
                    prev.cancel()
                    pass
                elif prev.state is TaskBase.IDLE:
                    cancelPrevQueue.append(prev)
                    pass
                pass

            element.cancel()
            pass
        pass

    def _prevComplete(self, task):
        if self.state is not TaskBase.IDLE:
            return False

        if task not in self.prevs:
            Trace.log("Task", 0, "TaskBase._prevComplete %s not found prev task %s" % (self, task))
            pass

        self.prevs.remove(task)

        if self._checkRun() is False:
            return False

        self._cancelPrev()

        if self.state is TaskBase.END:
            return False

        return True

    def _checkRun(self):
        if len(self.prevs) == 0:
            return True

        return False

    def _checkSkip(self):
        if len(self.prevs) == 0:
            return True

        return False

    def _taskPrint(self, ident=0):
        s = ""
        for i in xrange(ident):
            s += " "
            pass

        print(s, self, id(self))

        for next in self.nexts:
            next._taskPrint(ident + 2)
            pass
        pass

    def _onFinalizeFailed(self, msg):
        self.state = TaskBase.INVALID

        Trace.log("Task", 0, "TaskBase '%s' onFinalize failed: %s" % (self, msg))
        pass
    pass