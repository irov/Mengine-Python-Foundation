from Foundation.Task.MixinNode import MixinNode
from Foundation.Task.Task import Task

class TaskNodeMovieEvent(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeMovieEvent, self)._onParams(params)
        self.Event = params.get("Event")

        self.Filter = Utils.make_functor(params, "Filter")
        pass

    def _onValidate(self):
        super(TaskNodeMovieEvent, self)._onValidate()

        if self.node.hasMovieEvent(self.Event) is False:
            self.validateFailed("NodeMovie '%s' not exist event '%s'" % (self.node.getName(), self.Event))
            pass

        if self.Filter is not None:
            if Utils.is_valid_functor_args(self.Filter, 1) is False:
                self.validateFailed("NodeMovie %s filter %s is bad arguments or kwds" % (self.node.getName(), self.Filter))
                pass
            pass
        pass

    def _onRun(self):
        def __onEvent(position, isEnd):
            if self.Filter is not None:
                result = self.Filter(position)

                if isinstance(result, bool) is False:
                    self.log("[%s] filter %s must retun bool [True|False] but return %s" % (self.ID, self.Filter, result))

                    return
                    pass

                if result is False:
                    return
                    pass
                pass

            self.complete(isSkiped=isEnd is False)
            pass

        self.node.setMovieEvent(self.Event, __onEvent)

        return False
        pass

    def _onSkip(self):
        super(TaskNodeMovieEvent, self)._onSkip()

        self.node.removeMovieEvent(self.Event)
        pass
    pass