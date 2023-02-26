from GOAP2.GroupManager import GroupManager
from GOAP2.SceneManager import SceneManager
from Notification import Notification

class Main(object):
    def __init__(self):
        self.node = None  # Menge.Scene - main scene

        self.sceneDescriptions = None
        self.groupOrder = []
        self.sceneName = None
        self.slots = {}  # { scene_name: Menge.Layer2D }
        self.main_layer = None  # Menge.Layer2D ("GameArea")

    def getName(self):
        return self.sceneName

    def getMainLayer(self):
        return self.main_layer
        pass

    def getSlot(self, name):
        if name not in self.slots:
            Trace.log("Entity", 0, "Main.getSlot: scene %s not found slot %s" % (self.sceneName, name))
            return None
            pass

        slot = self.slots[name]

        return slot
        pass

    def hasSlot(self, name):
        return name in self.slots
        pass

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
            layer.setName(slot.name)
            layer.enable()

            if slot.main is True:
                self.main_layer = layer
                pass

            self.slots[slot.name] = layer

            if slot.name not in self.sceneDescriptions.slots:
                continue
                pass

            description = self.sceneDescriptions.slots[slot.name]

            self.groupOrder.append(description)

            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description["Group"]

                group = GroupManager.getGroup(groupName)

                if group is None:
                    Trace.log("Entity", 0, "Main.onActivate: %s not found group %s (scene initialize)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                groupScene = group.getScene()
                groupScene.disable()
                layer.addChild(groupScene)
                pass
            elif layerType == "Arrow":
                Menge.setArrowLayer(layer)
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
                        pass

                    if group.isInitialized() is False:
                        Trace.log("Entity", 0, "Main.onActivate: %s group %s not initialized" % (self.sceneDescriptions.scene, groupName))
                        continue
                        pass

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

    def onPreparationGroups(self):
        for description in self.groupOrder:
            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                group = GroupManager.getGroup(groupName)

                if group is None:
                    Trace.log("Entity", 0, "Main.onActivateGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                group.onPreparation()
                pass
            pass
        pass

    def onActivateGroups(self):
        for description in self.groupOrder:
            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                group = GroupManager.getGroup(groupName)

                if group is None:
                    Trace.log("Entity", 0, "Main.onActivateGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass
                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                group.onActivate()
                pass
            pass
        pass

    def onEnableGroups(self):
        for description in self.groupOrder:
            enable = description.get("Enable", True)

            if enable is False:
                continue
                pass

            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                group = GroupManager.getGroup(groupName)

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                if group is None:
                    Trace.log("Entity", "0", "Main.onEnableGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                if group.getEnable() is True:
                    Trace.log("Entity", "0", "Main.onEnableGroups: %s group %s already enable" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                group.onEnable()
                pass
            pass
        pass

    def onRunGroups(self):
        for description in self.groupOrder:
            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                group = GroupManager.getGroup(groupName)

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                if group is None:
                    Trace.log("Entity", 0, "Main.onRunGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                group.onRun()
                pass
            pass
        pass

    def onActivate(self):
        # onPreparation
        self.onPreparationGroups()

        # onActivate
        self.onActivateGroups()

        # onEnable
        self.onEnableGroups()

        self.onRunGroups()

        Notification.notify(Notificator.onSceneActivate, self.sceneName)

        pass

    def onDeactivateGroups(self):
        if GroupManager.isInitialized() is False:
            Trace.log("Entity", 0, "Main.onDeactivateGroups: GroupManager is not initialized (Maybe it is already finilized)")
            return

        for description in reversed(self.groupOrder):
            layerType = description["Type"]

            if layerType == "Scene":
                groupName = description.get("Group")

                group = GroupManager.getGroup(groupName)

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                if group is None:
                    Trace.log("Entity", "0", "Main.onDeactivateGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                group.onDeactivate()
                pass
            pass
        pass

    def onDisableGroups(self):
        if GroupManager.isInitialized() is False:
            Trace.log("Entity", 0, "Main.onDisableGroups: GroupManager is not initialized (Maybe it is already finilized)")
            return

        for description in reversed(self.groupOrder):
            layerType = description["Type"]
            if layerType == "Scene":
                groupName = description.get("Group")
                group = GroupManager.getGroup(groupName)

                if isinstance(GroupManager.getGroup(groupName), GroupManager.EmptyGroup):
                    continue

                if group is None:
                    Trace.log("Entity", "0", "Main.onDisableGroups: %s not found group %s (activate)" % (self.sceneDescriptions.scene, groupName))
                    continue
                    pass

                group.onDisable()
                pass
            pass
        pass

    def onDeactivate(self):
        Notification.notify(Notificator.onSceneDeactivate, self.sceneName)

        self.onDeactivateGroups()
        self.onDisableGroups()

        for slot in self.slots.itervalues():
            slot.removeChildren()
            Menge.destroyNode(slot)
            pass

        self.slots = {}
        self.main_layer = None
        pass
    pass