from Object import Object

class ObjectShift(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareParam("Shift")
        Type.declareConst("Shifts")
        pass

    def _onParams(self, params):
        super(ObjectShift, self)._onParams(params)

        self.initParam("Shift", params, None)
        self.initConst("Shifts", params)
        pass

    def hasShift(self, name):
        Shifts = self.getShifts()
        for shift in Shifts:
            if shift["ShiftName"] == name:
                return True
                pass
            pass

        return False
        pass

    def indexShift(self, name):
        Shifts = self.getShifts()
        for index, shift in enumerate(Shifts):
            if shift["ShiftName"] == name:
                return index
                pass
            pass

        return None
        pass

    def getNextShift(self):
        Shift = self.getShift()
        Shifts = self.getShifts()

        ShiftIndex = self.indexShift(Shift)

        ShiftsCount = len(Shifts)

        NextShiftIndex = (ShiftIndex + 1) % (ShiftsCount)

        NextShiftName = Shifts[NextShiftIndex]["ShiftName"]

        return NextShiftName
        pass
    pass