from GOAP2.Task.MixinObjectTemplate import MixinVideo
from GOAP2.Task.Task import Task
from GOAP2.TaskManager import TaskManager

class TaskVideoPlay(MixinVideo, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskVideoPlay, self)._onParams(params)
        self.wait = params.get("Wait", True)
        pass

    def _onRun(self):
        self.Video.setParam("Play", True)

        if self.wait is True:
            with TaskManager.createTaskChain(Cb=self._onVideoPlayWait) as tc:
                tc.addTask("TaskListener", ID=Notificator.onVideoEnd, Filter=self._onVideoPlayFilter)
                pass

            return False
            pass

        return True
        pass

    def _onVideoPlayWait(self, isSkip):
        self.complete()
        pass

    def _onVideoPlayFilter(self, video):
        return self.Video is video
        pass

    def _onSkip(self):
        self.Video.setParam("Play", False)
        pass
    pass