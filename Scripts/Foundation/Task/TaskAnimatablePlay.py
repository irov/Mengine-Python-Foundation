from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.Task import Task

class TaskAnimatablePlay(MixinEvent, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimatablePlay, self)._onParams(params)
        self.Animatable = params.get("Animatable")
        self.Loop = params.get("Loop", None)
        self.Wait = params.get("Wait", True)
        self.StartTiming = params.get("StartTiming", None)
        self.SpeedFactor = params.get("SpeedFactor", None)
        self.Time = params.get("Time", None)
        self.DefaultSpeedFactor = params.get("DefaultSpeedFactor", None)
        self.LastFrame = params.get("LastFrame", True)
        self.AutoEnable = params.get("AutoEnable", False)
        self.Destroy = params.get("Destroy", False)
        self.Rewind = params.get("Rewind", False)

        self.id = None
        pass

    def _onValidate(self):
        super(TaskAnimatablePlay, self)._onValidate()

        if Menge.isHomeless(self.Animatable) is True:
            self.validateFailed("Animatable %s is Homeless" % (self.Animatable.getName()))
            pass

        Enable = self.Animatable.isEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Animatable %s is Disable" % (self.Animatable.getName()))
            pass
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Animatable.enable()
            pass

        if self.StartTiming is not None:
            self.Animatable.setStartTiming(self.StartTiming)
            pass

        if self.Rewind is True:
            self.Animatable.setFirstFrame()
            pass

        if self.Loop is not None:
            self.Animatable.setLoop(self.Loop)
            pass

        if self.SpeedFactor is not None:
            if self.DefaultSpeedFactor is None:
                self.DefaultSpeedFactor = self.Animatable.getSpeedFactor()
                pass

            TotalSpeedFactor = self.DefaultSpeedFactor * self.SpeedFactor

            self.Animatable.setSpeedFactor(TotalSpeedFactor)
            pass
        elif self.Time is not None:
            Duration = self.Animatable.getDuration()

            SpeedFactor = Duration / self.Time
            self.Animatable.setSpeedFactor(SpeedFactor)
            pass

        if self.Wait is False:
            self.id = self.Animatable.play()

            return True
            pass

        if self.Animatable.isActivate() is False:
            self.log("Animatable '%s' Entity is disable", self.Animatable.getName())

            return True
            pass

        def __onAnimatableEnd(id):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=False)
            # self.complete()
            pass

        def __onAnimatableStop(id):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=True)
            # self.skip()
            # self.complete()
            pass

        self.Animatable.setEventListener(onAnimatableEnd=__onAnimatableEnd)
        self.Animatable.setEventListener(onAnimatableStop=__onAnimatableStop)

        self.id = self.Animatable.play()

        return False
        pass

    def _onSkip(self):
        super(TaskAnimatablePlay, self)._onSkip()

        if self.Wait is False:
            return

        if self.Animatable is None:
            return

        id = self.Animatable.getPlayId()

        if self.id != id:
            return

        self.Animatable.stop()
        pass

    def _onFinally(self):
        super(TaskAnimatablePlay, self)._onFinally()

        if self.Wait is False:
            return
            pass

        self.Animatable.setEventListener(onAnimatableEnd=None)
        self.Animatable.setEventListener(onAnimatableStop=None)

        if self.SpeedFactor is not None:
            self.Animatable.setSpeedFactor(self.DefaultSpeedFactor)
            pass

        if self.LastFrame is True:
            self.Animatable.setLastFrame()
            pass

        if self.AutoEnable is True:
            self.Animatable.disable()
            pass

        if self.Destroy is True:
            Menge.destroyNode(self.Animatable)
            self.Animatable = None
            pass
        pass
    pass