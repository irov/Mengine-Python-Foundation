from GOAP2.Entity.BaseEntity import BaseEntity

class Switch(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Switch", Update=Switch._updateSwitch)
        Type.addAction(Type, "Switches")
        pass

    def __init__(self):
        super(Switch, self).__init__()

        self.currentSwitch = None
        pass

    def _onPreparation(self):
        pass

    def _updateSwitch(self, value):
        Switches = self.object.getSwitches()

        for SwitchName in Switches:
            Switch = self.object.getObject(SwitchName)
            if Switch.getParam("Enable") is True:
                Switch.setEnable(False)
                pass
            pass

        if value is None:
            return

        if value not in Switches:
            Trace.log("Entity", 0, "Switch '%s' not found element '%s'" % (self.object.name, value))
            return

        self.currentSwitch = self.object.getObject(value)

        if self.currentSwitch.getParam("Enable") is False:
            self.currentSwitch.setEnable(True)
            pass
        pass
    pass