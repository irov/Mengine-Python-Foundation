from GOAP2.Initializer import Initializer

class Session(Initializer):
    def _onInitialize(self, accountID):
        super(Session, self)._onInitialize(accountID)

        self.accountID = accountID
        pass

    def _onFinalize(self):
        super(Session, self)._onFinalize()
        pass

    def onRun(self):
        self._onRun()
        pass

    def _onRun(self):
        pass

    def onStop(self):
        self._onStop()
        pass

    def _onStop(self):
        pass
    pass