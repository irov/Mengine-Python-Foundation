from Foundation.Task.Task import Task

class TaskVoicePlay(Task):
    Skiped = True

    def __init__(self):
        super(TaskVoicePlay, self).__init__()
        self.identity = None
        pass

    def _onParams(self, params):
        super(TaskVoicePlay, self)._onParams(params)

        self.VoiceID = params.get("VoiceID")
        self.Wait = params.get("Wait", True)
        self.Loop = params.get("Loop", False)
        pass

    def _onRun(self):
        if self.Wait is False:
            self.identity = Mengine.voicePlay(self.VoiceID, self.Loop, None)

            if self.identity is None:
                return True

            return True

        cbs = dict(onSoundPause=None, onSoundResume=None, onSoundStop=self._onVoiceStop, onSoundEnd=self._onVoiceEnd)

        self.identity = Mengine.voicePlay(self.VoiceID, self.Loop, cbs)

        if self.identity is None:
            return True

        return False

    def _onVoiceStop(self, identity):
        self.complete(isSkiped=True)
        pass

    def _onVoiceEnd(self, method, playId):
        self.complete(isSkiped=False)
        pass

    def _onSkip(self):
        if self.identity is None:
            return

        Mengine.voiceStop(self.identity)
        pass

    def _onFinally(self):
        self.identity = None
        pass
    pass