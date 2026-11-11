from Foundation.Task.Task import Task
from Foundation.TaskManager import TaskManager


class TaskScopeChain(Task):
    __metaclass__ = baseslots("_scope_chain")

    def __init__(self):
        super(TaskScopeChain, self).__init__()

        self._scope_chain = None

    def _onRun(self):
        self._scope_chain = TaskManager.createTaskChain(Cb=self.__onScopeComplete)

        with self._scope_chain as source:
            self._onScopeRun(source)

        return False

    def _onScopeRun(self, source):
        pass

    def __onScopeComplete(self, isSkip):
        self._scope_chain = None
        self._onScopeComplete(isSkip)
        self.complete()

    def _onScopeComplete(self, isSkip):
        pass

    def _onFinally(self):
        super(TaskScopeChain, self)._onFinally()

        chain = self._scope_chain
        self._scope_chain = None
        if chain is not None:
            chain.cancel()
