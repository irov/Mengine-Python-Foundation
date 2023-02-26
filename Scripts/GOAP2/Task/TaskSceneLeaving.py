from GOAP2.SceneManager import SceneManager
from GOAP2.Task.Task import Task

class TaskSceneLeaving(Task):
    Skiped = True

    def _onRun(self):
        SceneManager.setCurrentSceneEntering(False)
        return True
        pass
    pass