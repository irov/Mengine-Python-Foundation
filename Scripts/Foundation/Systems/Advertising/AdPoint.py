from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider

SCHEDULE_ID_EMPTY = 0
STATE_COOLDOWN_DISABLE = -1


class TriggerParams(object):

    """
        action tips:
            0) counter formula: `cooldown - offset`
            1) Show ad every 3 games (play 3 games without ads, then show ad)
                > trigger_action_offset = 3
                > trigger_action_cooldown = 3
            2) Show ad every 3 games, but on start no ad for next 10 games, then every 3 games as planned
                > trigger_action_offset = 10
                > trigger_action_cooldown = 3
            3) Show ad every 3 games, but on start show ad immediately, then every 3 games as planned
                > trigger_action_offset = 0
                > trigger_action_cooldown = 3

        time tips:
            0) at first runs schedule for `trigger_time_offset` minutes, then `trigger_time_cooldown` minutes always
            1) Show ad every 10 min, but on start show ad immediately
                > trigger_time_offset = 0
                > trigger_time_cooldown = 10
            2) Show ad every 10 min, but on start no ad for next 10 min, then every 10 min as planned
                > trigger_time_offset = 10
                > trigger_time_cooldown = 10
    """

    def __init__(self, params):
        self.name = params["name"]
        self.enable = params.get("enable", True)
        self.ad_type = params.get("ad_type", "Interstitial")
        self.ad_unit_name = params.get("ad_unit_name", self.ad_type)

        self.action_offset = max(params.get("trigger_action_offset", 0), 0)
        self.action_cooldown = params.get("trigger_action_cooldown", STATE_COOLDOWN_DISABLE)

        self.time_offset = max(params.get("trigger_time_offset", 0), 0)
        self.time_cooldown = params.get("trigger_time_cooldown", STATE_COOLDOWN_DISABLE)
        if self.time_cooldown != STATE_COOLDOWN_DISABLE:
            self.time_cooldown *= 1000.0
            self.time_offset *= 1000.0

        self.group = params.get("cooldown_group", None)

    def validate(self):
        def _error(message):
            Trace.msg_err("[AdPoint {}] validation error: {}".format(self.name, message))

    def isActionBased(self):
        return self.action_cooldown != STATE_COOLDOWN_DISABLE

    def isTimeBased(self):
        return self.time_cooldown != STATE_COOLDOWN_DISABLE

    def isEnable(self):
        return self.enable is True


class AdPoint(Initializer):

    def __init__(self):
        super(AdPoint, self).__init__()
        self.params = None  # type: TriggerParams  # noqa
        self.active = False

        self._last_view_timestamp = None

        # action based
        self._action_counter = 0

        # time based
        self._time_ready = False
        self._schedule_id = SCHEDULE_ID_EMPTY

        # trigger group resets this trigger if one of group members started
        self._cooldown_group_observer = None

    @property
    def name(self):
        return self.params.name

    def _onInitialize(self, trigger_params):
        self.params = TriggerParams(trigger_params)

        if self.params.validate() is False:
            return False
        return True

    def onActivate(self):
        if self.active is True:
            Trace.log("System", 0, "AdPoint '{}' is already activated".format(self.name))
            return False

        if self.params.isTimeBased() is True:
            self._createSchedule(self.params.time_offset)
        if self.params.isActionBased() is True:
            self._action_counter = self.params.action_cooldown - self.params.action_offset
        if self.params.group is not None:
            self._cooldown_group_observer = Notification.addObserver(Notificator.onAdPointStart, self._cbAdPointStart)

        self.active = True
        return True

    def _onFinalize(self):
        if self.active is False:
            Trace.log("System", 1, "AdPoint '{}' finalize before activate".format(self.name))

        self._removeSchedule()
        if self._cooldown_group_observer is not None:
            Notification.removeObserver(self._cooldown_group_observer)
            self._cooldown_group_observer = None

        self.params = None
        self.active = False

    def check(self):
        """ returns True if trigger conditions are met and ad is available to view """
        if self._checkTrigger() is False:
            return False

        # trigger is ok, check if ad is available
        if AdvertisementProvider.isAdvertAvailable(self.params.ad_type, self.params.ad_unit_name) is False:
            return False

        # ad is ready to view, allow to start!
        return True

    def _checkTrigger(self):
        """ returns True if at least one of trigger conditions is met """
        if self._time_ready is True:
            return True
        if self.params.isActionBased() is True and self._action_counter >= self.params.action_cooldown:
            return True
        return False

    def trigger(self):
        """ increase action counter """
        self._action_counter += 1
        Trace.msg_dev("[AdPoint {}] triggered, action counter = {}".format(self.name, self._action_counter))
        return False

    def start(self):
        def _cb(*args, **kwargs):
            Trace.msg("[AdPoint {}] show {}:{} advert using {}".format(
                self.name, self.params.ad_type, self.params.ad_unit_name, AdvertisementProvider.getName()))
            self.updateViewedTime(Mengine.getTime())

        Notification.notify(Notificator.onAdPointStart, self.params)
        TaskManager.runAlias("AliasShowAdvert", _cb,
                             AdType=self.params.ad_type, AdUnitName=self.params.ad_unit_name)
        self._resetTrigger()

        return False

    def _resetTrigger(self):
        if self.params.isTimeBased() is True:
            self._removeSchedule()
            self._createSchedule()
        self._action_counter = 0
        Trace.msg_dev("[AdPoint {}] reset trigger".format(self.name))

    # general utils

    def updateViewedTime(self, timestamp):
        if _DEVELOPMENT is True:
            _seconds_passed = (timestamp - self._last_view_timestamp) if self._last_view_timestamp else None
            Trace.msg("[AdPoint {}] updateViewedTime to {} ({} seconds from last view)".format(
                self.name, timestamp, _seconds_passed))
        self._last_view_timestamp = timestamp

    # time based trigger

    def __onSchedule(self, schedule_id, is_complete):
        if self._schedule_id != schedule_id:
            return
        self._schedule_id = SCHEDULE_ID_EMPTY

        self._time_ready = True
        Trace.msg_dev("[AdPoint {}] time based trigger is ready".format(self.name))

    def _createSchedule(self, cooldown=None):
        if cooldown is None:
            cooldown = self.params.time_cooldown
        self._schedule_id = Mengine.scheduleGlobal(cooldown, self.__onSchedule)

    def _removeSchedule(self):
        if self._schedule_id != SCHEDULE_ID_EMPTY:
            Mengine.scheduleGlobalRemove(self._schedule_id)
            self._schedule_id = SCHEDULE_ID_EMPTY

    # cooldown group

    def _cbAdPointStart(self, ad_point_params):
        if ad_point_params == self.params:
            return False

        if ad_point_params.group == self.params.group:
            Trace.msg_dev("[AdPoint {}] one of member ({}) of cooldown group '{}' is started"
                          .format(self.name, ad_point_params.name, self.params.group))
            self._resetTrigger()
        return False



