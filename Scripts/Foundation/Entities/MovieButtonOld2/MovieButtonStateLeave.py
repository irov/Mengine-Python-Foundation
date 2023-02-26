from Notification import Notification

from MovieButtonState import MovieButtonState

class MovieButtonStateLeave(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateLeave, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Idle"
        Notification.notify(Notificator.onButtonMouseLeave, self.buttonEntity.object)
        pass

    def _onMouseEnter(self):
        if self.stateClick is True:
            return
            pass
        self.stateEnter = True
        pass

    def _onMouseLeave(self):
        if self.stateClick is True:
            return
            pass
        self.stateEnter = None
        pass

    def _onMovieEnd(self):
        self.changeState()
        pass

    def _onKeyEvent(self):
        self.stateClick = True
        pass

    pass