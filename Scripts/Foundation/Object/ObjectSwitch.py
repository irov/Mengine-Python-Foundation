from DemonObject import DemonObject

class ObjectSwitch(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addParam(Type, "Switch")
        Type.addParam(Type, "Switches")
        pass

    def _onParams(self, params):
        super(ObjectSwitch, self)._onParams(params)

        self.initParam("Switch", params, None)
        self.initParam("Switches", params, [])
        pass

    def _onLoader(self):
        super(ObjectSwitch, self)._onLoader()

        Switches = self.getObjects()

        for object in Switches:
            object.superParam("Enable", False)
            pass

        self.params["Switches"] = [switch.getName() for switch in Switches]
        pass

    def hasSwitch(self, name):
        return name in self.params["Switches"]
        pass

    def findSwitch(self, name):
        if self.hasSwitch(name) is False:
            return None
            pass

        Switch = self.getObject(name)

        return Switch
        pass
    pass