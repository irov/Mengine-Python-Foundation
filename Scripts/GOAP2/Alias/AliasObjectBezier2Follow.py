from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.TaskAlias import TaskAlias

class AliasObjectBezier2Follow(MixinObject, TaskAlias):
    def _onParams(self, params):
        super(AliasObjectBezier2Follow, self)._onParams(params)

        self.Follow = params.get("Follow")
        self.Time = params.get("Time")
        self.id = None
        pass

    def _onInitialize(self):
        super(AliasObjectBezier2Follow, self)._onInitialize()

        if self.Time is None:
            self.initializeFailed("Time is None.")
            pass
        pass

    def _onGenerate(self, source):
        ObjectEntityNode = self.Object.getEntityNode()

        source.addTask("TaskNodeBezier2Follow", Node=ObjectEntityNode, Follow=self.Follow, Time=self.Time)
        pass

    pass