from Foundation.Task.Task import Task

from Foundation.TaskManager import TaskManager

class TaskRepeat(Task):
    __metaclass__ = finalslots("repeatTaskChain", "untilTaskChain", "isRepeat", "RepeatSource", "UntilSource", "HasUntil", "Wait", "AntiStackCycle")

    Skiped = False

    def __init__(self):
        super(TaskRepeat, self).__init__()

        self.repeatTaskChain = None
        self.untilTaskChain = None

        self.isRepeat = True

        self.RepeatSource = None
        self.UntilSource = None
        self.HasUntil = None
        self.Wait = None

        self.AntiStackCycle = 0
        pass

    def _onParams(self, params):
        super(TaskRepeat, self)._onParams(params)

        self.RepeatSource = params.get("RepeatSource")
        self.UntilSource = params.get("UntilSource")
        self.HasUntil = params.get("HasUntil")
        self.Wait = params.get("Wait", False)
        pass

    def _onFinalize(self):
        super(TaskRepeat, self)._onFinalize()

        self.isRepeat = False

        self.RepeatSource = None
        self.UntilSource = None

        if self.repeatTaskChain is not None:
            repeatTaskChain = self.repeatTaskChain
            self.repeatTaskChain = None
            repeatTaskChain.cancel()
            pass

        if self.untilTaskChain is not None:
            untilTaskChain = self.untilTaskChain
            self.untilTaskChain = None
            untilTaskChain.cancel()
            pass
        pass

    def _onCheck(self):
        if self.HasUntil is True:
            if len(self.UntilSource) == 0:
                self.invalidTask("TaskRepeat until source is empty")

                return False
            pass

        if len(self.RepeatSource) == 0:
            self.invalidTask("TaskRepeat repeat source is empty")

            return False

        return True

    def _onRun(self):
        if self.HasUntil is True:
            self.untilTaskChain = self.__initializeSourceTask(self.UntilSource, self.__untilComplete)

            if self.untilTaskChain is None:
                self.invalidTask("TaskRepeat._onRun invalid initialize UntilSource")

                return True

            if self.untilTaskChain.run() is False:
                self.repeatTaskChain.cancel()

                return True
            pass

        if self.isRepeat is False:
            return True

        self.repeatTaskChain = self.__initializeSourceTask(self.RepeatSource, self.__repeatComplete)

        if self.repeatTaskChain is None:
            self.invalidTask("TaskRepeat._onRun invalid initialize RepeatSource")

            return True

        if self.repeatTaskChain.run() is False:
            return True

        return False

    def __initializeSourceTask(self, source, cb):
        chain = self.base.getChain()
        Group = chain.getGroup()

        task = TaskManager.createTaskChain(Caller=self.base.caller, Group=Group, Source=source, Cb=cb, AutoRun=False, AutoReg=False)

        if task is None:
            return None

        return task

    def __repeatComplete(self, isSkip):
        if self.isRepeat is False:
            return

        if isSkip is True:
            self.complete()
            return

        self.repeatTaskChain = self.__initializeSourceTask(self.RepeatSource, self.__repeatComplete)

        if self.repeatTaskChain is None:
            return

        if self.AntiStackCycle != 0:
            self.base._traceError("TaskRepeat Anti Stack Cycle")

            self.complete()
            return

        self.AntiStackCycle += 1

        if self.repeatTaskChain.run() is False:
            self.complete()
            pass

        self.AntiStackCycle -= 1
        pass

    def __untilComplete(self, isSkip):
        self.isRepeat = False

        if self.Wait is False:
            if self.repeatTaskChain is not None:
                repeatTaskChain = self.repeatTaskChain
                self.repeatTaskChain = None
                repeatTaskChain.cancel()
                pass

            #            if isSkip is False:
            self.complete()
            #                pass
            pass
        pass

    def _onSkip(self):
        # if self.repeatTaskChain is not None:
        #     self.repeatTaskChain.cancel()
        #     pass
        #
        # if self.untilTaskChain is not None:
        #     self.untilTaskChain.cancel()
        #     pass

        pass