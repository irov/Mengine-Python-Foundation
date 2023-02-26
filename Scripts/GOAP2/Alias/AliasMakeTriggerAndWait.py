from GOAP2.Task.TaskAlias import TaskAlias

class AliasMakeTriggerAndWait(TaskAlias):
    def _onParams(self, params):
        super(AliasMakeTriggerAndWait, self)._onParams(params)
        self.Parent = params.get("Parent")
        self.AOI = params.get("AOI")
        self.Radius = params.get("Radius")
        self.IFF_Self = params.get("IFF_Self")
        self.IFF_Enemies = params.get("IFF_Enemies")
        self.Filter = params.get("Filter")
        self.Args = params.get("Args", ())
        self.Position = params.get("Position")
        pass

    def _onGenerate(self, source):
        Trigger = self.Parent.createChild("NodeAOITrigger")
        Trigger.setAOI(self.AOI)
        Trigger.setRadius(self.Radius)
        Trigger.setIFF(self.IFF_Self)

        if self.Position is not None:
            Trigger.setLocalPosition(self.Position)
            pass

        Trigger.enable()

        source.addTask("TaskTrigger", Trigger=Trigger, IFF=self.IFF_Enemies, Filter=self.Filter, Args=self.Args)

        source.addTask("TaskNodeDestroy", Node=Trigger)
        pass
    pass