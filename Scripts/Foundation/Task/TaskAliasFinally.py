from Foundation.Task.TaskAlias import TaskAlias
from Foundation.Task.TaskForkFinally import TaskForkFinally
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskAliasFinally(TaskAlias):
    def _onRun(self):
        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        scope_finally = []
        finurce = TaskSource(scope_finally)

        skiped = self.isSkiped()
        source.setSkiped(skiped)
        finurce.setSkiped(skiped)

        self._onGenerate(source, finurce)

        finurce.end()

        if len(scope_finally) != 0:
            source.addTask(TaskForkFinally, Source=scope_finally)
            pass

        if self.base is None:
            return True
            pass

        nexts = base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskAliasFinally invalid generate scope")
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass

    def _onGenerate(self, source, finurce):
        pass
    pass
