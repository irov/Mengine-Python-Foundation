from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

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
        self.ValidationGroupEnable = params.get("ValidationGroupEnable", True)
        self.AutoEnable = params.get("AutoEnable", False)
        self.Docdeb = params.get("Docdeb", " Docdeb NOT YOUR OBJECT")
        pass

    def _onValidate(self):
        super(TaskObjectAnimatablePlay, self)._onValidate()

        Animatable = self.getAnimatable()

        if Animatable is None:
            self.validateFailed("Animatable is None")
            pass

        Enable = Animatable.getEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Animatable %s is Disable" % (Animatable.getName()))
            pass

        if self.ValidationGroupEnable is True:
            AnimatableGroup = Animatable.getGroup()

            if AnimatableGroup is not None:
                if AnimatableGroup.getEnable() is False:
                    self.validateFailed("Animatable %s Group %s is Disable" % (Animatable.getName(), AnimatableGroup.getName()))
                    pass
                pass
            pass
        pass

    def _onFastSkip(self):
        Animatable = self.getAnimatable()

        if self.Loop is not None:
            Animatable.setLoop(self.Loop)
            pass

        if self.Wait is True and self.Loop is None:
            Animatable.setPlay(False)

            if self.SpeedFactor is not None:
                Animatable.setSpeedFactor(self.DefaultSpeedFactor)
                pass

            Animatable.setLastFrame(self.LastFrame)
            pass

        return True
        pass

    def _onRun(self):
        Animatable = self.getAnimatable()

        if self.AutoEnable is True:
            Animatable.setEnable(True)
            pass

        if self.StartTiming is not None:
            Animatable.setStartTiming(self.StartTiming)
            pass

        if self.Loop is not None:
            Animatable.setLoop(self.Loop)
            pass

        if self.SpeedFactor is not None:
            if self.DefaultSpeedFactor is None:
                self.DefaultSpeedFactor = Animatable.getSpeedFactor()
                pass

            TotalSpeedFactor = self.DefaultSpeedFactor * self.SpeedFactor

            Animatable.setSpeedFactor(TotalSpeedFactor)
            pass
        elif self.Time is not None:
            Duration = Animatable.getDuration()

            SpeedFactor = Duration / self.Time
            Animatable.setSpeedFactor(SpeedFactor)
            pass

        if self.Wait is False:
            Animatable.setPlay(True)

            return True
            pass

        AnimatableEntity = Animatable.getEntity()

        if AnimatableEntity.isActivate() is False:
            self.log("Animatable '%s' Entity is disable", Animatable.getName())

            return True
            pass

        def __onAnimationEndFilter(animatable, isStop):
            if isStop is True:
                self.setEventSkip(True)
                pass

            if self.SpeedFactor is not None:
                animatable.setSpeedFactor(self.DefaultSpeedFactor)
                pass

            return True
            pass

        self.addEvent(Animatable.onAnimatableEnd, __onAnimationEndFilter)

        Animatable.setPlay(True)

        return False
        pass

    def getAnimatable(self):
        return None
        pass

    def onEndAnimatable(self):
        Animatable = self.getAnimatable()
        self._onEndAnimatable(Animatable)
        pass

    def _onEndAnimatable(self, Animatable):
        pass

    def _onEventComplete(self):
        self.onEndAnimatable()
        pass

    def _onFastSkip(self):
        return True
        pass

    def _onFinally(self):
        super(TaskObjectAnimatablePlay, self)._onFinally()

        Animatable = self.getAnimatable()

        if Animatable is None:
            self.log("Animatable is None")
            return
            pass

        if self.Wait is True and self.Loop is None:
            Animatable.setPlay(False)

            if self.SpeedFactor is not None:
                Animatable.setSpeedFactor(self.DefaultSpeedFactor)
                pass

            Animatable.setLastFrame(self.LastFrame)
            pass

        if self.AutoEnable is True:
            Animatable.setEnable(False)
            pass
        pass
    pass