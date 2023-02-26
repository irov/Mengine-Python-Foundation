from Foundation.Task.Task import Task

class MixinNode(Task):
    def __init__(self):
        super(MixinNode, self).__init__()

        self.node = None
        pass

    def _onFinalize(self):
        super(MixinNode, self)._onFinalize()

        self.node = None
        pass

    def _onValidate(self):
        super(MixinNode, self)._onValidate()

        if self.node is None:
            self.validateFailed("node is None")
            pass

        if Mengine.is_class(self.node) is False:
            self.validateFailed("node is not pybind class")
            pass

        if Mengine.is_wrap(self.node) is False:
            self.validateFailed("node is unwrap")
            pass
        pass

    def setNode(self, node):
        self.node = node
        pass

    def getNode(self):
        return self.node
        pass
    pass