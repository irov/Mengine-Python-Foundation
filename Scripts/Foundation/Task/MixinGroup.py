from Foundation.DemonManager import DemonManager
from Foundation.GroupManager import GroupManager
from Foundation.Initializer import Initializer
from Foundation.Params import Params

class MixinGroup(Params, Initializer):
    __metaclass__ = baseslots("Group", "GroupName", "DemonName")

    def __init__(self):
        super(MixinGroup, self).__init__()

        self.Group = None
        self.GroupName = None
        self.DemonName = None
        pass

    def _onParams(self, params):
        super(MixinGroup, self)._onParams(params)

        self.Group = params.get("Group", None)
        self.GroupName = params.get("GroupName", None)
        self.DemonName = params.get("DemonName", None)
        pass

    def _onInitialize(self):
        super(MixinGroup, self)._onInitialize()

        if self.DemonName is not None:
            self.Group = DemonManager.getDemon(self.DemonName)
            self.GroupName = self.Group.getName()
            pass
        elif self.Group is None and self.GroupName is not None:
            self.Group = GroupManager.getGroup(self.GroupName)

            if self.Group is None:
                self.initializeFailed("Group '%s' not found" % (self.GroupName))
                pass
            pass
        elif self.Group is not None and self.GroupName is None:
            self.GroupName = self.Group.getName()
            pass
        pass

    def _onFinalize(self):
        super(MixinGroup, self)._onFinalize()

        self.Group = None
        self.GroupName = None
        self.DemonName = None
        pass

    def setGroup(self, Group):
        self.Group = Group
        pass

    def getGroup(self):
        return self.Group

    def setGroupName(self, GroupName):
        self.GroupName = GroupName
        pass

    def getGroupName(self):
        return self.GroupName

    def setDemonName(self, DemonName):
        self.DemonName = DemonName
        pass

    def getDemonName(self):
        return self.DemonName
    pass