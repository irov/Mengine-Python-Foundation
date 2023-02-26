from Foundation.SceneManager import SceneManager
from Foundation.Task.Task import Task

class TaskSceneLeaving(Task):
    Skiped = True

    def _onRun(self):
        SceneManager.setCurrentSceneEntering(False)
        return True
        pass
    pass