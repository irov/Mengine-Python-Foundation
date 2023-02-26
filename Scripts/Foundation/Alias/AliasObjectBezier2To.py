from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.TaskAlias import TaskAlias

class AliasObjectBezier2To(MixinObject, TaskAlias):
    def _onParams(self, params):
        super(AliasObjectBezier2To, self)._onParams(params)

        self.P1 = params.get("Point1")
        self.positionTo = params.get("To")
        self.speed = params.get("Speed", None)
        self.time = params.get("Time", None)
        self.id = None
        pass

    def _onInitialize(self):
        super(AliasObjectBezier2To, self)._onInitialize()

        if self.speed is None and self.time is None:
            self.initializeFailed("Speed and Time is None.")
            pass

        pass

    def _onGenerate(self, source):
        positionFrom = self.Object.getPosition()

        if self.time is None:
            length = Menge.length_v2_v2(positionFrom, self.positionTo)
            self.time = length / self.speed
            pass

        if self.Object.isActive() is True:
            # ObjectEntity = self.Object.getEntity()
            ObjectEntityNode = self.Object.getEntityNode()

            source.addTask("TaskNodeBezier2To", Node=ObjectEntityNode, Point1=self.P1, To=self.positionTo, Time=self.time)
            pass

        source.addTask("TaskObjectSetPosition", Object=self.Object, Value=self.positionTo)
        pass

    pass