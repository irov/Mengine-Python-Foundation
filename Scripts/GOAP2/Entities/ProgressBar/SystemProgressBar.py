from GOAP2.System import System

from Notification import Notification

class SystemProgressBar(System):
    def _onParams(self, params):
        super(SystemProgressBar, self)._onParams(params)

        self.onProgressBarUpdate = None
        pass

    def _onRun(self):
        self.onProgressBarUpdate = Notification.addObserver(Notificator.onProgressBarUpdate, self.__updateProgressBar)
        return True
        pass

    def __updateProgressBar(self, barObject, value):
        barObject.setValue(value)
        return False
        pass

    def _onStop(self):
        Notification.removeObserver(self.onProgressBarUpdate)
        self.onProgressBarUpdate = None
        pass
    pass