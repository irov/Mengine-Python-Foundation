from Foundation.Initializer import Initializer
from Foundation.Params import Params
from Foundation.SceneManager import SceneManager

class MixinScene(Params, Initializer):
    def __init__(self):
        super(MixinScene, self).__init__()

        self.SceneName = None
        pass

    def _onParams(self, params):
        super(MixinScene, self)._onParams(params)

        self.SceneName = params.get("SceneName", None)
        pass

    def _onInitialize(self):
        super(MixinScene, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.SceneName is not None:
                if SceneManager.hasScene(self.SceneName) is False:
                    self.initializeFailed("Scene '%s' not found" % (self.SceneName))
                    pass
                pass
            pass
        pass

    def _onFinalize(self):
        super(MixinScene, self)._onFinalize()

        self.SceneName = None
        pass

    def getSceneName(self):
        return self.SceneName
        pass
    pass