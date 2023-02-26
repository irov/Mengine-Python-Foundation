from GOAP2.SceneManager import SceneManager
from GOAP2.Task.Task import Task

class TaskSceneEntering(Task):
    Skiped = True

    def _onRun(self):
        SceneManager.setCurrentSceneEntering(True)

        return True
        pass
    pass