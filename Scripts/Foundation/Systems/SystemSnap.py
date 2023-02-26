from Foundation.SceneManager import SceneManager
from Foundation.SnapManager import SnapManager
from Foundation.System import System

class SystemSnap(System):
    def __init__(self):
        super(SystemSnap, self).__init__()
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneInit, self.__onSceneInit)
        self.addObserver(Notificator.onRenderViewportChange, self.__onRenderViewportChange)

        return True
        pass

    def __onRenderViewportChange(self, viewport, contentResolution):
        SceneName = SceneManager.getCurrentSceneName()
        if SceneName is None:
            return False
            pass

        self.__onSceneInit(SceneName)
        return False
        pass

    def __onSceneInit(self, SceneName):
        groups = SceneManager.getSceneLayerGroups(SceneName)
        for gr in groups:
            self.__doGroupSnap(gr)
            pass

        return False
        pass

    def __doGroupSnap(self, Group):
        GroupName = Group.getName()

        if SnapManager.hasSnapGroup(GroupName) is False:
            return
            pass

        SnapManager.applySnaps(GroupName)
        pass
    pass