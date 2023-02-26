from Foundation.DatabaseManager import DatabaseManager
from Foundation.GroupManager import GroupManager

class SnapManager(object):
    s_Snaps = {}  # group # item [][]

    class Snap(object):
        def __init__(self, Object, SnapDir):
            self.Object = Object
            self.SnapDir = SnapDir

            Position = Object.getPosition()
            self.Position = [Position[0], Position[1]]
            pass

        def apply(self):
            viewportCurent = Mengine.getGameViewport()

            ContentResolution = Mengine.getContentResolution()
            ContentResolutionWidth = ContentResolution.getWidth()
            ContentResolutionHeight = ContentResolution.getHeight()

            dif_End_x = ContentResolutionWidth - viewportCurent.end.x
            dif_Beg_x = 0 - viewportCurent.begin.x
            dif_End_y = ContentResolutionHeight - viewportCurent.end.y
            dif_Beg_y = 0 - viewportCurent.begin.y

            newPos = self.Position

            if self.SnapDir == "None":
                pass
            elif self.SnapDir == "Top":
                newPos = [self.Position[0], self.Position[1] - dif_Beg_y]
                pass
            elif self.SnapDir == "Down":
                newPos = [self.Position[0], self.Position[1] - dif_End_y]
                pass
            elif self.SnapDir == "Left":
                newPos = [self.Position[0] - dif_Beg_x, self.Position[1]]
                pass
            elif self.SnapDir == "Right":
                newPos = [self.Position[0] - dif_End_x, self.Position[1]]
                pass

            self.Object.setPosition(newPos)
            pass

        def reset(self):
            self.Object.setPosition(self.Position)
            self.Object = None
            pass
        pass

    @staticmethod
    def loadParams(module, param):
        if SnapManager.loadSnaps(module, param) is False:
            return False
            pass

        return True
        pass

    @staticmethod
    def addSnap(GroupName, ObjectName, SnapAlign):
        if SnapManager.hasSnap(GroupName, ObjectName) is True:
            Trace.log("Manager", 0, "SnapManager.loadSnaps snap with group %s and name %s already exist" % (GroupName, ObjectName))
            return False
            pass

        if GroupManager.hasObject(GroupName, ObjectName) is False:
            Trace.log("Manager", 0, "SnapManager.loadSnaps Group %s not have object %s" % (GroupName, ObjectName))
            return False
            pass

        Object = GroupManager.getObject(GroupName, ObjectName)

        Snap = SnapManager.Snap(Object, SnapAlign)

        if GroupName not in SnapManager.s_Snaps:
            SnapManager.s_Snaps[GroupName] = {}
            pass

        listGroups = SnapManager.s_Snaps[GroupName]

        listGroups[ObjectName] = Snap

        Snap.apply()

        return True
        pass

    @staticmethod
    def removeSnap(GroupName, ObjectName):
        if SnapManager.hasSnap(GroupName, ObjectName) is False:
            Trace.log("Manager", 0, "SnapManager.removeSnap snap with group %s and name %s not exist" % (GroupName, ObjectName))
            return False
            pass

        GroupSnaps = SnapManager.s_Snaps[GroupName]

        snap = GroupSnaps[ObjectName]
        snap.reset()

        del GroupSnaps[ObjectName]

        if len(GroupSnaps) == 0:
            del SnapManager.s_Snaps[GroupName]
            pass

        return True
        pass

    @staticmethod
    def loadSnaps(module, param):
        contentResolution = Mengine.getContentResolution()
        SnapManager.ContentResolution = (contentResolution.getWidth(), contentResolution.getHeight())

        records = DatabaseManager.getDatabaseRecords(module, param)

        if records is None:
            return False
            pass

        for record in records:
            GroupName = record.get("GroupName")
            ObjectName = record.get("ObjectName")

            SnapAlign = record.get("SnapAlign", "None")

            if SnapManager.addSnap(GroupName, ObjectName, SnapAlign) is False:
                return False
                pass
            pass

        return True
        pass

    @staticmethod
    def applySnaps(GroupName):
        Snaps = SnapManager.s_Snaps[GroupName]
        for key, value in Snaps.iteritems():
            value.apply()
            pass
        pass

    @staticmethod
    def hasSnapGroup(GroupName):
        return GroupName in SnapManager.s_Snaps
        pass

    @staticmethod
    def getGroupShaps(GroupName):
        return SnapManager.s_Snaps[GroupName]
        pass

    @staticmethod
    def hasSnap(GroupName, ObjectName):
        if SnapManager.hasSnapGroup(GroupName) is False:
            return False
            pass

        group = SnapManager.s_Snaps[GroupName]

        if ObjectName not in group:
            return False
            pass

        return True
        pass

    @staticmethod
    def getSnap(GroupName, ObjectName):
        if SnapManager.hasSnap(GroupName, ObjectName) is False:
            Trace.log("Manager", 0, "SnapManager.getSnap can't find object %s in group %s" % (ObjectName, GroupName))

            return None
            pass

        Snap = SnapManager.s_Snaps[GroupName][ObjectName]

        return Snap
        pass
    pass