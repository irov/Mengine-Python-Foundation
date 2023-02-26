from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

class TaskObjectAnimatableEnd(MixinEvent, Task):
    Skiped = True

    def _onCheck(self):
        Animatable = self.getAnimatable()

        if Animatable is None:
            self.log("Animatable is None")
            return False
            pass

        if Animatable.getPlay() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        Animatable = self.getAnimatable()

        def __onAnimatableEndFilter(animatable, isStop):
            if isStop is True:
                self.setEventSkip(True)
                pass

            return True
            pass

        self.addEvent(Animatable.onAnimatableEnd, __onAnimatableEndFilter)

        return False
        pass
    pass