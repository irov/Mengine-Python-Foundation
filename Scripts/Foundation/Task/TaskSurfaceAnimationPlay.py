from Foundation.Task.Task import Task

class TaskSurfaceAnimationPlay(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSurfaceAnimationPlay, self)._onParams(params)
        self.Surface = params.get("Surface")
        self.Wait = params.get("Wait", True)

        self.id = None
        pass

    def _onValidate(self):
        super(TaskSurfaceAnimationPlay, self)._onValidate()
        pass

    def _onRun(self):
        Animation = self.Surface.getAnimation()

        if self.Wait is False:
            self.id = Animation.play()

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

        self.Surface.setEventListener(onAnimatableEnd=__onAnimatableEnd)
        self.Surface.setEventListener(onAnimatableStop=__onAnimatableStop)

        self.id = Animation.play()

        return False
        pass

    def _onSkip(self):
        super(TaskSurfaceAnimationPlay, self)._onSkip()

        if self.Wait is False:
            return

        Animation = self.Surface.getAnimation()

        id = Animation.getPlayId()

        if self.id != id:
            return

        Animation.stop()
        pass

    def _onFinally(self):
        super(TaskSurfaceAnimationPlay, self)._onFinally()

        if self.Wait is False:
            return
            pass

        self.Surface.setEventListener(onAnimatableEnd=None)
        self.Surface.setEventListener(onAnimatableStop=None)
        pass
    pass