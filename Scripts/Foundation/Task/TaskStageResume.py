from Foundation.SceneManager import SceneManager
from Foundation.Task.TaskAlias import TaskAlias
from GOAP3.StageManager import StageManager
from GOAP3.TransitionManager import TransitionManager
from GOAP3.ZoomManager import ZoomManager

class TaskStageResume(TaskAlias):

    def _onParams(self, params):
        super(TaskStageResume, self)._onParams(params)
        pass

    def _onGenerate(self, source):
        SceneName = SceneManager.getCurrentGameSceneName()

        if SceneName is None:
            Stage = StageManager.getCurrentStage()
            SceneName = Stage.getSceneName()

            if SceneName is None:
                Trace.log("Task", 0, "TaskStageResume: SceneName is None - no GameScene and no Stage ({}) SceneName".format(Stage.getName()))

        ZoomName = ZoomManager.getCurrentGameZoomName()

        if ZoomName is None:
            Stage = StageManager.getCurrentStage()
            ZoomName = Stage.getZoomName()

        source.addFunction(TransitionManager.changeScene, SceneName, ZoomName, True)

        return True