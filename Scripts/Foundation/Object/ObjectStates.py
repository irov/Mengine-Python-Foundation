from Foundation.Object.DemonObject import DemonObject

class ObjectStates(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addConst(Type, "States")
        Type.addParam(Type, "CurrentState")
        pass

    def _onParams(self, params):
        super(ObjectStates, self)._onParams(params)

        self.initConst("States", params, [])
        self.initParam("CurrentState", params, None)
        pass

    def hasState(self, state):
        if state not in self.getParam("States"):
            return False
            pass

        return True
        pass

    def getState(self, state):
        if self.hasState(state) is False:
            Trace.log("Object", 0, "ObjectStates  getState unknown state %s" % (state))
            return None
            pass

        DemonName = "Demon_State_%s" % (state)
        DemonState = self.getObject(DemonName)

        return DemonState
        pass

    def getCurrentStateObject(self):
        CurrentState = self.getParam("CurrentState")
        if CurrentState is None:
            print("ObjectStates.getCurrentState %s not current state" % (self.getName()))
            return None
            pass

        State = self.getState(CurrentState)

        return State
        pass
    pass