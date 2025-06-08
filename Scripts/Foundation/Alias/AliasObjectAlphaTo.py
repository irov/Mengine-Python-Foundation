from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.MixinTime import MixinTime
from Foundation.Task.TaskAlias import TaskAlias

class AliasObjectAlphaTo(MixinObject, MixinTime, TaskAlias):
    Skiped = True

    def _onParams(self, params):
        super(AliasObjectAlphaTo, self)._onParams(params)

        self.alpha_from = params.get("From", None)
        self.alpha_to = params.get("To")

        self.easing = params.get("Easing", None)
        pass

    def _onInitialize(self):
        super(AliasObjectAlphaTo, self)._onInitialize()
        pass

    def _onGenerate(self, source):
        if self.alpha_from is None:
            self.alpha_from = self.Object.getParam("Alpha")
        else:
            self.Object.setParam("Alpha", self.alpha_from)

        if self.time == 0.0:
            self.Object.setParam("Alpha", self.alpha_to)
            return

        if self.Object.isActive() is True:
            entity_node = self.Object.getEntityNode()
            if entity_node.isActivate() is True:
                source.addTask("TaskNodeAlphaTo", Node=entity_node, Time=self.time, From=self.alpha_from, To=self.alpha_to, Easing=self.easing)

        source.addTask("TaskObjectSetAlpha", Object=self.Object, Value=self.alpha_to)
        pass
    pass