# coding=utf-8
from GOAP2.Bootstrapper import checkBuildMode
from GOAP2.DatabaseManager import DatabaseManager

class GroupManager(object):
    class EmptyGroup(object):
        def __init__(self):
            pass

        def hasObject(self, name):
            Trace.log("Group", 0, "You try to find object {} in EmptyGroup!!".format(name))
            return False

        def hasPrototype(self, name):
            Trace.log("Group", 0, "You try to find prototype {} in EmptyGroup!!".format(name))
            return False

    s_groups = {}
    s_groupsType = {}
    s_groupsDynamicInfos = {}
    s_initialized = False

    @staticmethod
    def onInitialize():
        GroupManager.s_initialized = True
        return True
        pass

    @staticmethod
    def onFinalize():
        # copy for delete in remove parent group
        for group in GroupManager.s_groups.values():
            if isinstance(group, GroupManager.EmptyGroup):
                continue
                pass

            if group.isDestroy() is True:
                continue
                pass

            ParentGroupName = group.getParentGroupName()
            if ParentGroupName is not None:
                GroupManager.__removeGroup(ParentGroupName)
                pass

            group.onFinalize()
            group.onDestroy()
            pass

        GroupManager.s_groups = {}
        GroupManager.s_groupsStage = {}
        GroupManager.s_groupsType = {}
        GroupManager.s_groupsDynamicInfos = {}

        GroupManager.s_initialized = False
        pass

    @staticmethod
    def isInitialized():
        return GroupManager.s_initialized

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            GroupName = record.get("GroupName")
            if GroupName is None:
                continue
                pass

            if GroupName in GroupManager.s_groups:
                Trace.log("Manager", 0, "GroupManage.loadGroups group %s already exist" % GroupName)
                continue
                pass

            ModuleName = record.get("ModuleName")

            if ModuleName is None:
                ModuleName = "Group"
                pass

            result = GroupManager.importGroup(ModuleName, GroupName)

            if result is None:
                return False
                pass
            pass

        for record in records:
            groupName = record.get("GroupName")

            if groupName is None:
                continue
                pass

            Dynamic = bool(int(record.get("Dynamic", 0)))
            if Dynamic is True:
                GroupManager.s_groupsDynamicInfos[groupName] = record
                continue
                pass

            ParentGroupName = record.get("ParentGroupName", None)
            Tag = record.get("Tag", None)
            Save = bool(int(record.get("Save", 0)))
            OffsetY = float(record.get("OffsetY", 0.0))
            Survey = int(record.get("Survey", 0))
            CE = int(record.get("CE", 0))
            BuildModeTags = record.get("BuildModeTags", [])

            if GroupManager.addGroup(groupName, ParentGroupName, Tag, Save, OffsetY, Survey, CE, BuildModeTags) is False:
                Trace.log("Manager", 0, "GroupManager.loadParams: load params %s invalid add group %s" % (param, groupName))
                return False
                pass
            pass

        return True
        pass

    @staticmethod
    def addGroupDynamic(groupName):
        if not groupName in GroupManager.s_groupsDynamicInfos:
            Trace.log("Manager", 0, "GroupManage.addGroupDynamic group info in missing for %s" % groupName)
            return
            pass

        record = GroupManager.s_groupsDynamicInfos[groupName]

        ParentGroupName = record.get("ParentGroupName", None)
        Tag = record.get("Tag", None)
        Save = bool(int(record.get("Save", 0)))
        OffsetY = float(record.get("OffsetY", 0.0))
        Survey = int(record.get("Survey", 0))
        CE = int(record.get("CE", 0))
        BuildModeTags = int(record.get("BuildMode", 0))

        GroupManager.addGroup(groupName, ParentGroupName, Tag, Save, OffsetY, Survey, CE, BuildModeTags)
        pass

    @staticmethod
    def addGroup(groupName, ParentGroupName, Tag, Save, OffsetY, Survey, CE, BuildModeTags):
        if groupName in GroupManager.s_groups:
            Trace.log("Manager", 0, "GroupManage.addGroup group %s already exist" % groupName)
            return False
            pass

        if checkBuildMode(groupName, Survey, CE, BuildModeTags) is True:
            GroupManager.s_groups[groupName] = GroupManager.EmptyGroup()
            return True

        group = GroupManager.__createGroup(groupName)

        if group is None:
            return False
            pass

        if Tag is None:
            if group.onInitialize() is False:
                Trace.log("Manager", 0, "GroupManage.addGroup group %s invalid initialize" % groupName)
                return False
                pass
            pass

        group.setSave(Save)
        group.setStageName(Tag)

        group.setParentGroupName(ParentGroupName)

        def __offsetY(obj):
            pos = obj.getPosition()
            new_pos = (pos[0], pos[1] + OffsetY)
            obj.setPosition(new_pos)
            pass

        group.visitChild(__offsetY)

        GroupManager.s_groups[groupName] = group

        return True
        pass

    @staticmethod
    def __removeGroup(groupName):
        if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
            return

        if not groupName in GroupManager.s_groups:
            Trace.log("Manager", 0, "GroupManage.removeGroup group %s is missing" % groupName)
            return

        group = GroupManager.s_groups.pop(groupName)

        if group.isDestroy():
            return
            pass

        ParentGroupName = group.getParentGroupName()
        if ParentGroupName is not None:
            GroupManager.__removeGroup(ParentGroupName)
            pass

        group.onFinalize()
        group.onDestroy()
        pass

    @staticmethod
    def importGroup(module, name):
        Name = "Group%s" % (name)
        FromName = module
        ModuleName = "%s.%s" % (FromName, Name)

        try:
            Module = __import__(ModuleName, fromlist=[FromName])
        except ImportError as ex:
            Trace.log("GroupManager", 0, "GroupManager.importGroup '%s' not found Group '%s' maybe not export from PSD?" % (name, ModuleName))

            return None
            pass

        GroupType = getattr(Module, Name)

        GroupManager.addGroupType(name, GroupType)

        return GroupType
        pass

    @staticmethod
    def addGroupType(name, GroupType):
        GroupManager.s_groupsType[name] = GroupType
        pass

    @staticmethod
    def initializeGroupTag(stageName):
        for name, group in GroupManager.s_groups.iteritems():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            groupStageName = group.getStageName()
            if stageName != groupStageName:
                continue
                pass

            if group.onInitialize() is False:
                Trace.log("Manager", 0, "GroupManage.initializeGroupTag group %s invalid initialize" % name)

                return False
                pass
            pass

        return True
        pass

    @staticmethod
    def __createGroup(name):
        if name not in GroupManager.s_groupsType:
            Trace.log("GroupManager", 0, "GroupManager.createGroup: group type %s not found)" % (name))

            return None
            pass

        GroupType = GroupManager.s_groupsType[name]

        group = GroupType()

        group.setName(name)

        group.onLoader()

        return group
        pass

    @staticmethod
    def hasGroup(name):
        return name in GroupManager.s_groups
        pass

    @staticmethod
    def getGroup(name):
        if GroupManager.hasGroup(name) is False:
            Trace.log("GroupManager", 0, "GroupManager.getGroup: not found group [%s], maybe forgot add [%s] in Groups.xls)" % (name, name))

            return None
            pass

        Group = GroupManager.s_groups[name]

        return Group
        pass

    @staticmethod
    def hasObject(groupName, objectName):
        if GroupManager.hasGroup(groupName) is False:
            return False
            pass

        group = GroupManager.getGroup(groupName)

        if group.hasObject(objectName) is False:
            return False
            pass

        return True
        pass

    @staticmethod
    def hasPrototype(groupName, prototypeName):
        if not GroupManager.hasGroup(groupName):
            return False

        group = GroupManager.getGroup(groupName)

        if not group.hasPrototype(prototypeName):
            return False

        return True

    @staticmethod
    def getObject(groupName, objectName):
        group = GroupManager.getGroup(groupName)

        if GroupManager.hasObject(groupName, objectName) is False:
            Trace.log("GroupManager", 0, "GroupManager.getObject: group '%s' not found object '%s')" % (groupName, objectName))
            return None
            pass

        obj = group.getObject(objectName)

        return obj
        pass

    @staticmethod
    def generateObjectUnique(objectName, groupName, prototypeName, **params):
        if GroupManager.hasGroup(groupName) is False:
            Trace.log("GroupManager", 0, "GroupManager.generateObjectUnique: not found group '%s')" % (groupName))
            return None
            pass

        group = GroupManager.getGroup(groupName)

        if group.hasPrototype(prototypeName) is False:
            Trace.log("GroupManager", 0, "GroupManager.generateObjectUnique: group '%s' not found prototype '%s')" % (groupName, prototypeName))
            return None
            pass

        obj = group.generateObjectUnique(objectName, prototypeName, **params)

        return obj
        pass

    @staticmethod
    def reloadGroup(groupName):
        if GroupManager.hasGroup(groupName) is True:
            return
            pass

        group = GroupManager.getGroup(groupName)
        group.onLoader()

        return group
        pass

    @staticmethod
    def reloadGroups():
        for group in GroupManager.s_groups.itervalues():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            if group.getSave() is False:
                continue
                pass

            group.onLoader()
            pass
        pass
    pass