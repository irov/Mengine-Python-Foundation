from Notification import Notification

Interaction = Mengine.importEntity("Interaction")

class Socket(Interaction):
    @staticmethod
    def declareORM(Type):
        Interaction.declareORM(Type)
        pass

    def _mouseClickBegin(self, x, y):
        Notification.notify(Notificator.onSocketClickBegin, self.object)
        pass

    def _mouseClick(self, x, y):
        Notification.notify(Notificator.onSocketClick, self.object)
        pass

    def _mouseClickUp(self, x, y):
        Notification.notify(Notificator.onSocketClickUp, self.object)
        pass

    def _mouseClickUpBegin(self, x, y):
        Notification.notify(Notificator.onSocketClickUpBegin, self.object)
        pass

    def _mouseClickEnd(self, x, y):
        Notification.notify(Notificator.onSocketClickEnd, self.object)
        pass

    def _mouseClickEndUp(self, x, y):
        Notification.notify(Notificator.onSocketClickEndUp, self.object)
        pass

    def _mouseEnter(self):
        Notification.notify(Notificator.onSocketMouseEnter, self.object)
        pass

    def _mouseLeave(self):
        Notification.notify(Notificator.onSocketMouseLeave, self.object)
        pass
    pass