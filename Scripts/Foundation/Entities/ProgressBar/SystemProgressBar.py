from Foundation.System import System

class SystemProgressBar(System):
    def _onParams(self, params):
        super(SystemProgressBar, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserver(Notificator.onProgressBarUpdate, self.__updateProgressBar)
        return True

    def __updateProgressBar(self, barObject, value):
        barObject.setValue(value)
        return False
    pass