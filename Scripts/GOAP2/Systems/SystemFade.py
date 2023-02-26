from GOAP2.System import System

class SystemFade(System):
    def __init__(self):
        super(SystemFade, self).__init__()
        self.fade_count = 0

    def _onRun(self):
        return True

    def getFadeCount(self):
        return self.fade_count

    def incFadeCount(self):
        self.fade_count += 1

    def decFadeCount(self):
        self.fade_count -= 1
        if self.fade_count < 0:
            self.clearFadeCount()

    def clearFadeCount(self):
        self.fade_count = 0