from GOAP2.DefaultManager import DefaultManager
from GOAP2.DemonManager import DemonManager
from GOAP2.TaskManager import TaskManager
from Session import Session

class WalktrhoughSession(Session):

    def _onInitialize(self, accountID):
        super(WalktrhoughSession, self)._onInitialize(accountID)
        pass

    def _onFinalize(self):
        super(WalktrhoughSession, self)._onFinalize()
        pass

    def loadSystems(self):
        pass

    def saveSystems(self):
        pass

    def _onRun(self):
        StartSceneName = DefaultManager.getDefault("WalktrhoughStartScene", "Menu")

        hasSparks = DemonManager.hasDemon("Sparks")
        if hasSparks is True:
            Sparks = DemonManager.getDemon("Sparks")
            Sparks.setEnable(False)
            pass

        with TaskManager.createTaskChain() as tc:
            tc.addTask("AliasTransition", SceneName=StartSceneName)
            pass
        pass

    def _onStop(self):
        pass

    pass