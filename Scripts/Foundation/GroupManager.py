from Foundation.Manager import Manager
from Foundation.Bootstrapper import checkBuildMode, checkPlatform
from Foundation.DatabaseManager import DatabaseManager

class GroupManager(Manager):
    class EmptyGroup(object):
        def __init__(self):
            pass

        def hasObject(self, name):
            Trace.log("Group", 0, "You try to find object {} in EmptyGroup!!".format(name))
            return False

        def hasPrototype(self, name):
            Trace.log("Group", 0, "You try to find prototype {} in EmptyGroup!!".format(name))
            return False

        def getEnable(self):
            Trace.log("Group", 0, "You try to check enable in EmptyGroup!!")
            return False

    s_groups = {}
    s_groupsType = {}
    s_groupsDynamicInfos = {}

    @staticmethod
    def _onInitialize(*args):
        return True

    @staticmethod
    def _onFinalize():
        # copy for delete in remove parent group
        for group in GroupManager.s_groups.values():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            if group.isDestroy() is True:
                continue

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
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            GroupName = record.get("GroupName")
            if GroupName is None:
                continue

            if GroupName in GroupManager.s_groups:
                Trace.log("Manager", 0, "GroupManage.loadGroups group %s already exist" % GroupName)
                continue

            ModuleName = record.get("ModuleName")

            if ModuleName is None:
                ModuleName = "Group"
                pass

            result = GroupManager.importGroup(ModuleName, GroupName)

            if result is None:
                return False
            pass

        for record in records:
            groupName = record.get("GroupName")

            if groupName is None:
                continue

            Dynamic = bool(int(record.get("Dynamic", 0)))
            if Dynamic is True:
                GroupManager.s_groupsDynamicInfos[groupName] = record
                continue

            ParentGroupName = record.get("ParentGroupName", None)
            Tag = record.get("Tag", None)
            Save = bool(int(record.get("Save", 0)))
            OffsetX = float(record.get("OffsetX", 0.0))
            OffsetY = float(record.get("OffsetY", 0.0))
            Survey = int(record.get("Survey", 0))
            CE = int(record.get("CE", 0))
            BuildModeTags = record.get("BuildModeTags", [])
            Platform = record.get("Platform", None)

            if GroupManager.addGroup(groupName, ParentGroupName, Tag, Save, OffsetX, OffsetY, Survey, CE, BuildModeTags, Platform) is False:
                Trace.log("Manager", 0, "GroupManager.loadParams: load params %s invalid add group %s" % (param, groupName))
                return False
            pass

        return True

    @staticmethod
    def addGroupDynamic(groupName):
        if _DEVELOPMENT is True:
            if not groupName in GroupManager.s_groupsDynamicInfos:
                Trace.log("Manager", 0, "GroupManage.addGroupDynamic group info in missing for %s" % groupName)
                return
            pass

        record = GroupManager.s_groupsDynamicInfos[groupName]

        ParentGroupName = record.get("ParentGroupName", None)
        Tag = record.get("Tag", None)
        Save = bool(int(record.get("Save", 0)))
        OffsetX = float(record.get("OffsetX", 0.0))
        OffsetY = float(record.get("OffsetY", 0.0))
        Survey = int(record.get("Survey", 0))
        CE = int(record.get("CE", 0))
        BuildModeTags = int(record.get("BuildMode", 0))
        Platform = record.get("Platform", None)

        GroupManager.addGroup(groupName, ParentGroupName, Tag, Save, OffsetX, OffsetY, Survey, CE, BuildModeTags, Platform)
        pass

    @staticmethod
    def addGroup(groupName, ParentGroupName, StageName, Save, OffsetX, OffsetY, Survey, CE, BuildModeTags, Platform):
        if _DEVELOPMENT is True:
            if groupName in GroupManager.s_groups:
                Trace.log("Manager", 0, "GroupManage.addGroup group %s already exist" % groupName)
                return False
            pass


        if checkBuildMode(groupName, Survey, CE, BuildModeTags) is True:
            GroupManager.s_groups[groupName] = GroupManager.EmptyGroup()
            return True

        if checkPlatform(Platform) is False:
            GroupManager.s_groups[groupName] = GroupManager.EmptyGroup()
            Trace.msg_dev("[GroupManager] Platform '%s' Group '%s' not match current platform" % (Platform, groupName))
            return True

        group = GroupManager.__createGroup(groupName)

        if group is None:
            return False

        if StageName is None:
            if group.onInitialize() is False:
                Trace.log("Manager", 0, "GroupManage.addGroup group %s invalid initialize" % groupName)
                return False
            pass

        group.setSave(Save)
        group.setStageName(StageName)

        group.setParentGroupName(ParentGroupName)

        def __offsetXY(obj):
            pos = obj.getPosition()
            new_pos = (pos[0] + OffsetX, pos[1] + OffsetY)
            obj.setPosition(new_pos)
            pass

        group.visitChildren(__offsetXY)

        GroupManager.s_groups[groupName] = group

        return True

    @staticmethod
    def __removeGroup(groupName):
        if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
            return

        if not groupName in GroupManager.s_groups:
            Trace.log("Manager", 0, "GroupManage.removeGroup group %s is missing" % groupName)
            return

        group = GroupManager.s_groups.pop(groupName)

        if group.isDestroy() is True:
            return

        ParentGroupName = group.getParentGroupName()
        if ParentGroupName is not None:
            GroupManager.__removeGroup(ParentGroupName)
            pass

        StageName = group.getStageName()

        if StageName is None:
            group.onFinalize()
            pass
        pass

    @staticmethod
    def __importGroupDemain(module, name):
        ModuleName = "%s.%s" % (module, name)

        try:
            Module = __import__(ModuleName, fromlist=[module])
        except ImportError as ex:
            Trace.log("Manager", 0, "GroupManager.__importGroupDemain module '%s' not found group '%s' maybe not export from PSD?" % (module, name))
            return None

        try:
            GroupType = getattr(Module, name)
        except AttributeError as ex:
            Trace.log("Manager", 0, "GroupManager.__importGroupDemain module '%s' not found type '%s'" % (ModuleName, name))
            return None

        try:
            GroupType.declareORM(GroupType)
        except ParamsException as pex:
            Trace.log("Manager", 0, "GroupManager.__importGroupDemain module %s group %s declare ORM error: %s\n%s" % (ModuleName, GroupType, pex, traceback.format_exc()))
            return None

        return GroupType

    @staticmethod
    def importGroup(module, name):
        GroupType = GroupManager.s_groupsType.get(name)

        if GroupType is not None:
            return GroupType

        GroupName = "Group%s" % (name)

        NewGroupType = GroupManager.__importGroupDemain(module, GroupName)

        if NewGroupType is None:
            return None

        GroupManager.addGroupType(name, NewGroupType)

        return NewGroupType

    @staticmethod
    def addGroupType(name, GroupType):
        GroupManager.s_groupsType[name] = GroupType
        pass

    @staticmethod
    def initializeGroupStageName(stageName):
        for name, group in GroupManager.s_groups.iteritems():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            groupStageName = group.getStageName()

            if stageName != groupStageName:
                continue

            if group.onInitialize() is False:
                Trace.log("Manager", 0, "GroupManage.initializeGroupStageName stage %s group %s invalid initialize" % (stageName, name))

                return False
            pass

        return True

    @staticmethod
    def __createGroup(name):
        if _DEVELOPMENT is True:
            if name not in GroupManager.s_groupsType:
                Trace.log("Manager", 0, "GroupManager.createGroup: group type %s not found" % name)
                return None
            pass

        GroupType = GroupManager.s_groupsType[name]
        group = GroupType()
        group.setName(name)
        group.onLoader()

        return group

    @staticmethod
    def hasGroup(name):
        return name in GroupManager.s_groups

    @staticmethod
    def getGroup(name):
        if GroupManager.hasGroup(name) is False:
            Trace.log("Manager", 0, "GroupManager.getGroup: not found group [%s], maybe forgot add [%s] in Groups.xls)" % (name, name))

            return None

        Group = GroupManager.s_groups[name]

        return Group

    @staticmethod
    def hasObject(groupName, objectName):
        if GroupManager.hasGroup(groupName) is False:
            return False

        group = GroupManager.getGroup(groupName)

        if group.hasObject(objectName) is False:
            return False

        return True

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
            Trace.log("Manager", 0, "GroupManager.getObject: group '%s' not found object '%s')" % (groupName, objectName))
            return None

        obj = group.getObject(objectName)

        return obj

    @staticmethod
    def generateObjectUnique(objectName, groupName, prototypeName, EntityHierarchy=True, **prototypeParams):
        if GroupManager.hasGroup(groupName) is False:
            Trace.log("Manager", 0, "GroupManager.generateObjectUnique: not found group '%s')" % (groupName))
            return None

        group = GroupManager.getGroup(groupName)

        if group.hasPrototype(prototypeName) is False:
            Trace.log("Manager", 0, "GroupManager.generateObjectUnique: group '%s' not found prototype '%s' params '%s')" % (groupName, prototypeName, prototypeParams))
            return None

        obj = group.generateObjectUnique(objectName, prototypeName, EntityHierarchy=EntityHierarchy, **prototypeParams)

        return obj

    @staticmethod
    def reloadGroup(groupName):
        if GroupManager.hasGroup(groupName) is True:
            return

        group = GroupManager.getGroup(groupName)
        group.onLoader()

        return group

    @staticmethod
    def reloadGroups():
        for group in GroupManager.s_groups.itervalues():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            if group.getSave() is False:
                continue

            group.onLoader()

    @staticmethod
    def isEnableGroup(groupName):
        if GroupManager.hasGroup(groupName) is False:
            return False

        group = GroupManager.getGroup(groupName)
        is_enable = group.getEnable()

        return is_enable is True
