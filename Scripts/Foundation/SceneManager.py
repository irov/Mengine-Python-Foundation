from Foundation.Manager import Manager

from Foundation.Bootstrapper import checkPlatform
from Foundation.DatabaseManager import DatabaseManager
from Foundation.GroupManager import GroupManager
from Notification import Notification

import copy

class SceneManager(Manager):
    s_scenesType = {}

    s_blockGameScenes = 0
    s_scenes = {}
    s_gameScenes = []
    s_extraScenes = []
    s_specialScenes = {}
    s_defaultDescription = {}

    s_slots = {}

    s_currentDescription = None

    s_prevSceneName = None

    s_currentSceneName = None
    s_currentGameSceneName = None
    s_currentScene = None
    s_currentSceneEntering = False
    s_currentSceneSlots = None
    s_changeScene = False
    s_changeSceneName = None
    s_stageScenes = {}

    s_transitionProgress = False

    module = None

    @staticmethod
    def getGameScenes():
        return SceneManager.s_gameScenes

    @staticmethod
    def _onInitialize():
        SceneManager.addObserver(Notificator.onTransitionBegin, SceneManager.__onTransitionBegin)
        SceneManager.addObserver(Notificator.onTransitionEnd, SceneManager.__onTransitionEnd)
        SceneManager.addObserver(Notificator.onSessionSave, SceneManager.__onSessionSave)
        SceneManager.addObserver(Notificator.onSessionLoad, SceneManager.__onSessionLoad)
        SceneManager.addObserver(Notificator.onSessionRemoveComplete, SceneManager.__onSessionRemoveComplete)
        pass

    @staticmethod
    def _onFinalize():
        SceneManager.s_scenes = {}
        SceneManager.s_gameScenes = []
        SceneManager.s_extraScenes = []
        SceneManager.s_specialScenes = {}
        SceneManager.s_defaultDescription = {}
        SceneManager.s_slots = {}

        SceneManager.s_currentDescription = None

        SceneManager.s_changeSceneName = None
        SceneManager.s_currentSceneName = None

        SceneManager.s_currentGameSceneName = None

        SceneManager.s_currentScene = None
        SceneManager.s_currentSceneEntering = False
        pass

    @staticmethod
    def getSceneType(name):
        if name not in SceneManager.s_scenesType:
            Trace.log("Manager", 0, "SceneManager.getSceneType scene %s not found" % name)

            return None

        Type, module = SceneManager.s_scenesType.get(name)

        return Type

    @staticmethod
    def importScene(module, name):
        Name = "%s" % name
        FromName = module
        ModuleName = "%s.%s.%s" % (FromName, Name, Name)
        Module = __import__(ModuleName, fromlist=[FromName])
        Type = getattr(Module, Name)

        if name in SceneManager.s_scenesType:
            Type2, module2 = SceneManager.s_scenesType[name]

            Trace.log("Manager", 0, "SceneManager.importScene scene %s module %s already exist (module '%s')" % (name, module, module2))

            return None
            pass

        SceneManager.s_scenesType[name] = (Type, module)

        if Mengine.addScenePrototypeFinder(name, SceneManager.getSceneType) is False:
            Trace.log("Manager", 0, "SceneManager.importScene invalid scene %s module %s" % (name, module))

            return None
            pass

        return Type
        pass

    @staticmethod
    def importScenes(module, prototypes):
        for prototype in prototypes:
            SceneManager.importScene(module, prototype)
            pass
        pass

    @staticmethod
    def __onTransitionBegin(sceneFrom, sceneTo, ZoomGroupName):
        SceneManager.s_transitionProgress = True

        if SceneManager.isGameScene(sceneTo) is True:
            SceneManager.setCurrentGameSceneName(sceneTo)
            pass
        elif SceneManager.isGameScene(sceneFrom) is True:
            SceneManager.setCurrentGameSceneName(sceneFrom)
            pass

        return False
        pass

    @staticmethod
    def __onTransitionEnd(sceneFrom, sceneTo, ZoomGroupName):
        SceneManager.s_transitionProgress = False

        if SceneManager.isGameScene(sceneTo) is True:
            SceneManager.setCurrentGameSceneName(sceneTo)
            pass

        return False
        pass

    @staticmethod
    def __onSessionSave(params):
        params["SceneManager"] = {}

        gameSceneName = SceneManager.getCurrentGameSceneName()
        prevSceneName = SceneManager.getPrevSceneName()
        currentSceneName = SceneManager.getCurrentSceneName()
        if currentSceneName is None:
            currentSceneName = gameSceneName

        params["SceneManager"]["GameSceneName"] = gameSceneName
        params["SceneManager"]["CurrentSceneName"] = currentSceneName
        params["SceneManager"]["PreviousSceneName"] = prevSceneName
        return False
        pass

    @staticmethod
    def __onSessionLoad(params):
        gameSceneName = params["SceneManager"]["GameSceneName"]
        prevSceneName = params["SceneManager"].get("PreviousSceneName", None)
        currentSceneName = params["SceneManager"]["CurrentSceneName"]

        SceneManager.setCurrentGameSceneName(gameSceneName)
        SceneManager.s_prevSceneName = prevSceneName

        return False
        pass

    @staticmethod
    def __onSessionRemoveComplete():
        SceneManager.s_currentGameSceneName = None

        return False
        pass

    @staticmethod
    def isTransitionProgress():
        return SceneManager.s_transitionProgress
        pass

    @staticmethod
    def isCurrentSceneActive():
        if SceneManager.isTransitionProgress() is True:
            return False
            pass

        CurrentScene = SceneManager.getCurrentScene()

        if CurrentScene is None:
            return False
            pass

        if CurrentScene.node.isActivate() is False:
            return False
            pass

        return True
        pass

    class SceneDescription(object):
        def __init__(self, scene, slots):
            self.scene = scene
            self.slots = slots
            self.mainGroupName = None
            pass

        def getName(self):
            return self.scene
            pass

        def getSlotsGroup(self, slotsName):
            if slotsName not in self.slots:
                return None
                pass

            desc = self.slots[slotsName]

            return desc["Group"]
            pass

        def hasSlotsGroup(self, slotsName):
            return slotsName in self.slots.keys()
            pass
        pass

    class SceneSlot(object):
        __slots__ = "name", "type", "x", "y", "width", "height", "main"

        def __init__(self, name, type, x, y, width, height, main):
            self.name = name
            self.type = type
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.main = main
            pass
        pass

    @staticmethod
    def loadParams(module, param):
        SceneManager.module = module
        if param == "DefaultSlots":
            SceneManager.loadDefaultDescriptions(module, "DefaultSlots")
            pass
        elif param == "SceneSlots":
            if SceneManager.loadSceneSlots(module, "SceneSlots") is False:
                return False
                pass
            pass
        elif param == "Scenes":
            if SceneManager.loadScenes(module, "Scenes") is False:
                return False
                pass
            pass
        elif param == "Stages":
            Trace.log("Manager", 0, "SceneManager loadParams %s [%s] not implemented" % (param, module))
            # SceneManager.loadStageStartScenes(module, "Stages")
            pass
        else:
            return False
            pass

        return True
        pass

    @staticmethod
    def loadDefaultDescriptions(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            Platform = record.get("Platform")
            if checkPlatform(Platform) is False:
                continue

            SceneName = record.get("SceneName")
            DefaultSlot = record.get("DefaultSlot")

            SceneManager.loadDefaultDescription(SceneName, module, DefaultSlot)
            pass
        pass

    @staticmethod
    def addStageStartScenes(StageName, SceneName):
        SceneManager.s_stageScenes[StageName] = SceneName
        pass

    @staticmethod
    def getStages():
        return SceneManager.s_stageScenes.keys()
        pass

    @staticmethod
    def getStageStartScene(stageName):
        if stageName not in SceneManager.s_stageScenes.keys():
            return None
            pass

        return SceneManager.s_stageScenes[stageName]
        pass

    @staticmethod
    def loadDefaultDescription(name, module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        desc = {}
        for record in records:
            Platform = record.get("Platform")
            if checkPlatform(Platform) is False:
                continue

            Slot = record.get("Slot")
            Type = record.get("Type")
            Group = record.get("Group")
            Enable = bool(record.get("Enable", 1))
            ObjectsEnable = bool(record.get("ObjectsEnable", 1))

            desc[Slot] = dict(Type=Type, Group=Group, Enable=Enable, ObjectsEnable=ObjectsEnable)

        SceneManager.s_defaultDescription[name] = desc

    @staticmethod
    def changeDefaultSlotGroup(name, slotName, newGroup):
        desc = SceneManager.s_defaultDescription[name]
        slot = desc[slotName]
        slot["Group"] = newGroup
        pass

    @staticmethod
    def changeDefaultSlotGroupEnable(name, slotName, value):
        if name not in SceneManager.s_defaultDescription:
            return
            pass
        desc = SceneManager.s_defaultDescription[name]
        if slotName not in desc:
            return
            pass
        slot = desc[slotName]
        slot["Enable"] = value
        pass

    @staticmethod
    def loadSceneSlot(name, module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        if records is None:
            return False

        slots = []
        for record in records:
            Name = record.get("Name")
            Type = record.get("Type")
            X = record.get("X", 0.0)
            Y = record.get("Y", 0.0)
            Width = record.get("Width")
            Height = record.get("Height")
            Main = bool(record.get("Main"))

            if Width is None or Height is None:
                Trace.log("SceneManager", 0, "SceneManager.loadSceneSlot: scene %s invalid size %s:%s" % (Name, Width, Height))
                return False

            slot = SceneManager.SceneSlot(Name, Type, X, Y, Width, Height, Main)
            slots.append(slot)

        SceneManager.s_slots[name] = slots

        return True

    @staticmethod
    def loadSceneSlots(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        if records is None:
            return False
            pass

        for record in records:
            Platform = record.get("Platform")
            if checkPlatform(Platform) is False:
                continue

            SceneName = record.get("SceneName")
            SceneSlots = record.get("SceneSlots")

            if SceneManager.loadSceneSlot(SceneName, module, SceneSlots) is False:
                return False
                pass
            pass

        return True
        pass

    @staticmethod
    def loadScenes(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)
        for record in records:
            Platform = record.get("Platform")
            if checkPlatform(Platform) is False:
                continue

            SceneName = record.get("SceneName")
            DefaultScene = record.get("DefaultScene")
            BaseScene = record.get("BaseScene")
            SlotName = record.get("SlotName")
            SceneType = record.get("SceneType")
            GroupName = record.get("GroupName")
            GameScene = bool(record.get("GameScene", 0))
            ExtraScene = bool(record.get("ExtraScene", 0))

            if SceneManager.addScene(SceneName, DefaultScene, BaseScene, SlotName, SceneType, GroupName, GameScene, ExtraScene) is False:
                return False
                pass
            pass

        return True
        pass

    @staticmethod
    def getScenes():
        """ Return all scenes from Params/Scenes.xlsx """
        return SceneManager.s_scenes.keys()

    @staticmethod
    def addScene(SceneName, DefaultScene, BaseScene, SlotName, SceneType, GroupName, GameScene, ExtraScene):
        if SceneName not in SceneManager.s_scenes:
            copyDescription = {}

            if DefaultScene is not None:
                if DefaultScene not in SceneManager.s_defaultDescription:
                    Trace.log("SceneManager", 0, "SceneManager.loadScenes: not found default scene %s for scene %s" % (DefaultScene, SceneName))

                    return False
                    pass

                description = SceneManager.s_defaultDescription[DefaultScene]

                copyDescription = copy.deepcopy(description)
                pass

            SceneManager.s_scenes[SceneName] = SceneManager.SceneDescription(BaseScene, copyDescription)
            pass

        descriptions = SceneManager.s_scenes[SceneName]

        slots = descriptions.slots

        if SlotName not in slots:
            slots[SlotName] = {}
            pass

        slot = slots[SlotName]

        if BaseScene not in SceneManager.s_slots:
            Trace.log("SceneManager", 0, "SceneManager.loadScenes: not found base scene %s for scene %s" % (BaseScene, SceneName))

            return False
            pass

        scene_slots = SceneManager.s_slots[BaseScene]

        for descriptionSlot in scene_slots:
            if descriptionSlot.name != SlotName:
                continue
                pass

            if descriptionSlot.main is False:
                continue
                pass

            descriptions.mainGroupName = GroupName
            pass

        slot["Type"] = SceneType

        if SceneType == "Scene":
            slot["Group"] = GroupName
            if GameScene is True:
                SceneManager.s_gameScenes.append(SceneName)
                pass

            if ExtraScene is True:
                SceneManager.s_extraScenes.append(SceneName)
                pass
        elif SceneType == "Zoom":
            if "Groups" not in slot:
                slot["Groups"] = [GroupName]
            else:
                slot["Groups"].append(GroupName)
                pass
        else:
            Trace.log("SceneManager", 0, "SceneManager.loadParam: scene '%s' slot '%s' invalid type '%s'" % (SceneName, SlotName, SceneType))
            pass

        return True
        pass

    @staticmethod
    def blockGameScenes(value):
        if value is True:
            SceneManager.s_blockGameScenes += 1
            pass
        else:
            SceneManager.s_blockGameScenes -= 1
            pass
        pass

    @staticmethod
    def isBlockGameScenes():
        if SceneManager.s_blockGameScenes == 0:
            return False
            pass
        return True
        pass

    @staticmethod
    def isCurrentGameScene():
        SceneName = SceneManager.getCurrentSceneName()
        if SceneName not in SceneManager.s_gameScenes:
            return False
            pass

        return True
        pass

    @staticmethod
    def isGameScene(sceneName):
        if sceneName not in SceneManager.s_gameScenes:
            return False
            pass

        return True
        pass

    @staticmethod
    def getSceneDescription(name):
        if name not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneDescription: description for scene '%s' not found (Maybe add to Scenes.xlsx)" % name)
            return None
            pass

        description = SceneManager.s_scenes[name]

        return description

    @staticmethod
    def visitSceneDescriptions(visitor):
        for description in SceneManager.s_scenes.values():
            visitor(description)

    @staticmethod
    def getSceneGroups(name):
        return SceneManager.__getSceneGroups(name)
        pass

    @staticmethod
    def __getSceneGroups(name):
        if SceneManager.hasScene(name) is False:
            return None
            pass

        groups = []

        sceneDescriptions = SceneManager.getSceneDescription(name)

        for slot, description in sceneDescriptions.slots.iteritems():
            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description["Group"]
                groups.append(groupName)
                pass
            # elif layerType == "Zoom":
            #     groupNames = description.get("Groups")
            #
            #     groups.extend(groupNames)
            #     pass
            pass

        return groups
        pass

    @staticmethod
    def __getDiffSceneGroups(oldSceneName, newSceneName):
        old_groups = SceneManager.__getSceneGroups(oldSceneName)
        new_groups = SceneManager.__getSceneGroups(newSceneName)

        if old_groups is None:
            return []
            pass

        if new_groups is None:
            return []
            pass

        diff_groups = []

        for groupName in old_groups:
            if groupName in new_groups:
                diff_groups.append(groupName)
                pass
            pass

        return diff_groups
        pass

    @staticmethod
    def __cacheResourcesGroups(oldSceneName, newSceneName):
        cache_groups = SceneManager.__getDiffSceneGroups(oldSceneName, newSceneName)

        cache_groups_resource = []

        for groupName in cache_groups:
            Group = GroupManager.getGroup(groupName)
            if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                continue

            print "<SceneManager> cache scene '%s' group '%s' resources" % (newSceneName, groupName)

            resources = Mengine.cacheResources(Group.name)

            cache_groups_resource.append(resources)
            pass

        return cache_groups_resource
        pass

    @staticmethod
    def __cacheActiveGroups(oldSceneName, newSceneName):
        cache_groups = SceneManager.__getDiffSceneGroups(oldSceneName, newSceneName)

        cache_groups_active = []

        for groupName in cache_groups:
            Group = GroupManager.getGroup(groupName)

            if isinstance(Group, GroupManager.EmptyGroup):
                continue

            if Group.isActive() is False:
                continue

            Group.onActivate()

            cache_groups_active.append(Group)
            pass

        return cache_groups_active

    @staticmethod
    def isChangeScene():
        return SceneManager.s_changeScene

    @staticmethod
    def disableCurrentScene():
        if SceneManager.s_currentScene is None:
            Trace.log("SceneManager", 0, "SceneManager.deactivateScene current scene is None")

            return False

        SceneManager.s_currentScene.node.disable()
        pass

    @staticmethod
    def restartScene(cb):
        if SceneManager.s_currentSceneName is None:
            Trace.log("SceneManager", 0, "SceneManager.restartScene: Scene Name is None")
            return

        SceneManager.changeScene(SceneManager.s_currentSceneName, cb, False)
        pass

    @staticmethod
    def changeScene(sceneName, cb, check_current=True, immediately=False):
        if sceneName is None:
            Trace.log("SceneManager", 0, "SceneManager.changeScene: Scene Name is None")
            return

        if SceneManager.s_changeScene is True:
            Trace.log("SceneManager", 0, "SceneManager.changeScene: Already Change Scene To %s" % sceneName)
            return

        if SceneManager.hasScene(sceneName) is False:
            Trace.log("SceneManager", 0, "SceneManager.changeScene: Scene '%s' not found" % sceneName)
            return

        sceneDescription = SceneManager.s_scenes[sceneName]

        if check_current is True and sceneDescription is SceneManager.s_currentDescription:
            if cb is not None:
                cb(SceneManager.s_currentScene)
                pass
            return

        Notification.notify(Notificator.onSceneChange, SceneManager.s_currentSceneName)

        SceneManager.s_prevSceneName = SceneManager.s_currentSceneName

        print "<SceneManager> change scene from '%s' to '%s'" % (SceneManager.s_currentSceneName, sceneName)

        Trace.trace()

        cache_resources_groups = SceneManager.__cacheResourcesGroups(SceneManager.s_currentSceneName, sceneName)
        cache_active_groups = SceneManager.__cacheActiveGroups(SceneManager.s_currentSceneName, sceneName)

        print "cache_resources_groups", cache_resources_groups
        print "cache_active_groups", cache_active_groups

        SceneManager.s_currentScene = None
        SceneManager.s_currentSceneName = None
        SceneManager.s_currentDescription = None
        SceneManager.s_currentSceneEntering = False

        SceneManager.s_changeScene = True
        SceneManager.s_changeSceneName = sceneName

        Trace.msg_dev("<SceneManager> change scene to '%s'" % sceneName)

        if Mengine.createCurrentScene("Main", sceneName, immediately, True, SceneManager._onChangeScene, sceneName, sceneDescription, cache_resources_groups, cache_active_groups, cb) is False:
            print "<SceneManager> change scene to '%s' failed" % sceneName

            for resources in cache_resources_groups:
                Mengine.uncacheResources(resources)
                pass

            for Group in cache_active_groups:
                Group.onDeactivate()
                pass
            pass
        pass

    @staticmethod
    def _onChangeScene(scene, isActive, isError, sceneName, sceneDescription, cache_resources_groups, cache_active_groups, cb):
        print "_onChangeScene", scene, isActive, isError, sceneName, sceneDescription, cache_resources_groups, cache_active_groups, cb

        if isError is True:
            Trace.log("SceneManager", 0, "SceneManager._onChangeScene: change scene '%s' failed" % sceneName)

            for resources in cache_resources_groups:
                Mengine.uncacheResources(resources)
                pass

            for Group in cache_active_groups:
                Group.onDeactivate()
                pass

            SceneManager.s_changeSceneName = None
            SceneManager.s_changeScene = False
            return

        if scene is None:
            if sceneName in SceneManager.s_gameScenes and sceneName not in SceneManager.s_extraScenes:
                SceneManager.setCurrentGameSceneName(sceneName)
                pass

            Notification.notify(Notificator.onSceneRemoved, SceneManager.s_prevSceneName)
            return

        print "<SceneManager> change scene '%s' isActive %s" % (sceneName, isActive)

        if isActive is False:
            SceneManager.s_currentScene = scene
            SceneManager.s_currentSceneName = sceneName

            SceneManager.s_currentDescription = sceneDescription
            SceneManager.s_currentSceneEntering = False

            scene.setDescription(sceneName, sceneDescription)

            sceneDescription = SceneManager.s_scenes[sceneName]
            SceneManager.s_currentSceneSlots = SceneManager.s_slots[sceneDescription.scene]

            Notification.notify(Notificator.onScenePreparation, sceneName)
            return

        print "<SceneManager> uncache resources %s" %(cache_resources_groups)

        for resources in cache_resources_groups:
            print "<SceneManager> uncache scene '%s' resources '%s' group '%s'" % (sceneName, resources, resources.getGroupName())
            Mengine.uncacheResources(resources)
            pass

        for Group in cache_active_groups:
            Group.onDeactivate()
            pass

        SceneManager.s_changeSceneName = None
        SceneManager.s_changeScene = False
        # SceneManager.s_prevSceneName = None

        Notification.notify(Notificator.onSceneInit, sceneName)

        if cb is not None:
            cb(scene)
            pass
        pass

    @staticmethod
    def removeCurrentScene(cb):
        SceneManager.s_currentScene = None
        SceneManager.s_currentSceneName = None
        SceneManager.s_currentDescription = None
        SceneManager.s_currentSceneEntering = False
        SceneManager.s_changeSceneName = None
        SceneManager.s_changeScene = False

        Mengine.removeCurrentScene(False, cb)

    @staticmethod
    def setCurrentSceneEntering(Value):
        SceneManager.s_currentSceneEntering = Value

        if Value is True:
            Notification.notify(Notificator.onSceneEnter, SceneManager.s_currentSceneName)
        else:
            Notification.notify(Notificator.onSceneLeave, SceneManager.s_currentSceneName)
            pass
        pass

    @staticmethod
    def isCurrentScene(sceneName):
        if sceneName != SceneManager.s_currentSceneName:
            return False

        return True

    @staticmethod
    def isSceneInit(sceneName):
        if SceneManager.s_currentSceneName != sceneName:
            return False

        if SceneManager.s_changeSceneName is not None:
            return False

        return True

    @staticmethod
    def isSceneEnter(sceneName):
        if SceneManager.s_currentSceneName != sceneName:
            return False

        if SceneManager.s_currentSceneEntering is False:
            return False

        return True

    @staticmethod
    def isCurrentSceneEntering():
        return SceneManager.s_currentSceneEntering


    @staticmethod
    def getCurrentDescription():
        return SceneManager.s_currentDescription

    @staticmethod
    def getSceneSlots(SceneName):
        if SceneName not in SceneManager.s_slots:
            Trace.log("SceneManager", 0, "SceneManager.getSceneSlots: not found slots for scene %s " % SceneName)
            return None

        slots = SceneManager.s_slots[SceneName]

        return slots

    @staticmethod
    def getCurrentScene():
        return SceneManager.s_currentScene

    @staticmethod
    def getCurrentSceneName():
        return SceneManager.s_currentSceneName

    @staticmethod
    def setCurrentGameSceneName(sceneName):
        Notification.notify(Notificator.onGameSceneChange, SceneManager.s_currentGameSceneName, sceneName)
        SceneManager.s_currentGameSceneName = sceneName
        pass

    @staticmethod
    def getCurrentGameSceneName():
        return SceneManager.s_currentGameSceneName

    @staticmethod
    def getChangeSceneName():
        return SceneManager.s_changeSceneName

    @staticmethod
    def getPrevSceneName():
        return SceneManager.s_prevSceneName

    @staticmethod
    def getSceneLayerGroup(SceneName, LayerName):
        if SceneName not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneLayerGroup: not found scene %s %s" % (SceneName, LayerName))
            return None

        currentDescription = SceneManager.s_scenes[SceneName]

        if LayerName not in currentDescription.slots:
            Trace.log("SceneManager", 0, "SceneManager.getSceneLayerGroup: scene %s not found slot %s" % (SceneName, LayerName))
            return None

        slot = currentDescription.slots[LayerName]

        if slot["Type"] != "Scene":
            Trace.log("SceneManager", 0, "SceneManager.getSceneLayerGroup: scene %s:%s is not type 'Scene'" % (SceneName, LayerName))
            return None

        groupName = slot["Group"]

        group = GroupManager.getGroup(groupName)

        return group

    @staticmethod
    def isSceneLayerGroupEnable(SceneName, LayerName):
        """ returns True if group is enabled on given (or current) Scene """

        if SceneName is None:
            SceneName = SceneManager.getCurrentSceneName()

        layer_group = SceneManager.getSceneLayerGroup(SceneName, LayerName)

        if layer_group is None:
            Trace.log("Manager", 0, "Scene %s Layer %s Group is None" % (SceneName, LayerName))
            return

        enable = layer_group.getEnable()

        return enable

    @staticmethod
    def enableSceneLayerGroup(SceneName, LayerName):
        layer_group = SceneManager.getSceneLayerGroup(SceneName, LayerName)

        if layer_group is None:
            Trace.log("Manager", 0, "Enable Scene %s Layer %s Group is None" % (SceneName, LayerName))
            return

        enable = layer_group.getEnable()

        if enable is True:
            return

        layer_group.onEnable()
        Notification.notify(Notificator.onEnableSceneLayerGroup, SceneName, LayerName)
        pass

    @staticmethod
    def disableSceneLayerGroup(SceneName, LayerName):
        layer_group = SceneManager.getSceneLayerGroup(SceneName, LayerName)

        if layer_group is None:
            Trace.log("Manager", 0, "Disable Scene %s Layer %s Group is None" % (SceneName, LayerName))
            return

        enable = layer_group.getEnable()

        if enable is False:
            return

        layer_group.onDisable()
        Notification.notify(Notificator.onDisableSceneLayerGroup, SceneName, LayerName)

        pass

    @staticmethod
    def getSceneLayerGroups(SceneName):
        if SceneName not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneLayerGroups: not found scene '%s'" % SceneName)
            return None
            pass

        currentDescription = SceneManager.s_scenes[SceneName]

        groups = []
        for slot in currentDescription.slots.itervalues():
            if slot["Type"] != "Scene":
                continue

            groupName = slot["Group"]

            group = GroupManager.getGroup(groupName)

            groups.append(group)
            pass

        return groups

    @staticmethod
    def hasLayerScene(name):
        scene = SceneManager.s_currentScene
        if scene is None:
            return False

        result = scene.hasSlot(name)

        return result

    @staticmethod
    def getLayerScene(name):
        scene = SceneManager.s_currentScene

        slot = scene.getSlot(name)

        return slot

    @staticmethod
    def hasSceneZoom(sceneName, zoomName):
        if sceneName not in SceneManager.s_scenes:
            return False

        sceneDescription = SceneManager.s_scenes[sceneName]

        if "Zoom" not in sceneDescription.slots:
            return False

        zoomDesc = sceneDescription.slots["Zoom"]

        if zoomDesc["Type"] != "Zoom":
            return False

        zooms = zoomDesc["Groups"]

        if zoomName not in zooms:
            return False

        return True

    @staticmethod
    def getSceneMainGroupName(sceneName):
        if sceneName is None:
            return None

        if sceneName not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneZoom: scene %s not found" % sceneName)
            return None

        sceneDescription = SceneManager.s_scenes[sceneName]

        return sceneDescription.mainGroupName

    @staticmethod
    def getSceneZoomGroup(sceneName, zoomName):
        if sceneName not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneZoom: scene %s not found (%s)" % (sceneName, zoomName))
            return None

        scene = SceneManager.s_scenes[sceneName]

        if "Zoom" not in scene.slots:
            Trace.log("SceneManager", 0, "SceneManager.getSceneZoomGroup: scene %s zoom empty (%s)" % (sceneName, zoomName))
            return None

        zoomDesc = scene.slots["Zoom"]

        if zoomDesc["Type"] != "Zoom":
            Trace.log("SceneManager", 0, "SceneManager.getSceneZoomGroup: scene %s zoom invalid type (%s)" % (sceneName, zoomName))
            return None

        zooms = zoomDesc["Groups"]

        if zoomName not in zooms:
            Trace.log("SceneManager", 0, "SceneManager.getSceneZoomGroup: scene %s not have zoom %s" % (sceneName, zoomName))
            return None

        group = GroupManager.getGroup(zoomName)

        return group

    @staticmethod
    def hasScene(sceneName):
        return sceneName in SceneManager.s_scenes

    @staticmethod
    def hasSceneZooms(sceneName):
        if sceneName not in SceneManager.s_scenes:
            return False

        sceneDescription = SceneManager.s_scenes[sceneName]

        if "Zoom" not in sceneDescription.slots:
            return False

        zoomDesc = sceneDescription.slots["Zoom"]

        if zoomDesc["Type"] != "Zoom":
            return False

        zooms = zoomDesc["Groups"]

        return len(zooms) != 0

    @staticmethod
    def getSceneZooms(sceneName):
        if sceneName not in SceneManager.s_scenes:
            Trace.log("SceneManager", 0, "SceneManager.getSceneZooms: scene %s not found" % sceneName)
            return False

        sceneDescription = SceneManager.s_scenes[sceneName]

        if "Zoom" not in sceneDescription.slots:
            return None

        zoomDesc = sceneDescription.slots["Zoom"]

        if zoomDesc["Type"] != "Zoom":
            return None

        zooms = zoomDesc["Groups"]

        if len(zooms) == 0:
            return None

        return zooms

    @staticmethod
    def findZoomMainScene(zoomGroupName):
        """
        Warning! This is slow algorithm, do not use it often
        """
        sceneNames = SceneManager.getScenes()
        for sceneName in sceneNames:
            sceneZooms = SceneManager.getSceneZooms(sceneName)
            if sceneZooms and zoomGroupName in sceneZooms:
                return sceneName

    @staticmethod
    def loadSpecialScenes(module, name):
        records = DatabaseManager.getDatabaseRecords(module, name)

        for value in records:
            SpecialSceneName = value.get("SpecialSceneName")
            SceneName = value.get("SceneName")

            SceneManager.s_specialScenes[SpecialSceneName] = SceneName
            pass
        pass

    @staticmethod
    def isSpecialScene(sceneName):
        if sceneName in SceneManager.s_specialScenes:
            return True
        return False

    @staticmethod
    def getSpecialSceneName(sceneNameFrom):
        if SceneManager.hasSpecialScene(sceneNameFrom) is False:
            Trace.log("SceneManager", 0, "SceneManager.getSpecialSceneName invalid param sceneNameFrom %s, it don't have special scene" % sceneNameFrom)
            return None
        for special, scene in SceneManager.s_specialScenes.iteritems():
            if scene == sceneNameFrom:
                return special
            continue
        pass

    @staticmethod
    def hasSpecialScene(sceneName):
        for special, scene in SceneManager.s_specialScenes.iteritems():
            if scene == sceneName:
                return True
            continue
        return False

    @staticmethod
    def getSpecialMainSceneName(sceneName):
        if SceneManager.isSpecialScene(sceneName) is False:
            Trace.log("SceneManager", 0, "SceneManager.getSpecialMainSceneName  scene %s is not special and don't have related scene" % sceneName)
            return None
        record = SceneManager.s_specialScenes[sceneName]
        return record

    @staticmethod
    def getSceneBase(sceneName):
        records = DatabaseManager.getDatabaseRecords(SceneManager.module, "Scenes")
        BaseScene = None
        for record in records:
            if record.get("SceneName") == sceneName:
                BaseScene = record.get("BaseScene")
                break
        return BaseScene