from MixinNode import MixinNode
from Task import Task

class TaskNodeFollowToWorld(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeFollowToWorld, self)._onParams(params)

        self.Target = params.get("Target")
        self.Offset = params.get("Offset", (0.0, 0.0, 0.0))
        self.Distance = params.get("Distance", 0.0)
        self.MoveSpeed = params.get("MoveSpeed")
        self.MoveAcceleration = params.get("MoveAcceleration")
        self.MoveLimit = params.get("MoveLimit")

        self.affector = None
        pass

    def _onInitialize(self):
        super(TaskNodeFollowToWorld, self)._onInitialize()
        pass

    def _onRun(self):
        def __onFollowTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.followToW(self.Target, self.Offset, self.Distance, self.MoveSpeed, self.MoveAcceleration, self.MoveLimit, __onFollowTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False
        pass

    def _onSkip(self):
        self.affector = None
        self.node.moveStop()
        pass
    pass