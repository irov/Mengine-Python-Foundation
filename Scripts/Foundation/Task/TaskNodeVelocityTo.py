from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeVelocityTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeVelocityTo, self)._onParams(params)

        self.velocity = params.get("Velocity")

        self.id = None
        pass

    def _onInitialize(self):
        super(TaskNodeVelocityTo, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.velocity is None:
                self.initializeFailed("velocity not initialized")
                pass
            pass
        pass

    def _onRun(self):
        def __onVelocityTo(node, id, isEnd):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.id = self.node.velocityTo2(self.velocity, self.time, __onVelocityTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = None

        self.node.moveStop()
        pass
    pass