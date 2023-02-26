from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

class TaskAnimatableInterrupt(MixinEvent, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimatableInterrupt, self)._onParams(params)
        self.Animatable = params.get("Animatable")
        self.Wait = params.get("Wait", True)
        pass

    def _onValidate(self):
        super(TaskAnimatableInterrupt, self)._onValidate()

        if Menge.isHomeless(self.Animatable) is True:
            self.validateFailed("Animatable %s is Homeless" % (self.Node.getName()))
            pass

        if self.Animatable.isActivate() is False:
            self.validateFailed("Animatable %s is Deactive" % (self.Node.getName()))
            pass
        pass

    def _onCheck(self):
        if self.Animatable is None:
            return False
            pass

        if self.Animatable.isPlay() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        if self.isSkiped() is True:
            self.Animatable.stop()
            return True
            pass

        if self.Wait is False:
            self.id = self.Animatable.play()

            return True
            pass

        def __onAnimatableEnd(id):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=False)
            pass

        def __onAnimatableStop(id):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=True)
            pass

        self.Animatable.setEventListener(onAnimatableEnd=__onAnimatableEnd)
        self.Animatable.setEventListener(onAnimatableStop=__onAnimatableStop)

        if self.Animatable.interrupt() is False:
            self.Animatable.setEventListener(onAnimatableEnd=None)
            self.Animatable.setEventListener(onAnimatableStop=None)

            return True
            pass

        return False
        pass
    pass