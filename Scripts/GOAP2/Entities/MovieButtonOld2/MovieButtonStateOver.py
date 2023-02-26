from MovieButtonState import MovieButtonState

class MovieButtonStateOver(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateOver, self).__init__()
        pass

    def _onMouseLeave(self):
        if self.stateClick is True:
            return
            pass
        self.stateEnter = False
        self.changeState()
        pass

    def _onMouseButtonEvent(self):
        if self.stateClick is True:
            return
            pass

        self.stateClick = True
        self.changeState()
        pass

    def _onKeyEvent(self):
        if self.stateClick is True:
            return
            pass
        self.stateClick = True
        self.changeState()
        pass

    pass