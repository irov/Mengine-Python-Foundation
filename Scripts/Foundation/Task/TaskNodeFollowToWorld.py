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
        pass

    def _onInitialize(self):
        super(TaskNodeFollowToWorld, self)._onInitialize()

        pass

    def _onRun(self):
        def __onFollowTo(node, id, isEnd):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete()
            pass

        self.id = self.node.followToW(self.Target, self.Offset, self.Distance, self.MoveSpeed, self.MoveAcceleration, self.MoveLimit, __onFollowTo)

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