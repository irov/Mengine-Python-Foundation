from Notification import Notification

from MovieButtonState import MovieButtonState

class MovieButtonStateClick(MovieButtonState):
    def __init__(self):
        super(MovieButtonStateClick, self).__init__()
        pass

    def _activate(self):
        self.DefaultNextState = "Idle"
        Notification.notify(Notificator.onButtonClickBegin, self.buttonEntity.object)
        Notification.notify(Notificator.onButtonClick, self.buttonEntity.object)
        pass

    def _onMouseEnter(self):
        self.stateEnter = True
        pass

    def _onMouseLeave(self):
        self.stateEnter = None
        pass

    def _onMovieEnd(self):
        self.changeState()
        pass

    pass