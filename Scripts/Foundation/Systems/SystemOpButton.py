from Foundation.Providers.AdminPanelProvider import AdminPanelProvider
from Foundation.System import System
from Foundation.SystemManager import SystemManager


class SystemOpButton(System):
    """Connect running systems to the native SDK through optional methods."""

    def __init__(self):
        super(SystemOpButton, self).__init__()

        self.__stopped = False
        self.__ready = False
        pass

    @staticmethod
    def _onAvailable(params):
        if _DEVELOPMENT is False:
            return False

        return AdminPanelProvider.hasProvider()

    def _onRun(self):
        Mengine.waitSemaphore("OpButtonReady", self.__onReady)
        return True

    def _onStop(self):
        self.__stopped = True
        self.__setReady(False)
        pass

    def onSystemRun(self, system):
        if self.__ready is False:
            return

        SystemManager.callSystemMethod(system, "onOpButtonReady")
        pass

    def __onReady(self, successful):
        if self.__stopped is True:
            return

        self.__setReady(successful is True)
        pass

    def __setReady(self, ready):
        if self.__ready is ready:
            return

        self.__ready = ready
        if ready is True:
            SystemManager.broadcastSystemMethod("onOpButtonReady")
            pass
        else:
            SystemManager.broadcastSystemMethod("onOpButtonStop")
            pass
        pass
