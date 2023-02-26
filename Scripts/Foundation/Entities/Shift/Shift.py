import Trace
from Foundation.Entity.BaseEntity import BaseEntity

class Shift(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Shift", Update=Shift._updateShift)
        Type.addAction(Type, "Shifts")
        pass

    def __init__(self):
        super(Shift, self).__init__()

        self.currentShift = None

        self.shifts = []
        self.shiftCache = {}
        pass

    def getSprite(self):
        return self.currentShift
        pass

    def _onInitialize(self, obj):
        super(Shift, self)._onInitialize(obj)

        for ShiftData in self.Shifts:
            ShiftName = ShiftData['ShiftName']
            ResourceName = ShiftData['ResourceName']
            Position = ShiftData['Position']

            Resource = Mengine.getResourceReference(ResourceName)
            shift = Mengine.createSprite(ShiftName, Resource)
            shift.setLocalPosition(Position)
            shift.disable()

            self.addChild(shift)

            self.shifts.append(shift)
            self.shiftCache[ShiftName] = shift
            pass
        pass

    def _onFinalize(self):
        super(Shift, self)._onFinalize()

        for shift in self.shifts:
            Mengine.destroyNode(shift)
            pass

        self.shifts = []
        self.shiftCache = {}
        pass

    def _updateShift(self, value):
        if value is None:
            return
            pass

        if value not in self.shiftCache:
            Trace.log("Entity", 0, "Shift '%s' not found element '%s'" % (self.getName(), value))
            return
            pass

        for shift in self.shifts:
            shift.disable()
            shift.release()
            pass

        self.currentShift = self.shiftCache.get(value)
        self.currentShift.enable()
        pass
    pass