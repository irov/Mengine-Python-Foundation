from Foundation.Notificator import Notificator
from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskSceneLayerGroupEnable(MixinObserver, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSceneLayerGroupEnable, self)._onParams(params)

        self.LayerName = params.get("LayerName")
        self.SceneName = params.get("SceneName", None)

        # We have parameter validation: "SceneManager.isCurrentSceneActive() is False"
        # so we can just make this parameter enabled on default
        self.WaitSceneInit = params.get("WaitSceneInit", False)

        self.Value = params.get("Value", True)

    def __enableGroup(self):
        layer_group = SceneManager.getSceneLayerGroup(self.SceneName, self.LayerName)

        if layer_group is None:
            self.log("Scene %s Layer %s Group is None" % (self.SceneName, self.LayerName))
            return

        if self.Value is True:
            if layer_group.onEnable() is False:
                self.log("Layer scene '%s' layer '%s' group '%s' already enabled" % (self.SceneName, self.LayerName, layer_group.name))
                pass
        else:
            if layer_group.onDisable() is False:
                self.log("Layer scene '%s' layer '%s' group '%s' already disabled" % (self.SceneName, self.LayerName, layer_group.name))
                pass

    def __cbOnSceneInit(self, scene_name):
        if scene_name != self.SceneName:
            return False

        self.__enableGroup()

        return True

    def _onRun(self):
        if self.SceneName is None:
            cur_scene_name = SceneManager.getCurrentSceneName()

            if cur_scene_name is None:
                if SceneManager.isTransitionProgress() is False:
                    self.invalidTask("Layer '%s' CurrentSceneName is None" % self.LayerName)

                return True

            self.SceneName = cur_scene_name

        if SceneManager.isCurrentSceneActive() is False and self.WaitSceneInit:
            self.addObserver(Notificator.onSceneInit, self.__cbOnSceneInit)
            return False

        else:
            self.__enableGroup()
            return True