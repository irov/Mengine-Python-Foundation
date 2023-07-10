from Foundation.System import System
from Notification import Notification

ANALYTIC_PREFIX_NAME = "mng_"


class SystemAnalytics(System):
    s_active_analytics = {}
    __static_extra_params_methods = []
    __ignore_log_events = []

    class AnalyticUnit(object):
        allowed_types = (int, str, float, bool)

        def __init__(self, event_key, identity, check_method=None, create_params_method=None):
            self.key = event_key
            self._service_key = ANALYTIC_PREFIX_NAME + event_key
            self.identity = identity

            self._check = None
            if check_method is not None and callable(check_method) is True:
                self._check = check_method

            self._create_params = None
            if create_params_method is not None:
                if callable(create_params_method) is True:
                    self._create_params = create_params_method
                if create_params_method is False:
                    # no params
                    self._create_params = lambda *_, **__: {}

            self._observer = None
            self.create_observer()

        def create_observer(self):
            if self._observer is not None:
                return

            def _cb(*args, **kwargs):
                if self.check(*args, **kwargs) is False:
                    return False
                params = self.create_params(*args, **kwargs)
                self.send(params)
                return False

            observer = Notification.addObserver(self.identity, _cb)
            self._observer = observer

        def check(self, *args, **kwargs):
            """ check is analytic ready to send event """
            if self._check is None:
                return True
            else:
                ans = self._check(*args, **kwargs)
                return ans

        def create_params(self, *args, **kwargs):
            """ returns params that will be sent with event call """
            if self._create_params is None:
                params = kwargs.copy()
                for i, arg in enumerate(args):
                    if isinstance(arg, self.allowed_types) is False:
                        continue
                    params["value_{}".format(i + 1)] = arg
            else:
                params = self._create_params(*args, **kwargs)

            # extra params such as current scene, previous scene, etc
            params.update(SystemAnalytics.getExtraAnalyticParams())

            return params

        def send(self, params):
            """ finally send event with name from `self.key` and params from `params` dict """
            SystemAnalytics._sendDebugLog(self.key, params)
            Mengine.analyticsCustomEvent(self._service_key, None, params)

        def clean(self):
            if self._observer is not None:
                Notification.removeObserver(self._observer)
                self._observer = None
            self._check = None
            self._create_params = None
            self.identity = None
            self.key = None

    class EarnCurrencyAnalytic(AnalyticUnit):
        def send(self, params):
            currency_name = params["name"]  # str
            amount = params["amount"]   # float
            _params = {"name": currency_name, "amount": amount}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsEarnVirtualCurrencyEvent(currency_name, amount)

    class SpentCurrencyAnalytic(AnalyticUnit):
        def send(self, params):
            currency_name = params["name"]  # str
            amount = params["amount"]   # float
            descr = params["description"]   # str
            _params = {"name": currency_name, "amount": amount, "description": descr}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsSpendVirtualCurrencyEvent(descr, currency_name, amount)

    class UnlockAchievementAnalytic(AnalyticUnit):
        def send(self, params):
            achievement_id = params["achievement_id"]   # str
            _params = {"achievement_id": achievement_id}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsUnlockAchievementEvent(achievement_id)

    class LevelUpAnalytic(AnalyticUnit):
        def send(self, params):
            name = params["name"] + "_level"    # str
            level = params["level"]     # int
            _params = {"name": name, "level": level}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsLevelUp(name, level)

    class LevelStartAnalytic(AnalyticUnit):
        def send(self, params):
            name = params["name"]   # str
            _params = {"name": name}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsLevelStart(name)

    class LevelEndAnalytic(AnalyticUnit):
        def send(self, params):
            name = params["name"]   # str
            successful = params["successful"]   # bool
            _params = {"name": name, "successful": successful}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsLevelEnd(name, successful)

    class SelectItemAnalytic(AnalyticUnit):
        def send(self, params):
            category = params["category"]   # str
            item_id = params["item_id"]   # str
            _params = {"category": category, "item_id": item_id}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsSelectItem(category, item_id)

    class TutorialBeginAnalytic(AnalyticUnit):
        def send(self, params):
            SystemAnalytics._sendDebugLog(self.key, {})
            Mengine.analyticsTutorialBegin()

    class TutorialCompleteAnalytic(AnalyticUnit):
        def send(self, params):
            SystemAnalytics._sendDebugLog(self.key, {})
            Mengine.analyticsTutorialComplete()

    class ScreenViewAnalytic(AnalyticUnit):
        def send(self, params):
            screen_type = params["screen_type"]   # str
            screen_name = params["screen_name"]   # str
            _params = {"screen_type": screen_type, "screen_name": screen_name}

            SystemAnalytics._sendDebugLog(self.key, _params)
            Mengine.analyticsScreenView(screen_type, screen_name)

    def _onInitialize(self):
        self.addDefaultAnalytics()

    def _onFinalize(self):
        # clean up
        for analytics_unit in SystemAnalytics.s_active_analytics.values():
            analytics_unit.clean()
        SystemAnalytics.s_active_analytics = {}
        SystemAnalytics.__static_extra_params_methods = []
        SystemAnalytics.__ignore_log_events = []

    @staticmethod
    def addExtraAnalyticParams(static_method):
        if _DEVELOPMENT is True:
            test_params = static_method()
            if isinstance(test_params, dict) is False:
                Trace.log("System", 0, "Wrong extra params method return type {} (must be dict)".format(type(test_params)))
                return

        SystemAnalytics.__static_extra_params_methods.append(static_method)

    @staticmethod
    def getExtraAnalyticParams():
        params = {}
        for extra_method in SystemAnalytics.__static_extra_params_methods:
            extra_params = extra_method()
            params.update(extra_params)
        return params

    @staticmethod
    def hasAnalytic(event_key):
        return event_key in SystemAnalytics.s_active_analytics

    @staticmethod
    def addAnalytic(event_key, identity, check_method=None, params_method=None):
        """ create and run new analytic unit with name `ANALYTIC_PREFIX_NAME + event_key` into analytic service

            @param event_key: event id without service prefix (ANALYTIC_PREFIX_NAME)
            @param identity: Notificator identity id that triggers analytic
            @param check_method: should get same args as notificator sends: returns bool, if True - send event
            @param params_method: should get same args as notificator sends: returns dict
        """
        if SystemAnalytics.hasAnalytic(event_key) is True:
            Trace.log("System", 1, "SystemAnalytics already has analytic with event key '%s'" % event_key)
            return False

        analytics_unit = SystemAnalytics.AnalyticUnit(event_key, identity,
                                                      check_method=check_method, create_params_method=params_method)

        SystemAnalytics.s_active_analytics[analytics_unit.key] = analytics_unit
        return True

    @staticmethod
    def addSpecificAnalytic(event_type, event_key, identity, check_method=None, params_method=None):
        specific_analytics = {
            "earn_currency": SystemAnalytics.EarnCurrencyAnalytic,
            "spent_currency": SystemAnalytics.SpentCurrencyAnalytic,
            "unlock_achievement": SystemAnalytics.UnlockAchievementAnalytic,
            "level_up": SystemAnalytics.LevelUpAnalytic,
            "level_start": SystemAnalytics.LevelStartAnalytic,
            "level_end": SystemAnalytics.LevelEndAnalytic,
            "select_item": SystemAnalytics.SelectItemAnalytic,
            "tutorial_begin": SystemAnalytics.TutorialBeginAnalytic,
            "tutorial_complete": SystemAnalytics.TutorialCompleteAnalytic,
            "screen_view": SystemAnalytics.ScreenViewAnalytic,
        }

        if event_type not in specific_analytics:
            Trace.log("System", 0, "SystemAnalytics unknown event type '%s'" % event_type)
            return False

        if SystemAnalytics.hasAnalytic(event_key) is True:
            Trace.log("System", 1, "SystemAnalytics already has analytic with event key '%s'" % event_key)
            return False

        event_class = specific_analytics[event_type]

        analytics_unit = event_class(event_type, identity,
                                     check_method=check_method, create_params_method=params_method)

        SystemAnalytics.s_active_analytics[event_key] = analytics_unit
        return True

    @staticmethod
    def sendCustomAnalytic(event_key, send_params):
        """ force sends analytic event to analytic service """
        params = SystemAnalytics.getExtraAnalyticParams()
        params.update(send_params)

        SystemAnalytics._sendDebugLog(event_key, params)
        Mengine.analyticsCustomEvent(ANALYTIC_PREFIX_NAME+event_key, None, params)

    def addDefaultAnalytics(self):
        """ create default analytics and run them """
        self.addSpecificAnalytic("screen_view", "scene_open", Notificator.onSceneActivate,
                                 params_method=lambda name: {"screen_type": "MengineScene", "screen_name": name})

        self._addDefaultAnalytics()

    def _addDefaultAnalytics(self):
        return

    @staticmethod
    def addRelatedAnalytics(this_event_key, related_event_key, Filter=None, Params=None):
        """ Creates analytics based on analytic with key `related_event_key`.
            Sends this event if Filter is True.
            For specific params input Params as function <- related_event_params_dict
        """
        def check_method(type, event_key, timestamp, params):
            return event_key == ANALYTIC_PREFIX_NAME+related_event_key and Filter(params) is True
        def params_method(type, event_key, timestamp, params):
            return Params(params)

        return SystemAnalytics.addAnalytic(this_event_key, Notificator.onAnalyticsEvent,
                                           check_method=check_method, params_method=params_method)

    @staticmethod
    def addIgnoreLogEventKey(event_key):
        if event_key not in SystemAnalytics.__ignore_log_events:
            SystemAnalytics.__ignore_log_events.append(event_key)

    @staticmethod
    def isEventKeyInIgnore(event_key):
        return event_key in SystemAnalytics.__ignore_log_events

    @staticmethod
    def _sendDebugLog(event_key, params):
        if _DEVELOPMENT is False:
            return
        if 'analytics' not in Mengine.getOptionValues("debug"):
            return
        if SystemAnalytics.isEventKeyInIgnore(event_key) is True:
            return
        Trace.msg("<SystemAnalytics> send analytic event '{}': {}".format(event_key, params))
