from GOAP2.GameManager import GameManager
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskGameUnblock(MixinObserver, Task):
    Skiped = False

    def _onCheck(self):
        if GameManager.isBlockGame() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onGameBlock, self.__onGameBlockFilter)

        return False
        pass

    def __onGameBlockFilter(self, value):
        if GameManager.isBlockGame() is True:
            return False
            pass

        if value is True:
            return False
            pass

        return True
        pass
    pass