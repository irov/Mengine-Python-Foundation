from Foundation.ArrowManager import ArrowManager
from Foundation.Task.Task import Task

class TaskMouseUse(Task):
    def __init__(self):
        super(TaskMouseUse, self).__init__()

        self.GlobalHandleAdapter = None
        pass

    def _onRun(self):
        self.GlobalHandleAdapter = Mengine.addMouseButtonHandler(self.__onGlobalHandleMouseButtonEvent)

        return False
        pass

    def _onFinally(self):
        super(TaskMouseUse, self)._onFinally()

        Mengine.removeMouseButtonHandler(self.GlobalHandleAdapter)
        self.GlobalHandleAdapter = None
        pass

    def __onGlobalHandleMouseButtonEvent(self, event):
        if event.button != 0:
            return
            pass

        if event.isDown is False:
            return
            pass

        if ArrowManager.emptyArrowAttach() is True:
            return
            pass

        self.complete()
        return
        pass
    pass