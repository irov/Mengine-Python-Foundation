from Task import Task

class TaskNodeAddChild(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeAddChild, self)._onParams(params)
        self.nodeParent = params.get("ParentNode")
        self.nodeChild = params.get("ChildNode")
        pass

    def _onInitialize(self):
        super(TaskNodeAddChild, self)._onInitialize()

        if _DEVELOPMENT is True:
            if Mengine.is_class(self.nodeParent) is False:
                self.initializeFailed("Parent Node is not class")
                pass

            if Mengine.is_class(self.nodeChild) is False:
                self.initializeFailed("Child Node is not class")
                pass

            if Mengine.is_wrap(self.nodeParent) is False:
                self.initializeFailed("Parent Node is not wrap")
                pass

            if Mengine.is_wrap(self.nodeChild) is False:
                self.initializeFailed("Child Node is not wrap")
                pass
            pass
        pass

    def _onRun(self):
        self.nodeParent.addChild(self.nodeChild)

        return True
        pass
    pass