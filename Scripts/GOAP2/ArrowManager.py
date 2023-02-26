from GOAP2.Notificator import Notificator
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
    def getArrowType(name):
        Type, module = ArrowManager.s_arrowType.get(name)

        return Type

    @staticmethod
    def importArrow(module, name):
        Name = "%s" % name
        FromName = module
        ModuleName = "%s.%s.%s" % (FromName, Name, Name)
        Module = __import__(ModuleName, fromlist=[FromName])
        Type = getattr(Module, Name)

        if name in ArrowManager.s_arrowType:
            Type2, module2 = ArrowManager.s_arrowType[name]

            Trace.log("Manager", 0, "ArrowManager.importArrow scene %s module %s already exist (module '%s')" % (name, module, module2))

            return None

        ArrowManager.s_arrowType[name] = (Type, module)

        if Menge.addArrowPrototypeFinder(name, ArrowManager.getArrowType) is False:
            Trace.log("Manager", 0, "ArrowManager.importArrow invalid arrow %s module %s" % (name, module))

            return None

        return Type

    @staticmethod
    def importArrows(module, prototypes):
        for prototype in prototypes:
            ArrowManager.importArrow(module, prototype)

    @staticmethod
    def attachArrow(attach, movieAttach=True):
        if ArrowManager.s_attach is attach:
            if _DEVELOPMENT is True:
                Trace.log("Manager", 0, "ArrowManager.attachArrow: already has this item")
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

        ArrowManager.removeChildren()

        attach = ArrowManager.s_attach
        ArrowManager.s_attach = None

        Notification.notify(Notificator.onArrowDeattach, attach)

        return attach
        pass

    @staticmethod
    def removeChildren():
        # arrow = ArrowManager.getArrow()
        # arrow.removeAllChild()
        return

    @staticmethod
    def getArrow():
        arrow = Menge.getArrow()

        return arrow
        pass
    pass