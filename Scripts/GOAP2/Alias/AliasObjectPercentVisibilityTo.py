from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.MixinTime import MixinTime
from GOAP2.Task.TaskAlias import TaskAlias

class AliasObjectPercentVisibilityTo(MixinObject, MixinTime, TaskAlias):
    Skiped = True

    def _onParams(self, params):
        super(AliasObjectPercentVisibilityTo, self)._onParams(params)

        self.percentFrom = params.get("From", None)
        self.percentTo = params.get("To")

        self.id = None
        pass

    def _onGenerate(self, source):
        if self.Object.isActive() is True:
            ObjectEntity = self.Object.getEntity()
            sprite = ObjectEntity.getSprite()

            source.addTask("TaskNodePercentVisibilityTo", Node=sprite, From=self.percentFrom, To=self.percentTo, Time=self.time)
            pass
        pass

    pass