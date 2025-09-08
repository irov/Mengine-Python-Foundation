from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskTransition(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskTransition, self)._onParams(params)

        self.SceneName = params.get("SceneName")
        self.CheckToScene = params.get("CheckToScene", True)
        self.Wait = params.get("Wait", True)
        self.SkipTaskChains = params.get("SkipTaskChains", True)
        pass

    def _onCheck(self):
        if self.CheckToScene is True:
            CurrentSceneName = SceneManager.getCurrentSceneName()

            if CurrentSceneName == self.SceneName:
                return False

        ChangeSceneName = SceneManager.getChangeSceneName()

        if self.SceneName == ChangeSceneName:
            return False

        return True

    def _onRun(self):
        SceneManager.s_changeSceneName = self.SceneName

        Notification.notify(Notificator.onTransition, self.SceneName)

        if self.Wait is False:
            SceneManager.changeScene(self.SceneName, None, self.CheckToScene)
            return True

        if SceneManager.isChangeScene() is False:
            def __onTransition(scene):
                self.complete()
                pass

            SceneManager.changeScene(self.SceneName, __onTransition, self.CheckToScene)

            return False

        def __onSceneInit(sceneName):
            if self.SceneName != sceneName:
                return False

            self.complete()

            return True

        self.addObserver(Notificator.onSceneInit, __onSceneInit)

        return False

    def _onCancel(self):
        self.log("%s try cancel!!!" % (self.SceneName))
        pass
    pass