from Foundation.LayerManager import LayerManager
from Foundation.Object.ChildObject import ChildObject
from Notification import Notification

class Group(ChildObject):
    Category = "Resources"  # FIXME

    def __init__(self):
        super(Group, self).__init__()

        self.save = False
        self.stageName = None

        self.scene = None
        self.enable = False
        self.states = {}
        self.ParentGroupName = None

        self.layers_desc = {}
        self.layers_order = []

        self.layers = {}

        self.main_layer = None
        pass

    def setParentGroupName(self, ParentGroupName):
        self.ParentGroupName = ParentGroupName
        pass

    def setSave(self, save):
        self.save = save
        pass

    def getSave(self):
        return self.save
        pass

    def setStageName(self, stageName):
        self.stageName = stageName
        pass

    def getStageName(self):
        return self.stageName
        pass

    def getParentGroupName(self):
        return self.ParentGroupName
        pass

    def getLayerParams(self):
        params = self._getLayerParams()

        return params
        pass

    def getScene(self):
        return self.scene
        pass

    def getMainLayer(self):
        return self.main_layer.node
        pass

    def createLayer(self, name, **params):
        if name in self.layers_desc:
            layer = self.layers_desc[name]

            return layer
            pass

        self.setCurrentLayerName(name)

        layer = LayerManager.createLayer(name, params)

        if layer is None:
            Trace.log("Main", 0, "invalid create layer %s type %s" % (name, Type))
            return None
            pass

        self.layers_desc[name] = layer
        self.layers_order.append(layer)

        return layer
        pass

    def getLayer(self, Name):
        if Name is None:
            return self.main_layer.node
            pass

        if Name not in self.layers:
            return None
            pass

        layer = self.layers.get(Name)

        return layer
        pass

    def _onInitialize(self):
        super(Group, self)._onInitialize()

        self.scene = Mengine.createScene(self.name, None)

        if self.scene is None:
            self.initializeFailed("invalid create Mengine.Scene %s" % (self.name))
            pass

        layerParams = self.getLayerParams()

        Name = layerParams.get("Name")

        self.main_layer = self.createLayer(Name, **layerParams)

        for layer in self.layers_order:
            node = layer.createNode(self.scene)

            name = layer.getName()
            self.layers[name] = node
            pass

        self.setEntity(self.main_layer.node)
        pass

    def _onFinalize(self):
        super(Group, self)._onFinalize()

        self.layers_desc = {}
        self.layers_order = []

        for layer in self.layers.itervalues():
            layer.removeChildren()
            Mengine.destroyNode(layer)
            pass

        self.layers = {}

        self.main_layer = None

        self.setEntity(None)

        self.onDisable()

        self.scene.removeChildren()

        Mengine.destroyNode(self.scene)
        self.scene = None
        pass

    def _onActivate(self):
        objects = self.getObjects()

        for obj in objects:
            obj.onActivate()

            obj_entity = obj.getEntityNode()

            if obj_entity is None:
                Trace.log("Object", 0, "'%s' invalid node %s get entity" % (self.getName(), obj.getName()))

                return False
                pass

            obj_entity.disable()

            layerName = obj.getLayerName()

            layer = self.getLayer(layerName)

            if layer is None:
                Trace.log("Object", 0, "'%s' invalid node %s get layer %s" % (self.getName(), obj.getName(), layerName))

                return False
                pass

            layer.addChild(obj_entity)

            obj.onEntityRestore()
            pass

        return True
        pass

    def _onDestroy(self):
        super(Group, self)._onDestroy()

        self.states = {}
        pass

    def onRun(self):
        objects = self.getObjects()

        for obj in objects:
            obj.onRun()
            pass

        return True
        pass

    def addState(self, state, value):
        if state in self.states:
            Trace.log("Object", 0, "'%s' already exist state %s" % (self.name, state))
            return

        self.states[state] = value
        pass

    def changeState(self, state, value):
        if state not in self.states:
            Trace.log("Object", 0, "'%s' not exist state %s" % (self.name, state))
            return
            pass

        self.states[state] = value
        pass

    def getState(self, state):
        if state not in self.states:
            Trace.log("Object", 0, "'%s' not exist state %s" % (self.name, state))
            return
            pass

        value = self.states[state]
        return value
        pass

    def disableObject(self, *disabled):
        for name in disabled:
            obj = self.getObject(name)

            if obj is None:
                Trace.log("Object", 0, "failed disable object '%s'" % (name))
                return
                pass

            obj.setParam("Enable", False)
            pass
        pass

    def _onInitializeFailed(self, ex):
        Trace.log("Group", 0, "Group '%s' initialize failed: %s" % (self.name, ex))
        pass

    def onPreparation(self):
        if self.isInitialized() is False:
            Trace.log("Group", 0, "Group '%s' invalid enable, not initialized" % (self.name))
            return
            pass

        Notification.notify(Notificator.onLayerGroupPreparation, self.name)
        pass

    def onEnable(self):
        if self.enable is True:
            Trace.log("Group", 0, "Group '%s' already enable" % (self.name))
            return
            pass

        if self.isInitialized() is False:
            Trace.log("Group", 0, "Group '%s' invalid enable, not initialized" % (self.name))
            return
            pass

        if self.isActive() is False:
            Trace.log("Group", 0, "Group '%s' invalid enable, not activate" % (self.name))
            return
            pass

        self.enable = True

        Notification.notify(Notificator.onLayerGroupEnableBegin, self.name)

        self.scene.enable()

        Notification.notify(Notificator.onLayerGroupEnable, self.name)
        pass

    def onDisable(self):
        if self.enable is False:
            return
            pass

        self.enable = False

        Notification.notify(Notificator.onLayerGroupRelease, self.name)

        self.scene.disable()
        self.scene.release()

        Notification.notify(Notificator.onLayerGroupDisable, self.name)
        pass

    def getEnable(self):
        return self.enable
        pass
    pass