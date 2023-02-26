from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.Task import Task

class TaskObjectAnimatableInterrupt(MixinEvent, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectAnimatableInterrupt, self)._onParams(params)
        self.NoSkipStop = params.get("NoSkipStop", False)
        pass

    def _onCheck(self):
        Animatable = self.getAnimatable()

        if Animatable is None:
            return False
            pass

        if Animatable.getPlay() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        Animatable = self.getAnimatable()

        Entity = Animatable.getEntity()

        if self.isSkiped() is True:
            if self.NoSkipStop is True:
                return True

            Entity.stop()
            Entity.setLastFrame()

            return True
            pass

        def __onAnimatableEndFilter(animatable, isStop):
            if isStop is True:
                self.setEventSkip(True)
                pass

            return True
            pass

        self.addEvent(Animatable.onAnimatableEnd, __onAnimatableEndFilter)

        if Entity.interrupt() is False:
            self.removeEvent()
            return True
            pass

        return False
        pass
    pass