from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Providers.RemoteConfigProvider import RemoteConfigProvider
from Foundation.SceneManager import SceneManager
from Foundation.DefaultManager import DefaultManager
from Foundation.PolicyManager import PolicyManager
from Foundation.DemonManager import DemonManager
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger

_Log = SimpleLogger("SystemAdvertising")
DEFAULT_IGNORE_SCENES = [
    "CutScene", "Menu", "Bonus", "SplashScreen", "Intro", "PreIntro",
    "DebugMenu", "Store", "Guides", "Map", "MapBonusChapter", "Options"
]
AD_TYPE = "Interstitial"


class SystemAdvertising(System):
    disable_key = "075ae3d2fc31640504f814f60e5ef713"
    account_disable_setting_key = "IsInterstitialDisabled"

    is_enable = False
    s_interstitial_params = {}
    s_general_params = {}

    s_ignore_scenes = []

    def __init__(self):
        super(SystemAdvertising, self).__init__()
        self._first_enter_timestamp = None
        self._start_delay_done = False
        self._last_view_timestamp = None
        self._current_trigger_count = 0
        self._no_permission_identity = None

    def _onInitialize(self):
        if Mengine.hasTouchpad() is False:
            return
        if Mengine.getConfigBool('Advertising', AD_TYPE, False) is False:
            return

        interstitial_params = {
            "transition": Mengine.getConfigBool('Advertising', "ShowOnTransition", False),
            "mg_reset": Mengine.getConfigBool('Advertising', "ShowOnResetMG", False),
            "transition_scene": Mengine.getConfigBool("Advertising", "OverrideTransitionScene", False),
            "chapter_done": Mengine.getConfigBool('Advertising', "ShowOnChapterDone", False),
            "trigger": Mengine.getConfigBool('Advertising', "ShowOnTrigger", False),
            "manual_trigger": Mengine.getConfigBool('Advertising', "ManualTrigger", False),
            # param for 'ShowOnTransition'. If true: check if scene is game scene
            "only_game_scenes": Mengine.getConfigBool('Advertising', "ShowOnlyOnGameScenes", True),
            # param for 'ShowOnTransition'. If true: always show ads on this scenes
            "only_specific_scenes": Mengine.getConfigBool('Advertising', "ShowOnlyOnSpecificScenes", False),
        }

        general_params = {
            "view_delay": Mengine.getConfigInt('Advertising', "ViewDelayInMinutes", 10) * 60,
            "delay_on_start": Mengine.getConfigInt('Advertising', "StartDelayInMinutes", 5) * 60,
            "trigger": Mengine.getConfigString('Advertising', "TriggerNotificatorName", ""),
            "trigger_count_start": Mengine.getConfigInt('Advertising', "TriggerCountStart", 0),
            "trigger_count_show": Mengine.getConfigInt('Advertising', "TriggerCountShow", 1),
            "scenes_to_view": Mengine.getConfigString('Advertising', "ScenesToView", "").split(", "),
            "ad_unit_name": Mengine.getConfigString('Advertising', "InterstitialSystemAdUnitName", AD_TYPE),
        }

        if Mengine.getConfigBool('Advertising', "NoPermissionsNotify", False) is True:
            no_permission_identity_name = Mengine.getConfigString('Advertising', "NoPermissionsIdentity", "")
            if Notificator.hasIdentity(no_permission_identity_name) is True:
                self._no_permission_identity = Notificator.getIdentity(no_permission_identity_name)

        self._current_trigger_count = general_params["trigger_count_start"]

        SystemAdvertising.s_ignore_scenes = DefaultManager.getDefaultTuple("InterstitialAdvertisingIgnoreScenes",
                                                                           default=DEFAULT_IGNORE_SCENES)

        SystemAdvertising.s_interstitial_params = interstitial_params
        SystemAdvertising.s_general_params = general_params
        SystemAdvertising.is_enable = True

        self._initDisableAccountParam()

    def _onRun(self):
        self._first_enter_timestamp = Mengine.getTime()

        if self.is_enable is True:
            self._onActivate()

        return True

    def _onActivate(self):
        self._updateWithRemoteConfig()
        self.__addObservers()
        self._setupAdvertisingTransitionScene()

    def _setupAdvertisingTransitionScene(self):
        if self.isInterstitialParamEnable("transition_scene") is False:
            return True

        advert_demon_name = DefaultManager.getDefault("AdvertisingDemonName", default="AdvertisingScene")

        if DemonManager.hasDemon(advert_demon_name) is False:
            Trace.log("System", 0, "Advertising demon {!r} not found - add or disable ShowOnAdvertisingScene config".format(advert_demon_name))
            return False

        transition_policy_name = DefaultManager.getDefault("AdvertisingTransitionPolicyName",
                                                           default="PolicyTransitionAdvertising")

        PolicyManager.setPolicy("Transition", transition_policy_name)
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
        ad_unit_name = self.getGeneralParam("ad_unit_name")

        def _cb(*args, **kwargs):
            _Log("show {}:{} advert using {} [action={!r}]".format(
                AD_TYPE, ad_unit_name, AdvertisementProvider.getName(), descr))
            self.updateViewedTime(Mengine.getTime())

        TaskManager.runAlias("AliasShowAdvert", _cb, AdType=AD_TYPE, AdUnitName=ad_unit_name)

    def isReadyToView(self):
        """ for manual check if interstitial is ready to view """
        if self.isInterstitialParamEnable("trigger") is True:
            return self.__checkTriggerCounter() is True
        else:
            return self._hasPermissionToViewAd(Mengine.getTime()) is True

    def _hasPermissionToViewAd(self, timestamp):
        ad_unit_name = self.getGeneralParam("ad_unit_name")

        if AdvertisementProvider.isAdvertAvailable(AD_TYPE, ad_unit_name) is False:
            return False

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
        if view_delay is None:
            Trace.log("System", 0, "view_delay is None (no -touchpad or config 'Advertising' 'Interstitial' is OFF)")
            return False

        if (timestamp - self._last_view_timestamp) > view_delay:
            return True
        return False

    def canViewAdOnScene(self, scene_name):
        if self.isInterstitialParamEnable("only_specific_scenes") is True:
            if scene_name not in self.getGeneralParam("scenes_to_view"):
                return False
            return True

        if self.isInterstitialParamEnable("only_game_scenes") is True and SceneManager.isGameScene(scene_name) is False:
            return False
        if scene_name in self.s_ignore_scenes:
            return False
        return True

    def _optionalNotifyNoPermission(self):
        if self._no_permission_identity is not None:
            Notification.notify(self._no_permission_identity)

    def updateViewedTime(self, timestamp):
        if _DEVELOPMENT is True:
            _seconds_passed = (timestamp - self._last_view_timestamp) if self._last_view_timestamp else None
            _Log("updateViewedTime to {} ({} seconds from last view)".format(timestamp, _seconds_passed))
        self._last_view_timestamp = timestamp

    def _initDisableAccountParam(self):
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

        advert_demon_name = DefaultManager.getDefault("AdvertisingDemonName", default="AdvertisingScene")
        advert_no_ads_key = DefaultManager.getDefault("AdvertisingDemonNoAdsKey", default="CacheNoAds")

        if DemonManager.hasDemon(advert_demon_name) is True:
            advert_demon = DemonManager.getDemon(advert_demon_name)
            if advert_demon.hasParam(advert_no_ads_key) is True:
                advert_demon.setParam(advert_no_ads_key, True)

    def isDisabledForever(self):
        if Mengine.hasCurrentAccountSetting(self.account_disable_setting_key) is False:
            return True
        return Mengine.getCurrentAccountSetting(self.account_disable_setting_key) == self.disable_key

    def __addObservers(self):
        self.addObserver(Notificator.onDisableInterstitialAds, self._cbDisableInterstitialAds)

        def _setObserver(action, notificator):
            self.addObserver(notificator, self.__interstitialObserver, action=action)

        params = {
            "transition":
                ["onTransitionBegin", self.__cbTransitionBegin],
            "mg_reset":
                ["onEnigmaReset", None],
            "chapter_done":
                ["onGameComplete", None]
        }
        if self.isInterstitialParamEnable("manual_trigger") is False:
            params["trigger"] = [SystemAdvertising.s_general_params["trigger"], self.__cbTriggerCount]

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

        if self._hasPermissionToViewAd(Mengine.getTime()) is False:
            self._optionalNotifyNoPermission()
            return False

        action = kwargs.get("action")
        self.showInterstitial(descr=action)

        return False

    def _cbDisableInterstitialAds(self):
        self.disableForever()
        return True

    def __cbTransitionBegin(self, scene_from, scene_to, zoom_name, action=None):
        if self.canViewAdOnScene(scene_to) is False:
            return False

        return self.__interstitialObserver(action=action)

    def __cbTriggerCount(self, *args, **kwargs):
        if self.isDisabledForever() is True:
            return True

        self.increaseTriggerCounter()
        if self.__checkTriggerCounter() is False:
            self._optionalNotifyNoPermission()
            return False

        ad_unit_name = self.getGeneralParam("ad_unit_name")
        if AdvertisementProvider.isAdvertAvailable(AD_TYPE, ad_unit_name) is False:
            self._optionalNotifyNoPermission()
            return False

        self.releaseTriggerCounter()
        return False

    def __checkTriggerCounter(self):
        """ returns True if trigger counter >= trigger_count_show """
        if self._current_trigger_count < self.getGeneralParam("trigger_count_show"):
            return False
        return True

    def increaseTriggerCounter(self):
        self._current_trigger_count += 1

    def releaseTriggerCounter(self):
        self._current_trigger_count = 0
        self.showInterstitial(descr="trigger")
        return True

    def _updateWithRemoteConfig(self):
        remote_params = RemoteConfigProvider.getRemoteConfigValueJSON("ad_interstitial_system", {})

        general_params = remote_params.get("general", {})
        for param, value in general_params.items():
            if param not in self.s_general_params:
                continue
            self.s_general_params[param] = value

        inter_params = remote_params.get("inter", {})
        for param, value in inter_params.items():
            if param not in self.s_interstitial_params:
                continue
            self.s_interstitial_params[param] = value

        return False
