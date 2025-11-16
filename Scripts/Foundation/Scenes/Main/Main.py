from Foundation.GroupManager import GroupManager
from Foundation.SceneManager import SceneManager

class Main(object):
    def __init__(self):
        self.node = None  # Mengine.Scene - main scene

        self.sceneDescriptions = None
        self.groupOrder = []
        self.sceneName = None
        self.slots = {}  # { scene_name: Mengine.Layer2D }
        self.main_layer = None  # Mengine.Layer2D ("GameArea")

    def getName(self):
        return self.sceneName

    def getMainLayer(self):
        return self.main_layer

    def getSlot(self, name):
        if name not in self.slots:
            Trace.log("Entity", 0, "Main.getSlot: scene %s not found slot %s" % (self.sceneName, name))
            return None
            pass

        slot = self.slots[name]

        return slot

    def hasSlot(self, name):
        return name in self.slots

    def setDescription(self, name, description):
        self.sceneName = name
        self.sceneDescriptions = description
        pass

    def onCreate(self, node):
        self.node = node
        pass

    def onDestroy(self):
        self.node = None
        self.main_layer = None
        pass

    def onPreparation(self):
        sceneSlots = SceneManager.getSceneSlots(self.sceneDescriptions.scene)

        for slot in sceneSlots:
            layer = self.node.createChild(slot.type)
            layer.setSize((slot.width, slot.height))
            layer.setLocalPosition((slot.x, slot.y))
            layer.setName(slot.name)
            layer.enable()

            if slot.main is True:
                self.main_layer = layer
                pass

            self.slots[slot.name] = layer

            if slot.name not in self.sceneDescriptions.slots:
                continue

            description = self.sceneDescriptions.slots[slot.name]

            self.groupOrder.append(description)

            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description["Group"]

                group = GroupManager.getGroup(groupName)

                if group is None:
                    Trace.log("Entity", 0, "Main.onActivate: %s not found group %s (scene initialize)" % (self.sceneDescriptions.scene, groupName))
                    continue

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                groupScene = group.getScene()
                groupScene.disable()
                layer.addChild(groupScene)
                pass
            elif layerType == "Arrow":
                Mengine.setArrowLayer(layer)
                pass
            elif layerType == "Zoom":
                groupNames = description.get("Groups")
                for groupName in groupNames:
                    group = GroupManager.getGroup(groupName)

                    if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                        continue

                    if group is None:
                        Trace.log("Entity", 0, "Main.onActivate: %s not found group %s (zoom initialize)" % (self.sceneDescriptions.scene, groupName))
                        continue

                    if group.isInitialized() is False:
                        Trace.log("Entity", 0, "Main.onActivate: %s group %s not initialized" % (self.sceneDescriptions.scene, groupName))
                        continue

                    groupScene = group.getScene()
                    groupScene.disable()

                    layer.addChild(groupScene)
                    pass
                pass
            else:
                Trace.log("Entity", "0", "Main.onActivate: slot %s invalid type '%s'" % (slot, layerType))
                pass
            pass
        pass

    def onActivate(self):
        self.onPreparationGroups()
        self.onActivateGroups()
        self.onEnableGroups()
        self.onRunGroups()

        Notification.notify(Notificator.onSceneActivate, self.sceneName)
        pass

    def onDeactivate(self):
        Notification.notify(Notificator.onSceneDeactivate, self.sceneName)

        self.onDeactivateGroups()
        self.onDisableGroups()

        for slot in self.slots.itervalues():
            slot.removeChildren()
            Mengine.destroyNode(slot)
            pass

        self.slots = {}
        self.main_layer = None
        pass

    def foreachGroups(self, __lambdaGroups, isReverse = False, isEnable = False):
        for description in self.groupOrder if isReverse is False else reversed(self.groupOrder):
            if isEnable is True:
                enable = description.get("Enable", True)

                if enable is False:
                    continue
                pass

            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                group = GroupManager.getGroup(groupName)

                if isinstance(group, GroupManager.EmptyGroup):
                    continue

                __lambdaGroups(group)
                pass
            pass
        pass

    def onPreparationGroups(self):
        def __lambdaGroups(group):
            if group.isInitialized() is False:
                Trace.log("Entity", 0, "Main.onPreparationGroups: %s group %s not initialized" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onPreparation()
            pass

        self.foreachGroups(__lambdaGroups)
        pass

    def onActivateGroups(self):
        def __lambdaGroups(group):
            if group.isInitialized() is False:
                Trace.log("Entity", 0, "Main.onActivateGroups: %s group %s not initialized" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onActivate()
            pass

        self.foreachGroups(__lambdaGroups)
        pass

    def onEnableGroups(self):
        def __lambdaGroups(group):
            if group is None:
                Trace.log("Entity", "0", "Main.onEnableGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, group.getName()))
                return

            if group.getEnable() is True:
                Trace.log("Entity", "0", "Main.onEnableGroups: %s group %s already enable" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onEnable()
            pass

        self.foreachGroups(__lambdaGroups, isEnable=True)
        pass

    def onRunGroups(self):
        def __lambdaGroups(group):
            if group is None:
                Trace.log("Entity", 0, "Main.onRunGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onRun()
            pass

        self.foreachGroups(__lambdaGroups)
        pass

    def onDeactivateGroups(self):
        if GroupManager.isInitialized() is False:
            Trace.log("Entity", 0, "Main.onDeactivateGroups: GroupManager is not initialized (Maybe it is already finilized)")
            return

        def __lambdaGroups(group):
            if group is None:
                Trace.log("Entity", "0", "Main.onDeactivateGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onDeactivate()
            pass

        self.foreachGroups(__lambdaGroups, isReverse=True)
        pass

    def onDisableGroups(self):
        if GroupManager.isInitialized() is False:
            Trace.log("Entity", 0, "Main.onDisableGroups: GroupManager is not initialized (Maybe it is already finilized)")
            return

        def __lambdaGroups(group):
            if group is None:
                Trace.log("Entity", "0", "Main.onDisableGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, group.getName()))
                return

            group.onDisable()
            pass

        self.foreachGroups(__lambdaGroups, isReverse=True)
        pass
    pass