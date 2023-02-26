from Foundation.Task.Task import Task

class TaskSoundEffect(Task):
    Skiped = True

    def __init__(self):
        super(TaskSoundEffect, self).__init__()
        self.playId = None
        pass

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
            pass

        if _DEVELOPMENT is True:
            if Menge.hasSound(self.SoundName) is False:
                self.initializeFailed("TaskSoundEffect invalid sound %s" % (self.SoundName))
                pass
            pass
        pass

    def _onCheck(self):
        if self.Important is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        if self.Wait is True:
            self.playId = Menge.soundPlay(self.SoundName, False, self._onSoundEnd)

            if self.playId is None:
                return True
                pass

            return False
        else:
            self.playId = Menge.soundPlay(self.SoundName, False, None)

            if self.playId is None:
                return True
                pass

            return True
            pass
        pass

    def _onSoundEnd(self, playId, callback=None):
        if callback == 0:
            return
        if self.playId.getId() != playId.getId():
            return
            pass

        self.playId = None

        self.complete()
        pass

    def _onSkip(self):
        if self.playId is None:
            return
            pass
        stopId = self.playId
        self.playId = None

        Menge.soundStop(stopId)
        pass
    pass