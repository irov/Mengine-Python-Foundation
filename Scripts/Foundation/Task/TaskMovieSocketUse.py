from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieSocketUse(MixinMovie, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieSocketUse, self)._onParams(params)

        self.SocketName = params.get("SocketName")
        self.isDown = params.get("isDown", False)
        pass

    def _onInitialize(self):
        super(TaskMovieSocketUse, self)._onInitialize()
        if _DEVELOPMENT is True:
            ResourceMovie = self.Movie.getResourceMovie()
            hasSocket = Menge.hasMovieSocket(ResourceMovie, self.SocketName)
            if hasSocket is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        def __onSocketFilter(touchId, button, isDown, movieObject, hotspot, socketName):
            if isDown is not self.isDown:
                return False
                pass

            if ArrowManager.emptyArrowAttach() is True:
                return False
                pass

            if movieObject is not self.Movie:
                return False
                pass

            if socketName != self.SocketName:
                return False
                pass

            return True
            pass

        self.addObserver(Notificator.onMovieSocketClick, __onSocketFilter)

        return False
        pass

    pass