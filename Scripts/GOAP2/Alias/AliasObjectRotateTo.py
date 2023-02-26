from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.MixinTime import MixinTime
from GOAP2.Task.TaskAlias import TaskAlias

class AliasObjectRotateTo(MixinObject, MixinTime, TaskAlias):
    def _onParams(self, params):
        super(AliasObjectRotateTo, self)._onParams(params)

        self.rotationTo = params.get("To")

    def _onInitialize(self):
        super(AliasObjectRotateTo, self)._onInitialize()

    def _onGenerate(self, source):
        if self.Object.isActive() is True:
            object_entity = self.Object.getEntityNode()

            source.addTask("TaskNodeRotateTo", Node=object_entity, To=self.rotationTo, Time=self.time)