class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.currentState = None
        self.nextState = None
        pass

    def addState(self, name, state):
        self.states[name] = state
        pass

    def setState(self, name):
        self.nextState = name
        pass

    def updateState(self):
        while self.nextState is not None:
            if self.currentState is not None:
                currentState = self.currentState
                self.currentState = None

                currentState.onDiactivate()
                pass

            if self.nextState is not None:
                self.currentState = self.nextState
                self.nextState = None
                self.currentState.onActivate()
                pass
            pass
        pass
    pass