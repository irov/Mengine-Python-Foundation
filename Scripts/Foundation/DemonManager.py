from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.GroupManager import GroupManager

class DemonManager(Manager):
    s_demons = {}

    @staticmethod
    def _onFinalize():
        DemonManager.s_demons = {}

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            DemonName = record.get("DemonName")
            GroupName = record.get("GroupName")
            ObjectName = record.get("ObjectName")

            if DemonManager.addDemon(DemonName, GroupName, ObjectName) is False:
                Trace.log("Manager", 0, "DemonManager.loadParams not found demon %s:%s name %s" % (GroupName, ObjectName, DemonName))

                return False

        return True

    @staticmethod
    def addDemon(DemonName, GroupName, ObjectName):
        group = GroupManager.getGroup(GroupName)
        if isinstance(group, GroupManager.EmptyGroup):
            return True

        if GroupManager.hasObject(GroupName, ObjectName) is False:
            Trace.log("Manager", 0, "DemonManager.addDemon not found demon %s:%s name %s" % (GroupName, ObjectName, DemonName))

            return False

        Demon = GroupManager.getObject(GroupName, ObjectName)

        DemonManager.s_demons[DemonName] = Demon
        return True

    @staticmethod
    def hasDemon(name):
        if name not in DemonManager.s_demons:
            return False

        return True

    @staticmethod
    def getDemon(name):
        if DemonManager.hasDemon(name) is False:
            Trace.log("Manager", 0, "DemonManager.getDemon: not found demon '%s'" % name)
            return None

        Demon = DemonManager.s_demons[name]

        return Demon

    @staticmethod
    def hasObject(demon_name, object_name):
        if DemonManager.hasDemon(demon_name) is False:
            return False

        Demon = DemonManager.s_demons[demon_name]

        if Demon.hasObject(object_name) is False:
            return False

        return True

    @staticmethod
    def hasPrototype(demon_name, prototype_name):
        if DemonManager.hasDemon(demon_name) is False:
            return False

        demon = DemonManager.getDemon(demon_name)

        if demon.hasPrototype(prototype_name) is False:
            return False

        return True

    @staticmethod
    def getObject(demon_name, object_name):
        if DemonManager.hasObject(demon_name, object_name) is False:
            Trace.log("Manager", 0, "DemonManager.getObject: not found demon '%s' or object '%s' inside" % (demon_name, object_name))
            return None

        # we know, that demon and object exist
        Demon = DemonManager.s_demons[demon_name]
        obj = Demon.getObject(object_name)

        return obj
