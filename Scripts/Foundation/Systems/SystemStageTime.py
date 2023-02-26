from Foundation.System import System
from Notification import Notification

class SystemStageTime(System):

    def __init__(self):
        super(SystemStageTime, self).__init__()

        self.on_init_time = None
        self.on_init_scene_name = None

        self.last_passed_time = None
        self.last_passed_scene_name = None

        pass

    def _onParams(self, params):
        super(SystemStageTime, self)._onParams(params)

        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneInit, self._onSceneInit)
        self.addObserver(Notificator.onSceneLeave, self._onSceneLeave)

        return True
        pass

    def _onSceneInit(self, sceneName):
        self.on_init_time = Menge.getTimeMs()
        self.on_init_scene_name = sceneName

        return False
        pass

    def _onSceneLeave(self, sceneName):
        if sceneName == self.on_init_scene_name:
            self.last_passed_time = Menge.getTimeMs() - self.on_init_time
            self.last_passed_scene_name = sceneName

            self.sendAnalytics(self.last_passed_scene_name, self.last_passed_time)
            Notification.notify(Notificator.onStageTimePassed, self.last_passed_scene_name, self.last_passed_time)

        return False
        pass

    def sendAnalytics(self, stage_name, stage_time):
        data = {'clientID': Menge.getAccountUID(Menge.getCurrentAccountName()), 'category': 'Timing', 'action': 'Stage_Time', 'client_definition': {GoogleAnalytics.TimeDimension: stage_name, GoogleAnalytics.TimeMetric: stage_time, }}

        GoogleAnalytics.send_analytics(data)
        pass
    pass