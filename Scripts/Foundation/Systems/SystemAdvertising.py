from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.SceneManager import SceneManager
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger

_Log = SimpleLogger("SystemAdvertising")

class SystemAdvertising(System):
    disable_key = "075ae3d2fc31640504f814f60e5ef713"
    account_disable_setting_key = "IsInterstitialDisabled"

    is_enable = False
    s_interstitial_params = {}
    s_general_params = {}

    s_ignore_scenes = [
        "CutScene", "Menu", "Bonus", "SplashScreen", "Intro", "PreIntro",
        "DebugMenu", "Store", "Guides", "Map", "MapBonusChapter"
    ]

    def __init__(self):
        super(SystemAdvertising, self).__init__()
        self._first_enter_timestamp = None
        self._start_delay_done = False
        self._last_view_timestamp = None
        self._current_trigger_count = 0

    def _onInitialize(self):
        if Mengine.hasTouchpad() is False:
            return
        if Mengine.getConfigBool('Advertising', "Interstitial", False) is False:
            return

        interstitial_params = {
            "transition": Mengine.getConfigBool('Advertising', "ShowOnTransition", False),
            "mg_reset": Mengine.getConfigBool('Advertising', "ShowOnResetMG", False),
            "chapter_done": Mengine.getConfigBool('Advertising', "ShowOnChapterDone", False),
            "trigger": Mengine.getConfigBool('Advertising', "ShowOnTrigger", False),
        }

        general_params = {
            "view_delay": Mengine.getConfigInt('Advertising', "ViewDelayInMinutes", 10) * 60,
            "delay_on_start": Mengine.getConfigInt('Advertising', "StartDelayInMinutes", 5) * 60,
            "trigger": Mengine.getConfigString('Advertising', "TriggerNotificatorName", ""),
            "trigger_count_start": Mengine.getConfigInt('Advertising', "TriggerCountStart", 0),
            "trigger_count_show": Mengine.getConfigInt('Advertising', "TriggerCountShow", 1),
        }

        self._current_trigger_count = general_params["trigger_count_start"]

        SystemAdvertising.s_interstitial_params = interstitial_params
        SystemAdvertising.s_general_params = general_params
        SystemAdvertising.is_enable = True

        self.__initDisableAccountParam()

    def _onRun(self):
        if self.is_enable is False:
            return True

        self._first_enter_timestamp = Mengine.getTime()

        self.__addObservers()
        return True

    def _onFinalize(self):
        SystemAdvertising.is_enable = False

    @classmethod
    def isInterstitialParamEnable(cls, key):
        if cls.is_enable is False:
            return False
        return cls.s_interstitial_params.get(key, False)

    @classmethod
    def getGeneralParam(cls, key):
        return cls.s_general_params.get(key)

    def showInterstitial(self, descr=None):
        def _cb(*args, **kwargs):
            _Log("show interstitial advert using {} [action={!r}]".format(AdvertisementProvider.getName(), descr))
            self.updateViewedTime(Mengine.getTime())

        TaskManager.runAlias("AliasShowAdvert", _cb, AdType="Interstitial")

    def hasPermissionToViewAd(self, timestamp):
        if self._start_delay_done is False:
            start_delay = self.getGeneralParam("delay_on_start")
            seconds_since_first_enter = timestamp - self._first_enter_timestamp

            if seconds_since_first_enter >= start_delay:
                self._start_delay_done = True
                return True
            return False

        if self._last_view_timestamp is None:
            return True

        view_delay = self.getGeneralParam("view_delay")
        if (timestamp - self._last_view_timestamp) > view_delay:
            return True
        return False

    def updateViewedTime(self, timestamp):
        if _DEVELOPMENT is True:
            _seconds_passed = (timestamp - self._last_view_timestamp) if self._last_view_timestamp else None
            _Log("updateViewedTime to {} ({} seconds from last view)".format(timestamp, _seconds_passed))
        self._last_view_timestamp = timestamp

    def __initDisableAccountParam(self):
        def __addExtraAccountSettings(accountID, isGlobal):
            if isGlobal is True:
                return
            Mengine.addCurrentAccountSetting(self.account_disable_setting_key, u'no', None)

        from Foundation.AccountManager import AccountManager
        AccountManager.addCreateAccountExtra(__addExtraAccountSettings)

    def disableForever(self):
        """ used for stop interstitial forever for current user (e.g. purchased 'no ads' product) """

        if self.isDisabledForever() is True:
            return

        Mengine.changeCurrentAccountSetting(self.account_disable_setting_key, unicode(self.disable_key))
        Mengine.saveAccounts()  # then when observer triggers - we stop it (check __interstitialObserver)

    def isDisabledForever(self):
        return Mengine.getCurrentAccountSetting(self.account_disable_setting_key) == self.disable_key

    def __addObservers(self):
        def _setObserver(action, notificator):
            self.addObserver(notificator, self.__interstitialObserver, action=action)

        params = {
            "transition":
                ["onTransitionBegin", self.__cbTransitionBegin],
            "mg_reset":
                ["onEnigmaReset", None],
            "chapter_done":
                ["onGameComplete", None],
            "trigger":
                [SystemAdvertising.s_general_params["trigger"], self.__cbTriggerCount],
        }

        for action, (notificator_name, observer) in params.items():
            if self.isInterstitialParamEnable(action) is False:
                continue
            if Notificator.hasIdentity(notificator_name) is False:
                _Log("[{}] Not found notificator with name {!r}".format(action, notificator_name), err=True)
                continue

            notificator = Notificator.getIdentity(notificator_name)
            if observer is None:
                _setObserver(action, notificator)
            else:
                self.addObserver(notificator, observer, action=action)

    def __interstitialObserver(self, *args, **kwargs):
        if self.isDisabledForever() is True:
            return True

        if self.hasPermissionToViewAd(Mengine.getTime()) is False:
            return False

        action = kwargs.get("action")
        self.showInterstitial(descr=action)

        return False

    def __cbTransitionBegin(self, scene_from, scene_to, zoom_name, action=None):
        if SceneManager.isGameScene(scene_to) is False or scene_to in self.s_ignore_scenes:
            return False

        return self.__interstitialObserver(action=action)

    def __cbTriggerCount(self, *args, **kwargs):
        if self.isDisabledForever() is True:
            return True

        self._current_trigger_count += 1

        if self._current_trigger_count < self.s_general_params["trigger_count_show"]:
            return False

        self._current_trigger_count = 0

        self.showInterstitial(descr="trigger")
        return False