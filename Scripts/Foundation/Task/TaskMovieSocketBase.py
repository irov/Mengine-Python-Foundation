from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.Task import Task

class TaskMovieSocketBase(MixinMovie, MixinEvent, Task):
    def _onParams(self, params):
        super(TaskMovieSocketBase, self)._onParams(params)

        self.SocketName = params.get("SocketName")

        self.Any = params.get("Any", False)
        self.UseArrowFilter = params.get("UseArrowFilter", True)
        self.Filter = params.get("Filter", None)

        self.AutoEnable = params.get("AutoEnable", False)
        pass

    def _onValidate(self):
        super(TaskMovieSocketBase, self)._onValidate()

        if self.Any is False and self.SocketName is None:
            self.validateFailed("SocketName is None")
            pass

        ResourceMovie = self.Movie.getResourceMovie()

        if self.Any is False and ResourceMovie.hasLayerType(self.SocketName, "MovieSocketShape") is False and ResourceMovie.hasLayerType(self.SocketName, "MovieSocketImage") is False:
            self.validateFailed("Movie %s not fount socket %s" % (self.Movie.getName(), self.SocketName))
            pass

        Enable = self.Movie.getEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Movie %s is Disable" % (self.Movie.getName()))
            pass
        pass

    def _onBaseFilter(self, name):
        if self.Any is True:
            return True
            pass

        if self.SocketName != name:
            return False
            pass

        if self.UseArrowFilter is True:
            if ArrowManager.emptyArrowAttach() is False:
                return False
                pass
            pass

        if self.Filter is not None:
            if self.Filter() is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovieSocketBase, self)._onRun()

        if self.AutoEnable is True:
            self.Movie.setEnable(True)
            pass
        pass

    def _onFinally(self):
        super(TaskMovieSocketBase, self)._onFinally()

        if self.AutoEnable is True:
            self.Movie.setEnable(False)
            pass
        pass
    pass