from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.MixinTime import MixinTime
from GOAP2.Task.TaskAlias import TaskAlias

class AliasObjectScaleTo(MixinObject, MixinTime, TaskAlias):
    def _onParams(self, params):
        super(AliasObjectScaleTo, self)._onParams(params)

        self.scaleFrom = params.get("From", None)
        self.scaleTo = params.get("To")

        pass

    def _onInitialize(self):
        super(AliasObjectScaleTo, self)._onInitialize()
        pass

    def _onGenerate(self, source):
        if self.scaleFrom is None:
            self.scaleFrom = self.Object.getParam("Scale")
        else:
            self.Object.setParam("Scale", self.scaleFrom)
            pass

        if self.Object.isActive() is True:
            # objectEntity = self.Object.getEntity()
            # source.addTask("TaskNodeScaleTo", Node = objectEntity, From = self.scaleFrom, To = self.scaleTo, Time = self.time)

            entityNode = self.Object.getEntityNode()
            source.addTask("TaskNodeScaleTo", Node=entityNode, From=self.scaleFrom, To=self.scaleTo, Time=self.time)
            pass

        source.addTask("TaskObjectSetScale", Object=self.Object, Value=self.scaleTo)
        pass
    pass