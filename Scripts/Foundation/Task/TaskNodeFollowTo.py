from MixinNode import MixinNode
from Task import Task

class TaskNodeFollowTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeFollowTo, self)._onParams(params)

        self.Target = params.get("Target")
        self.Offset = params.get("Offset", (0.0, 0.0, 0.0))
        self.Distance = params.get("Distance", 0.0)
        self.MoveSpeed = params.get("MoveSpeed")
        self.MoveAcceleration = params.get("MoveAcceleration")
        self.MoveLimit = params.get("MoveLimit")
        self.Rotation = params.get("Rotation", False)
        self.RotationSpeed = params.get("RotationSpeed", 0.0)
        self.RotationAcceleration = params.get("RotationAcceleration", 0.0)
        self.RotationLimit = params.get("RotationLimit", 0.0)
        self.easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onInitialize(self):
        super(TaskNodeFollowTo, self)._onInitialize()
        pass

    def _onRun(self):
        def __onFollowTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.followTo(self.Target, self.Offset, self.Distance, self.MoveSpeed, self.MoveAcceleration, self.MoveLimit, self.Rotation, self.RotationSpeed, self.RotationAcceleration, self.RotationLimit, self.easing, __onFollowTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.affector = None
        self.node.moveStop()
        pass
    pass