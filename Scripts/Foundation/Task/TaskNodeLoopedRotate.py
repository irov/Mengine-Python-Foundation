from Foundation.Task.MixinObserver import MixinObserver
from Foundation.TaskManager import TaskManager

from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeLoopedRotate(MixinNode, MixinTime, MixinObserver, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeLoopedRotate, self)._onParams(params)

        self.tc = None
        pass

    def _onInitialize(self):
        super(TaskNodeLoopedRotate, self)._onInitialize()

        # self.rotateTo *= 3.14159 / 180.0
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSpinnerStop, self._onSpinnerStop)

        self.tc = TaskManager.createTaskChain(Repeat=True)
        with self.tc as tc:
            tc.addTask('TaskNodeRotateTo', Node=self.node, To=-6.28, Time=self.time)
            tc.addTask('TaskNodeRotateTo', Node=self.node, To=0, Time=0.1)

        return False
        pass

    def _onSpinnerStop(self):
        return True

    def _onFinally(self):
        super(TaskNodeLoopedRotate, self)._onFinally()

        chain = self.tc
        self.tc = None
        if chain is not None:
            chain.cancel()
        pass
    pass