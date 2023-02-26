class Default(object):
    def __init__(self):
        Mengine.Arrow.__init__(self)

        self.node = None

        self.itemNode = None
        self.cursorNode = None

        pass

    def setName(self, name):
        self.node.setName(name)
        pass

    def getName(self):
        return self.node.getName()
        pass

    def addChild(self, node):
        self.node.addChild(node)
        pass

    def createChild(self, type):
        return self.node.createChild(type)
        pass

    def addChildFront(self, node):
        return self.node.addChildFront(node)
        pass

    def enable(self):
        self.node.enable()
        pass

    def disable(self):
        self.node.disable()
        pass

    def onCreate(self, node):
        self.node = node

        self.itemNode = self.createChild("Interender")
        self.itemNode.enable()

        self.cursorNode = self.createChild("Interender")

        self.cursorNode.enable()
        pass

    def onPreparation(self):
        Notification.notify(Notificator.onArrowPreparation)

    def onActivate(self):
        Notification.notify(Notificator.onArrowActivate)

    def onDeactivate(self):
        Notification.notify(Notificator.onArrowDeactivate)

    def getItemNode(self):
        return self.itemNode
        pass

    def getCursorNode(self):
        return self.cursorNode
        pass

    def onCursorMode(self, mode):
        if mode is True:
            self.cursorNode.disable()
        else:
            self.cursorNode.enable()
            pass
        pass

    def onDestroy(self):
        if self.cursorNode is not None:
            Mengine.destroyNode(self.cursorNode)
            self.cursorNode = None
            pass

        if self.itemNode is not None:
            Mengine.destroyNode(self.itemNode)
            self.itemNode = None
            pass

        self.node = None
        pass
    pass