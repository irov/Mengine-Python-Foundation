from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.MixinTime import MixinTime
from Foundation.Task.TaskAlias import TaskAlias

class AliasObjectMoveTo(MixinTime, MixinObject, TaskAlias):
    Skiped = True
    MixinTime_Validate_TimeZero = False

    def _onParams(self, params):
        super(AliasObjectMoveTo, self)._onParams(params)

        self.positionTo = params.get("To", None)
        self.speed = params.get("Speed", None)
        self.point = params.get("Point", None)

    def _onInitialize(self):
        super(AliasObjectMoveTo, self)._onInitialize()
        position_from = self.Object.getParam("Position")
        if self.speed is not None:
            length = Menge.length_v2_v2(position_from, self.positionTo)
            self.time = length / self.speed

        if self.point is not None:
            point_entity = self.point.getEntity()
            self.positionTo = point_entity.getLocalPosition()

        if self.positionTo is None:
            self.initializeFailed("PositionTo not initialized")

    def _onGenerate(self, source):
        if self.Object.isActive() is True:
            object_entity = self.Object.getEntityNode()
            source.addTask("TaskNodeMoveTo", Node=object_entity, To=self.positionTo, Time=self.time)

        source.addTask("TaskObjectSetPosition", Object=self.Object, Value=self.positionTo)