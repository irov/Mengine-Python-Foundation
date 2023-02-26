from Foundation.SceneManager import SceneManager
from Foundation.System import System

"""
System manage game timing multiply. listen onSceneInit,onKeyEvent,onTimingFactor events
"""

class SystemTiming(System):
    SCHEDULE_NOT_INIT = -1

    def __init__(self):
        super(SystemTiming, self).__init__()

        self._scheduleId = SystemTiming.SCHEDULE_NOT_INIT
        self.pause = None
        pass

    def _onParams(self, params):
        super(SystemTiming, self)._onParams(params)

        # delta which added for timing
        self.timingFactorDelta = params.get("TimingFactorDelta", 0.0125)
        # time for view current timing on screen
        self.timingViewTime = params.get("TimingViewTime", 4000.0)
        self.textNode = None
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneInit, self.__onSceneInit)
        self.addObserver(Notificator.onTimingFactor, self.__onTimingFactor)

        return True
        pass

    def _onStop(self):
        pass

    #########################################################

    def __removeSchedule(self):
        if self.isOnSchedule() is not True:
            return False
            pass

        self.textNode.removeFromParent()
        Mengine.destroyNode(self.textNode)
        self.textNode = None

        if Mengine.scheduleRemove(self._scheduleId) is False:
            Trace.trace()
            pass

        self._scheduleId = SystemTiming.SCHEDULE_NOT_INIT
        pass

    def cb_timing(self, *args):
        for elem in args:
            print
            elem,
        pass

    def __attachSchedule(self, reloadTime):
        self._scheduleId = Mengine.schedule(reloadTime, self.__disableTextNode, self.cb_timing)
        pass

    def isOnSchedule(self):
        return self._scheduleId != SystemTiming.SCHEDULE_NOT_INIT
        pass

    def __disableTextNode(self, ID, isRemoved, somefunc):
        if self._scheduleId != ID:
            return
            pass

        if isRemoved is False:
            return
            pass

        self.textNode.removeFromParent()
        Mengine.destroyNode(self.textNode)
        self.textNode = None

        self._scheduleId = SystemTiming.SCHEDULE_NOT_INIT
        pass

    #########################################################

    def __onSceneInit(self, sceneName):
        self.__removeSchedule()
        return False
        pass

    def __onTimingFactor(self, factor):
        scene = SceneManager.getCurrentScene()
        if scene is None:
            Trace.log("System", 0, "__onTimingFactor scene is None")
            return False
            pass

        layer = scene.getMainLayer()
        if layer is None:
            Trace.log("System", 0, "__onTimingFactor layer is None")
            return False
            pass

        self.__removeSchedule()

        self.textNode = layer.createChild("TextField")
        self.textNode.setTextID("__ID_TIMING")
        self.textNode.setFontName("__CONSOLE_FONT__")
        self.textNode.setTextFormatArgs(round(factor, 2))
        self.textNode.enable()
        self.textNode.setWorldPosition((5.0, 20.0))

        self.__attachSchedule(self.timingViewTime * factor)

        return False
        pass
    pass