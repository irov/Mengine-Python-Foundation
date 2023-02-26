from Foundation.SceneManager import SceneManager
from Foundation.Task.Task import Task

class TaskSceneEntering(Task):
    Skiped = True

    def _onRun(self):
        SceneManager.setCurrentSceneEntering(True)

        return True
        pass
    pass