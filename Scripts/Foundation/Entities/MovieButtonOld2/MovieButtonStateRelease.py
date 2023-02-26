from MovieButtonState import MovieButtonState

class MovieButtonStateRelease(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateRelease, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Idle"
        pass

    def _onMovieEnd(self):
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