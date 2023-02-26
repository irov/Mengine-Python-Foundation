from Notification import Notification

Interaction = Menge.importEntity("Interaction")

class Socket(Interaction):
    @staticmethod
    def declareORM(Type):
        Interaction.declareORM(Type)
        pass

    def _mouseClickBegin(self):
        Notification.notify(Notificator.onSocketClickBegin, self.object)
        pass

    def _mouseClick(self):
        Notification.notify(Notificator.onSocketClick, self.object)
        pass

    def _mouseClickUp(self):
        Notification.notify(Notificator.onSocketClickUp, self.object)
        pass

    def _mouseClickUpBegin(self):
        Notification.notify(Notificator.onSocketClickUpBegin, self.object)
        pass

    def _mouseClickEnd(self):
        Notification.notify(Notificator.onSocketClickEnd, self.object)
        pass

    def _mouseClickEndUp(self):
        Notification.notify(Notificator.onSocketClickEndUp, self.object)
        pass

    def _mouseEnter(self):
        Notification.notify(Notificator.onSocketMouseEnter, self.object)
        pass

    def _mouseLeave(self):
        Notification.notify(Notificator.onSocketMouseLeave, self.object)
        pass
    pass