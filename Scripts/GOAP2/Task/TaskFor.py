from GOAP2.Task.Task import Task

from GOAP2.TaskManager import TaskManager

class TaskFor(Task):
    __metaclass__ = finalslots("forTaskChain", "Source", "Iterator", "Count", "AntiStackCycle")

    Skiped = True

    def __init__(self):
        super(TaskFor, self).__init__()

        self.forTaskChain = None

        self.Source = None
        self.Iterator = None
        self.Count = 0

        self.AntiStackCycle = 0
        pass

    def _onParams(self, params):
        super(TaskFor, self)._onParams(params)

        self.Source = params.get("Source")
        self.Iterator = params.get("Iterator")
        self.Count = params.get("Count")
        pass

    def _onFinalize(self):
        super(TaskFor, self)._onFinalize()

        self.Source = None

        if self.forTaskChain is not None:
            forTaskChain = self.forTaskChain
            self.forTaskChain = None
            forTaskChain.cancel()
            pass
        pass

    def _onCheck(self):
        if len(self.Source) == 0:
            self.invalidTask("TaskFor repeat source is empty")

            return False
            pass

        return True
        pass

    def _onRun(self):
        if self.__runTaskCycle() is False:
            return True
            pass

        return False
        pass

    def __initializeSourceTask(self, source, cb):
        chain = self.base.getChain()
        Group = chain.getGroup()

        taskChain = TaskManager.createTaskChain(Group=Group, Source=source, Cb=cb, AutoRun=False, AutoReg=False)

        if taskChain is None:
            return None
            pass

        return taskChain
        pass

    def __forComplete(self, isSkip):
        if self.isInitialized() is False:
            return
            pass

        if self.__runTaskCycle() is False:
            self.complete()
            pass
        pass

    def __runTaskCycle(self):
        if self.Iterator.isEqual(self.Count):
            self.forTaskChain = None

            return False
            pass

        self.forTaskChain = self.__initializeSourceTask(self.Source, self.__forComplete)

        if self.forTaskChain is None:
            return False
            pass

        if self.AntiStackCycle != 0:
            self.base._traceError("TaskFor Anti Stack Cycle")

            return False
            pass

        self.AntiStackCycle += 1

        if self.isSkiped() is False:
            if self.forTaskChain.run() is False:
                return False
                pass
            pass
        else:
            if self.forTaskChain.skip() is False:
                return False
                pass
            pass

        self.AntiStackCycle -= 1

        self.Iterator.incref(1)

        return True
        pass

    def _onSkip(self):
        #        if self.repeatTask is not None:
        #            self.repeatTask.cancel()
        #            pass
        #
        #        if self.untilTask is not None:
        #            self.untilTask.cancel()
        #            pass
        pass
    pass