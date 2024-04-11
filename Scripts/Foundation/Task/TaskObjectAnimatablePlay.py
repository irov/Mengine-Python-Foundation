from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.Task import Task


class TaskObjectAnimatablePlay(MixinEvent, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectAnimatablePlay, self)._onParams(params)
        self.Loop = params.get("Loop", None)
        self.Wait = params.get("Wait", True)
        self.StartTiming = params.get("StartTiming", None)
        self.SpeedFactor = params.get("SpeedFactor", None)
        self.Time = params.get("Time", None)
        self.DefaultSpeedFactor = params.get("DefaultSpeedFactor", None)
        self.LastFrame = params.get("LastFrame", True)
        self.ValidationParentEnable = params.get("ValidationParentEnable", True)
        self.AutoEnable = params.get("AutoEnable", False)
        self.Docdeb = params.get("Docdeb", " Docdeb NOT YOUR OBJECT")

    def _onValidate(self):
        super(TaskObjectAnimatablePlay, self)._onValidate()

        Animatable = self.getAnimatable()

        if Animatable is None:
            self.validateFailed("Animatable is None")
            return

        Enable = Animatable.getEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Animatable '%s' is Disable" % (Animatable.getName()))

        if self.ValidationParentEnable is True:
            AnimatableParent = Animatable.getParent()

            if AnimatableParent is not None and AnimatableParent.getEnable() is False:
                self.validateFailed("Animatable '%s' error: Parent '%s' is Disable" % (
                    Animatable.getName(), AnimatableParent.getName()))

    def _onFastSkip(self):
        Animatable = self.getAnimatable()

        if self.Loop is not None:
            Animatable.setLoop(self.Loop)

        if self.Wait is True and self.Loop is None:
            Animatable.setPlay(False)

            if self.SpeedFactor is not None:
                Animatable.setSpeedFactor(self.DefaultSpeedFactor)

            Animatable.setLastFrame(self.LastFrame)

        return True

    def _onRun(self):
        Animatable = self.getAnimatable()

        if self.AutoEnable is True:
            Animatable.setEnable(True)

        if self.StartTiming is not None:
            Animatable.setStartTiming(self.StartTiming)

        if self.Loop is not None:
            Animatable.setLoop(self.Loop)

        if self.SpeedFactor is not None:
            if self.DefaultSpeedFactor is None:
                self.DefaultSpeedFactor = Animatable.getSpeedFactor()

            TotalSpeedFactor = self.DefaultSpeedFactor * self.SpeedFactor

            Animatable.setSpeedFactor(TotalSpeedFactor)
        elif self.Time is not None:
            Duration = Animatable.getDuration()

            SpeedFactor = Duration / self.Time
            Animatable.setSpeedFactor(SpeedFactor)

        if self.Wait is False:
            Animatable.setPlay(True)

            return True

        AnimatableEntity = Animatable.getEntity()

        if AnimatableEntity.isActivate() is False:
            self.log("Animatable '%s' Entity is disable", Animatable.getName())

            return True

        def __onAnimationEndFilter(animatable, isStop):
            if isStop is True:
                self.setEventSkip(True)

            if self.SpeedFactor is not None:
                animatable.setSpeedFactor(self.DefaultSpeedFactor)

            return True

        self.addEvent(Animatable.onAnimatableEnd, __onAnimationEndFilter)

        Animatable.setPlay(True)

        return False

    def getAnimatable(self):
        raise NotImplementedError

    def onEndAnimatable(self):
        Animatable = self.getAnimatable()
        self._onEndAnimatable(Animatable)

    def _onEndAnimatable(self, Animatable):
        pass

    def _onEventComplete(self):
        self.onEndAnimatable()

    def _onFinally(self):
        super(TaskObjectAnimatablePlay, self)._onFinally()

        Animatable = self.getAnimatable()

        if Animatable is None:
            self.log("Animatable is None")
            return

        if self.Wait is True and self.Loop is None:
            Animatable.setPlay(False)

            if self.SpeedFactor is not None:
                Animatable.setSpeedFactor(self.DefaultSpeedFactor)

            Animatable.setLastFrame(self.LastFrame)

        if self.AutoEnable is True:
            Animatable.setEnable(False)
