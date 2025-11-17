from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.Task import Task

class TaskAnimatableEnd(MixinEvent, Task):
    Skiped = True

    def _onCheck(self):
        Animatable = self.getAnimation()

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

        self.addEvent(Animatable.onAnimatableEnd, __onAnimatableEndFilter)

        return False
    pass