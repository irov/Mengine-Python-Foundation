from GOAP2.Task.MixinGroup import MixinGroup
from GOAP2.Task.Task import Task
from GOAP2.Task.TaskGenerator import TaskGenerator
from GOAP2.Task.TaskGenerator import TaskSource

class TaskAlias(MixinGroup, Task):
    Skiped = True

    def _onRun(self):
        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        self._onGenerate(source)

        if self.base is None:
            return True
            pass

        nexts = base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskAlias invalid generate scope")
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass

    def _onGenerate(self, source):
        pass
    pass