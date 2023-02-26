from MovieButtonState import MovieButtonState

class MovieButtonStateIdle(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateIdle, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Enter"
        self.stateClick = False

        if self.isSocketMouseEnter() is True:
            self.stateEnter = True
            self.changeState()
            return False
            pass

        self.movie.setLoop(True)
        pass

    def _updateClickable(self):
        if self.isSocketMouseEnter() is True:
            self.changeState()
            pass
        pass

    def _onMouseEnter(self):
        if self.stateClick is True:
            return
            pass
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