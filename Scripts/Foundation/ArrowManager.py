from Foundation.Notificator import Notificator
from Notification import Notification

class ArrowManager(object):
    s_arrowType = {}

    s_arrow = None
    s_attach = None

    @staticmethod
    def onInitialize():
        pass

    @staticmethod
    def onFinalize():
        ArrowManager.s_arrow = None
        ArrowManager.s_attach = None

    @staticmethod
    def attachArrow(attach, movieAttach=True):
        if ArrowManager.s_attach is attach:
            if _DEVELOPMENT is True:
                Trace.log("Manager", 0, "ArrowManager.attachArrow: already has this item")
                pass
            return

        if ArrowManager.s_attach is not None:
            oldAttach = ArrowManager.s_attach
            ArrowManager.s_attach = None
            Notification.notify(Notificator.onArrowDeattach, oldAttach)

        ArrowManager.s_attach = attach

        Notification.notify(Notificator.onArrowAttach, attach)

    @staticmethod
    def getArrowAttach():
        return ArrowManager.s_attach

    @staticmethod
    def emptyArrowAttach():
        return ArrowManager.s_attach is None

    @staticmethod
    def removeArrowAttach():
        if ArrowManager.s_attach is None:
            Trace.log("ArrowManager", 0, "ArrowManager removeArrowAttach: You can't remove 'attach' - it's empty.")
            return

        attach = ArrowManager.s_attach
        ArrowManager.s_attach = None

        Notification.notify(Notificator.onArrowDeattach, attach)

        return attach
        pass
    pass