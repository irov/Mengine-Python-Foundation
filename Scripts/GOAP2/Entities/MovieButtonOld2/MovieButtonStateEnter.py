from Notification import Notification

from MovieButtonState import MovieButtonState

class MovieButtonStateEnter(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateEnter, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Over"
        Notification.notify(Notificator.onButtonMouseEnter, self.buttonEntity.object)
        return True
        pass

    def _onMovieEnd(self):
        self.changeState()
        pass

    def _onMouseEnter(self):
        if self.stateClick is True:
            return
            pass
        self.stateEnter = None
        pass

    def _onMouseLeave(self):
        if self.stateClick is True:
            return
            pass
        self.stateEnter = False
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