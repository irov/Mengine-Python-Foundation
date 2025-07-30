from Foundation.Task.Task import Task

class TaskSoundEffect(Task):
    Skiped = True

    def __init__(self):
        super(TaskSoundEffect, self).__init__()
        self.playId = None

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
        if self.Wait is True:
            self.playId = Mengine.soundPlay(self.SoundName, False, self._onSoundEnd)

            if self.playId is None:
                return True

            return False
        else:
            self.playId = Mengine.soundPlay(self.SoundName, False, None)

            if self.playId is None:
                return True

            return True
        pass

    def _onSoundEnd(self, method, playId):
        if self.playId.getId() != playId.getId():
            return

        self.playId = None

        self.complete()
        pass

    def _onSkip(self):
        if self.playId is None:
            return

        if self.playId is not None:
            stopId = self.playId
            self.playId = None

            Mengine.soundStop(stopId)
            pass
        pass
    pass