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

        assert isinstance(self.Tasks, (list, dict)) is True
        assert isinstance(self.Tasks, list) is False or switchId >= 0 and switchId < len(self.Tasks)
        assert isinstance(self.Tasks, dict) is False or switchId in self.Tasks

        self.switched = True

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