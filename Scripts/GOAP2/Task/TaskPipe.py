from MixinTime import MixinTime
from Task import Task

class TaskPipe(MixinTime, Task):
    __metaclass__ = finalslots("Scheduler", "Pipe", "Timing", "Event", "id")

    Skiped = True
    MixinTime_Validate_TimeZero = False

    def __init__(self):
        super(TaskPipe, self).__init__()

        self.Scheduler = None

        self.Pipe = None
        self.Timing = None
        self.Event = None

        self.id = None
        pass

    def _onFinalize(self):
        super(TaskPipe, self)._onFinalize()

        self.Scheduler = None

        self.Pipe = None
        self.Timing = None
        self.Event = None
        pass

    def _onParams(self, params):
        super(TaskPipe, self)._onParams(params)

        self.Scheduler = params.get("Scheduler", None)

        Pipe = params.get("Pipe", None)
        Timing = params.get("Timing", None)
        Event = params.get("Event", None)

        Args = params.get("Args", ())
        Kwds = params.get("Kwds", {})

        self.Pipe = FunctorStore(Pipe, Args, Kwds) if Pipe is not None else None
        self.Timing = FunctorStore(Timing, Args, Kwds) if Timing is not None else None
        self.Event = FunctorStore(Event, Args, Kwds) if Event is not None else None
        pass

    def _onRun(self):
        self.id = self.Scheduler.pipe(self.__onPipe, self.__onTiming, self.__onEvent)

        if self.id == 0:
            self.invalidTask("scheduler pipe invalid create")
            pass

        return False
        pass

    def __onPipe(self, id, index):
        if self.id != id:
            return
            pass

        return self.Pipe(index)
        pass

    def __onTiming(self, id, index, delay):
        if self.id != id:
            return
            pass

        self.Timing(index, delay)
        pass

    def __onEvent(self, id, isComplete):
        if self.id != id:
            return
            pass

        self.Event(isComplete)

        self.complete(isSkiped=isComplete is False)
        pass

    def _onSkip(self):
        remove_id = self.id
        self.id = None

        if self.Scheduler.remove(remove_id) is False:
            Trace.trace()
            pass
        pass
    pass