from GOAP2.Task.Task import Task

class TaskVoicePlay(Task):
    Skiped = True

    def __init__(self):
        super(TaskVoicePlay, self).__init__()
        self.playId = None
        pass

    def _onParams(self, params):
        super(TaskVoicePlay, self)._onParams(params)

        self.VoiceID = params.get("VoiceID")
        self.Wait = params.get("Wait", True)
        self.Loop = params.get("Loop", False)
        pass

    def _onRun(self):
        if self.Wait is True:
            self.playId = Menge.voicePlay(self.VoiceID, self.Loop, self._onVoiceEnd)

            if self.playId == 0:
                return True
                pass

            return False
        else:
            self.playId = Menge.voicePlay(self.VoiceID, self.Loop, None)

            if self.playId == 0:
                return True
                pass

            return True
        pass

    def _onVoiceEnd(self, playId, isEnd):
        """
        Voice play callback
        :param playId: SoundIdentity
        :param isEnd: sound play state, 0 - stop, 1 - end
        :return: None
        """
        if playId is None:
            return

        if self.playId is None:
            return

        if self.playId.getId() != playId.getId():
            return

        self.playId = None

        self.complete()
        pass

    def _onSkip(self):
        if self.playId is not None:
            stopId = self.playId

            self.playId = None
            Menge.voiceStop(stopId)
            pass
        pass
    pass