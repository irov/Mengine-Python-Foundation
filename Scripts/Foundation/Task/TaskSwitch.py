from Foundation.Task.Task import Task

class TaskSwitch(Task):
    __metaclass__ = finalslots("Cb", "CbArgs", "CbKwargs", "Tasks", "Lasts", "switched")

    Skiped = True

    def __init__(self):
        super(TaskSwitch, self).__init__()

        self.switched = False
        pass

    def _onParams(self, params):
        super(TaskSwitch, self)._onParams(params)

        self.Cb = params.get("Cb")
        self.CbArgs = params.get("CbArgs", ())
        self.CbKwargs = params.get("CbKwargs", {})
        self.Tasks = params.get("Tasks")
        self.Lasts = params.get("Lasts")
        pass

    def _onRun(self):
        skiped = self.isSkiped()

        self.Cb(*((skiped, self._onSwitch) + self.CbArgs), **self.CbKwargs)

        return False
        pass

    def _onSwitch(self, isSkip, switchId, *args):
        if self.isInitialized() is False:
            self.log("_onSwitch already finalized")
            return
            pass

        if self.switched is True:
            self.log("_onSwitch already switched!")
            return
            pass

        self.switched = True

        if isinstance(self.Tasks, list) is True:
            if switchId >= len(self.Tasks):
                self.log("_onSwitch id '%s' more source switch length '%d'" % (switchId, len(self.Tasks)))
                return
                pass
            pass
        elif isinstance(self.Tasks, dict) is True:
            if switchId not in self.Tasks:
                self.log("_onSwitch id '%s' not in source switch '%s'" % (switchId, self.Tasks.keys()))
                return
                pass
            pass

        firstTask = self.Tasks[switchId]
        lastTask = self.Lasts[switchId]

        nexts = self.base.popNexts()

        for next in nexts:
            lastTask.addNext(next)
            pass

        self.base.addNext(firstTask)

        if isSkip is False:
            self.complete()
            pass
        pass

    def _onFinalize(self):
        super(TaskSwitch, self)._onFinalize()

        # if self.switched is False:
        #     self.Cb(*((True, None) + self.CbArgs), **self.CbKwargs)
        #     pass

        self.Cb = None
        self.CbArgs = None
        self.CbKwargs = None

        self.Tasks = None
        self.Lasts = None
        pass
    pass