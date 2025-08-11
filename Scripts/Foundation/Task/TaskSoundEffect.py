from Foundation.Task.Task import Task

class TaskSoundEffect(Task):
    Skiped = True

    def __init__(self):
        super(TaskSoundEffect, self).__init__()
        self.identity = None

    def _onParams(self, params):
        super(TaskSoundEffect, self)._onParams(params)

        self.SoundName = params.get("SoundName")
        self.Wait = params.get("Wait", True)
        self.Important = params.get("Important", True)
        pass

    def _onInitialize(self):
        super(TaskSoundEffect, self)._onInitialize()

        if self.Important is False:
            return

        if _DEVELOPMENT is True:
            if Mengine.hasSound(self.SoundName) is False:
                self.initializeFailed("TaskSoundEffect invalid sound %s" % (self.SoundName))
                pass
        pass

    def _onCheck(self):
        if self.Important is False:
            return False

        return True

    def _onRun(self):
        if self.Wait is False:
            self.identity = Mengine.soundPlay(self.SoundName, False, None)

            if self.identity is None:
                return True

            return True

        cbs = dict(onSoundPause=None, onSoundResume=None, onSoundStop=self._onSoundStop, onSoundEnd=self._onSoundEnd)

        self.identity = Mengine.soundPlay(self.SoundName, False, cbs)

        if self.identity is None:
            return True

        return False

    def _onSoundStop(self, identity):
        self.complete(isSkiped=True)
        pass

    def _onSoundEnd(self, identity):
        self.complete(isSkiped=False)
        pass

    def _onSkip(self):
        if self.identity is None:
            return

        Mengine.soundStop(self.identity)
        pass

    def _onFinally(self):
        self.identity = None
        pass
    pass