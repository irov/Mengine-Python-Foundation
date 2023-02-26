from Foundation.Task.MixinObjectTemplate import MixinPuff
from Foundation.Task.Task import Task

class TaskPuffShowElement(MixinPuff, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskPuffShowElement, self)._onParams(params)

        self.enable = params.get("Enable", True)
        self.elementName = params.get("ElementName", None)
        pass

    def _onInitialize(self):
        super(TaskPuffShowElement, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.Puff.hasElement(self.elementName) is False:
                self.initializeFailed("There is no '%s' in '%s'" % (self.elementName, self.PuffName))
                pass
            pass
        pass

    def _onRun(self):
        if self.enable is True:
            self.Puff.addVisibleElement(self.elementName)
        else:
            self.Puff.removeVisibleElement(self.elementName)
            pass

        return True
        pass
    pass