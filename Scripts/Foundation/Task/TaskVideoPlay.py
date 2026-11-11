from Foundation.Task.MixinObjectTemplate import MixinVideo
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskVideoPlay(MixinVideo, MixinObserver, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskVideoPlay, self)._onParams(params)
        self.wait = params.get("Wait", True)
        pass

    def _onRun(self):
        if self.wait is True:
            self.addObserver(Notificator.onVideoEnd, self._onVideoPlayFilter)

        self.Video.setParam("Play", True)

        if self.wait is True:
            return False
            pass

        return True
        pass

    def _onVideoPlayFilter(self, video):
        return self.Video is video
        pass

    def _onSkip(self):
        self.Video.setParam("Play", False)
        pass
    pass