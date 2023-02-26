from GOAP2.Task.MixinNode import MixinNode
from GOAP2.Task.TaskAlias import TaskAlias

class AliasNodeTranslateTo(MixinNode, TaskAlias):
    def _onParams(self, params):
        super(AliasNodeTranslateTo, self)._onParams(params)

        self.direction = params.get("Direction")
        self.length = params.get("Length", None)
        self.speed = params.get("Speed", None)
        self.time = params.get("Time", None)
        self.id = None
        pass

    def _onInitialize(self):
        super(AliasNodeTranslateTo, self)._onInitialize()

        if _DEVELOPMENT is True:
            if (self.time is None) and (self.speed is None):
                self.initializeFailed("AliasNodeTranslateTo time and speed is None!!!")
                return

            if self.speed is not None and self.time is not None and self.length != self.time * self.speed:
                self.initializeFailed("AliasNodeTranslateTo wrong params!!!")
                pass
            pass
        pass

    def _onGenerate(self, source):
        if self.time is None:
            self.time = self.length / self.speed
            pass

        if self.speed is None:
            time = self.time
            pass

        if self.length is None:
            self.length = self.speed * self.time
            pass

        positionTo = self.computePositionTo()

        source.addTask("TaskNodeMoveTo", Node=self.node, To=positionTo, Time=self.time)
        source.addTask("TaskNodeSetPosition", Node=self.node, Value=positionTo)
        pass

    def computePositionTo(self):
        positionFrom = self.node.getLocalPosition()
        dx = self.length * self.direction[0]
        dy = self.length * self.direction[1]
        positionTo = (positionFrom.x + dx, positionFrom.y + dy)
        return positionTo
        pass

    pass