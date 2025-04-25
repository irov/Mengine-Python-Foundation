from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator

class TaskIf(MixinGroup, Task):
    __metaclass__ = finalslots("Fn", "Args", "Source_True", "Source_False")

    Skiped = True

    def _onParams(self, params):
        super(TaskIf, self)._onParams(params)

        self.Fn = params.get("Fn")
        self.Args = params.get("Args")
        self.Source_True = params.get("Source_True", [])
        self.Source_False = params.get("Source_False", [])
        pass

    def _onRun(self):
        result = self.Fn(*self.Args)

        if isinstance(result, bool) is False:
            self.invalidTask("TaskIf invalid result fn '%s' args '%s' must be [True|False] but is '%s'" % (self.Fn, self.Args, result))
            pass

        Source = self.Source_True if result is True else self.Source_False

        base = self.base
        chain = base.chain

        nexts = base.popNexts()

        tg = TaskGenerator(chain, self.Group, Source, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskIf invalid generate scope")
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass
    pass