from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager

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
    else:
        IDLE = 0
        INVALID = 1
        RUN = 3
        SKIP = 4
        STOP = 5
        CANCEL = 6
        COMPLETE = 7
        END = 8
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
        pass

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
        pass

    def setChain(self, chain):
        self.chain = chain
        pass

    def getChain(self):
        return self.chain
        pass

    def addNext(self, task):
        if task is None:
            Trace.log("Task", 0, "TaskBase.addNext %s invalid add 'None'" % (self))
            return
            pass

        self.nexts.append(task)
        task._addPrev(self)
        pass

    def getNexts(self):
        return self.nexts
        pass

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
        pass

    def isIdle(self):
        return self.state is TaskBase.IDLE
        pass

    def isRunning(self):
        return self.state is TaskBase.RUN
        pass

    def isEnd(self):
        return self.state is TaskBase.END
        pass

    def __createTask(self):
        if self.task is not None:
            return True
            pass

        task = TaskManager.createTask(self.taskType, self, self.chain, self.taskGroup, self.taskParams)

        if task is None:
            Trace.log("Task", 0, "invalid create %s" % (self))

            return False
            pass

        if self.taskSkiped is not None:
            task.Skiped = self.taskSkiped
            pass

        if task.onInitialize() is False:
            Trace.log("Task", 0, "invalid initialize %s" % (self))

            return False
            pass

        if _DEVELOPMENT is True:
            if task.onValidate() is False:
                Trace.log("Task", 0, "invalid validate %s" % (self))

                return False
                pass
            pass

        self.task = task

        return True
        pass

    def __checkTask(self):
        try:
            isCheck = self.task._onCheck()
        except Exception as ex:
            traceback.print_exc()

            self._onTaskCheckFailed(ex)

            return False
            pass

        if _DEVELOPMENT is True:
            if isinstance(isCheck, bool) is False:
                Trace.log("Task", 0, "TaskBase.run: %s _onCheck must return [True|False] but return %s" % (self, isCheck))

                return False
                pass
            pass

        return isCheck
        pass

    def __checkSkipTask(self):
        if self.task is None:
            return
            pass

        try:
            self.task._onCheckSkip()
        except Exception as ex:
            traceback.print_exc()

            self._onTaskCheckSkipFailed(ex)

            return
            pass
        pass

    def __onTaskRun(self, task):
        try:
            isComplete = task._onRun()
        except Exception as ex:
            traceback.print_exc()

            self._onTaskRunFailed(ex)

            return False, False
            pass

        if _DEVELOPMENT is True:
            if isinstance(isComplete, bool) is False:
                Trace.log("Task", 0, "TaskBase.run: %s _onRun must return [True|False] but return %s" % (self, isComplete))

                return False, False
                pass
            pass

        return True, isComplete
        pass

    def __onTaskSkip(self, task):
        try:
            task._onSkip()
        except Exception as ex:
            traceback.print_exc()

            self._onTaskSkipFailed(ex)

            return False
            pass

        return True
        pass

    def run(self, checkSkipedFalse=False):
        if self.state is not TaskBase.IDLE:
            Trace.log("Task", 0, "TaskBase.run: %s invalid run [state %s]" % (self, self.state))
            return False
            pass

        self.state = TaskBase.RUN

        self.chain.runTask(self)

        if self.__createTask() is False:
            self._traceError("TaskBase run create task '%s'" % (self))

            return False
            pass

        isCheck = self.__checkTask()

        if isCheck is False:
            self.__checkSkipTask()

            self.complete(isRunning=False)

            return True
            pass

        result, isComplete = self.__onTaskRun(self.task)

        if result is False:
            return False
            pass

        if self.state is not TaskBase.RUN:
            return True
            pass

        if isComplete is True:
            if checkSkipedFalse is True:
                if self.task.SkipBlock is True:
                    if self.task._onSkipBlock() is True:
                        self.complete()
                        pass

                    return True
                    pass

                if self.task.Skiped is False:
                    self._traceError("TaskBase.run: %s checkSkipedFalse from skip _onRun return [True] and Skiped is False" % (self))

                    return False
                    pass
                pass

            self.complete()
            pass

        return True
        pass

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
        pass

    def skip(self):
        if self.state is TaskBase.SKIP:
            return True
            pass

        if self.state is TaskBase.END:
            return True
            pass

        # print("TaskBase.skip %s [%s] chain %s:%s state %s" % (self, id(self), id(self.chain), self.chain.name, self.state))

        if self.skiped is True:
            Trace.log("Task", 0, "TaskBase.skip %s skip already %d" % (self, id(self)))

            return False
            pass

        if self.__createTask() is False:
            self._traceError("TaskBase skip create task '%s'" % (self))
            # Trace.log("Task", 0, "TaskBase.skip invalid create task %s"%(self))
            return False
            pass

        if self.task.Skiped is False:
            if self.state is TaskBase.IDLE:
                if self.run(True) is False:
                    return False
                    pass
                pass
            else:
                self.task._onSkipNoSkiped()
                pass

            return True
            pass

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
                        pass

                    if self.state is TaskBase.END:
                        return True
                        pass

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
        pass

    def cancel(self):
        if self.state is TaskBase.END:
            return
            pass

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
            pass

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
            pass

        if self.state is TaskBase.END:
            return
            pass

        if self.state is TaskBase.CANCEL:
            return
            pass

        if self.state is not TaskBase.RUN:
            Trace.log("Task", 0, "TaskBase.complete %s invalid state - %s" % (self, self.state))
            return
            pass

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
            pass

        if self.isInitialized() is False:
            Trace.log("Task", 0, "TaskBase._prevSkip %s skip prev %s invalid initialize state %s" % (self, task, self.state))
            return False
            pass

        if task not in self.prevs:
            Trace.log("Task", 0, "TaskBase._prevSkip %s  invalid prev task %s" % (self, task))
            return False
            pass

        self.prevs.remove(task)

        if self._checkSkip() is False:
            return False
            pass

        self._cancelPrev()

        if self.state is TaskBase.END:
            return False
            pass

        return True
        pass

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
                pass

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
            pass

        if task not in self.prevs:
            Trace.log("Task", 0, "TaskBase._prevComplete %s not found prev task %s" % (self, task))
            pass

        self.prevs.remove(task)

        if self._checkRun() is False:
            return False
            pass

        self._cancelPrev()

        if self.state is TaskBase.END:
            return False
            pass

        return True
        pass

    def _checkRun(self):
        if len(self.prevs) == 0:
            return True
            pass

        return False
        pass

    def _checkSkip(self):
        if len(self.prevs) == 0:
            return True
            pass

        return False
        pass

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