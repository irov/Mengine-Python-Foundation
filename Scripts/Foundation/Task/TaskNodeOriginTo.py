from MixinNode import MixinNode
from Task import Task

class TaskNodeOriginTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeOriginTo, self)._onParams(params)

        self.time = params.get("Time", None)
        self.origin = params.get("Origin")
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    '''
    def _onCheckParams(self):
        if self.Follow is None:
            self.paramsFailed("Follow is None.")
            pass

        if self.Time is None and self.Speed is None:
            self.paramsFailed("Time and Speed is None.")
            pass
        pass
    '''

    '''
    def _onInitialize(self):
        super(TaskNodeOriginTo, self)._onInitialize()

        if self.time is None:
            positionFrom = self.node.getScreenPosition()
            positionTo = self.Follow.getScreenPosition()
            length = Mengine.length_v2_v2(positionFrom, positionTo)
            self.Time = length / self.Speed
            pass
        pass
    '''

    def _onRun(self):
        self.id = self.node.originTo(self.time, self.origin, self.easing, self._onOriginTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        return

    def _onOriginTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass