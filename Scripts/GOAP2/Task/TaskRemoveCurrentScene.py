from GOAP2.SceneManager import SceneManager
from GOAP2.Task.Task import Task

class TaskRemoveCurrentScene(Task):
    def _onRun(self):
        SceneManager.removeCurrentScene(self.__removeCurrentSceneComplete)

        return False
        pass

    def __removeCurrentSceneComplete(self):
        self.complete()
        pass
    pass