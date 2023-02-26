from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

class TaskEvent(MixinEvent, Task):
    __metaclass__ = finalslots("Event", "Filter")

    Skiped = False

    def _onParams(self, params):
        super(TaskEvent, self)._onParams(params)

        self.Event = params.get("Event")

        self.Filter = Utils.make_functor(params, "Filter")
        pass

    def _onValidate(self):
        super(TaskEvent, self)._onValidate()

        if isinstance(self.Event, Event) is False:
            self.validateFailed("Event must be Event but is %s" % (self.Event))
            pass

        if self.Filter is not None:
            if callable(self.Filter) is False:
                self.validateFailed("Filter %s is not callable" % (self.Filter))
                pass
            pass
        pass

    def _onRun(self):
        self.addEvent(self.Event, self.__onEventFilter)

        return False
        pass

    def __onEventFilter(self, *args, **kwargs):
        if self.Filter is not None:
            if _DEVELOPMENT is True:
                if Utils.is_valid_function_args(self.Filter, len(args) + len(kwargs)) is False:
                    self.log("%s filter %s is bad arguments or kwds" % (self.ID, self.Filter))

                    return False
                    pass
                pass

            result = self.Filter(*args, **kwargs)

            if isinstance(result, bool) is False:
                self.log("%s filter %s must retun bool [True|False] but return %s" % (self.Event.name, self.Filter, result))
                return False
                pass

            if result is False:
                return False
                pass
            pass

        return True
        pass
    pass