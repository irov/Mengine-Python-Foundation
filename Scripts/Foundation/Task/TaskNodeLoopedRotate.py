from Foundation.TaskManager import TaskManager

from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeLoopedRotate(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeLoopedRotate, self)._onParams(params)

        self.onSpinnerStop = None
        self.tc = None
        pass

    def _onInitialize(self):
        super(TaskNodeLoopedRotate, self)._onInitialize()

        # self.rotateTo *= 3.14159 / 180.0
        pass

    def _onRun(self):
        self.onSpinnerStop = Notification.addObserver(Notificator.onSpinnerStop, self.comp)

        self.tc = TaskManager.createTaskChain(Repeat=True)
        with self.tc as tc:
            tc.addTask('TaskNodeRotateTo', Node=self.node, To=-6.28, Time=self.time)
            tc.addTask('TaskNodeRotateTo', Node=self.node, To=0, Time=0.1)

        return False
        pass

    def comp(self):
        self.complete()
        self.tc.cancel()
        return True

    def _onFinalize(self):
        super(Task, self)._onFinalize()

        Notification.removeObserver(self.onSpinnerStop)

        if self.tc is not None:
            self.tc.cancel()
        self.base = None
        pass