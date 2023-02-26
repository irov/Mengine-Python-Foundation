from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskSceneLayerAddEntity(MixinObject, Task):
    Skiped = True

    def __init__(self):
        super(TaskSceneLayerAddEntity, self).__init__()
        pass

    def _onParams(self, params):
        super(TaskSceneLayerAddEntity, self)._onParams(params)
        self.LayerName = params.get("LayerName")
        self.AdaptScreen = params.get("AdaptScreen", False)
        pass

    def _onInitialize(self):
        super(TaskSceneLayerAddEntity, self)._onInitialize()

        if _DEVELOPMENT is True:
            if SceneManager.hasLayerScene(self.LayerName) is False:
                self.initializeFailed("invalid get Layer %s" % (self.LayerName))
                pass
            pass
        pass

    def _onCheck(self):
        ObjectEntity = self.Object.getEntity()

        if ObjectEntity is None:
            self.log("invalid object entity %s add to layer %s" % (self.ObjectName, self.LayerName))

            return False
            pass

        return True
        pass

    def _onRun(self):
        ObjectEntity = self.Object.getEntity()

        if self.AdaptScreen is True:
            Camera = Menge.getRenderCamera2D()
            ScreenPosition = ObjectEntity.getCameraPosition(Camera)
            self.Object.setPosition((ScreenPosition.x, ScreenPosition.y))
            pass

        Layer = SceneManager.getLayerScene(self.LayerName)

        Layer.addChild(ObjectEntity.node)

        return True
        pass
    pass