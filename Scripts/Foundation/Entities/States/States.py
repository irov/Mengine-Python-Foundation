from Foundation.Entity.BaseEntity import BaseEntity

class States(BaseEntity):

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction("States")
        Type.addAction("CurrentState", Update=States._updateCurrentState)
        pass

    def visitStates(self, visitor):
        for stateName in self.States:
            obj = self.object.getState(stateName)
            visitor(obj, stateName)
            pass
        pass

    def _updateCurrentState(self, currentState):
        if self.object.hasState(currentState) is False:
            Trace.log("Entity", 0, "States _updateCurrentState unknown state %s" % (currentState,))
            return
            pass

        for stateName in self.States:
            stateObject = self.object.getState(stateName)
            stateObject.setEnable(False)
            pass

        currentStateObject = self.object.getState(currentState)
        currentStateObject.setEnable(True)
        pass
    pass