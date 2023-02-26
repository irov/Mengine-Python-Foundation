from MovieButtonState import MovieButtonState

class MovieButtonStatePush(MovieButtonState):
    def __init__(self):
        super(MovieButtonStatePush, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Idle"
        pass

    def _onMouseEnter(self):
        self.stateEnter = True
        pass

    def _onMouseLeave(self):
        self.stateEnter = None
        pass

    def _onMovieEnd(self):
        self.clickEnd()
        self.changeState()
        pass

    def _onMouseButtonEvent(self):
        self.stateClick = True
        self.changeState()
        pass

    def _onKeyEvent(self):
        self.stateClick = True
        self.changeState()
        pass

    pass