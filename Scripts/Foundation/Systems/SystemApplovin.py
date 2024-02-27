from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemApplovin")
CREDENTIALS_CONFIG_KEY = "AppLovinPlugin"
ANDROID_PLUGIN_NAME = "MengineAppLovin"
APPLE_PLUGIN_NAME = "AppleAppLovin"
APPLE_METHODS_PREFIX = "appleAppLovin"
DEVDEBUGGER_TAB_NAME = "Applovin"


def ad_callback(bound_method):
    if _ANDROID:
        # I add callback, that returns an `ad_unit_id` as first argument
        def cb_wrapper(self, ad_unit_id, *args, **kwargs):
            if ad_unit_id != self.ad_unit_id:
                return
            return bound_method(self, *args, **kwargs)
    elif _IOS:
        # each callback is bounded to a specific ad unit
        def cb_wrapper(self, *args, **kwargs):
            return bound_method(self, *args, **kwargs)
    else:
        def cb_wrapper(self, *args, **kwargs):
            return bound_method(self, *args, **kwargs)
    return cb_wrapper


def _addAndroidCallback(self, name, cb):
    if name in self._cbs:
        Trace.log("System", 0, "[{}:{}] android callback {!r} already exists !!!".format(self.ad_type, self.name, name))
        Mengine.removeAndroidCallback(ANDROID_PLUGIN_NAME, self.s_callbacks, self._cbs[name])
    identity = Mengine.addAndroidCallback(ANDROID_PLUGIN_NAME, self.s_callbacks[name], cb)
    self._cbs[name] = identity
    return identity


class ApplovinMengineProvider(object):
    if _ANDROID:
        @staticmethod
        def call(func_name, *args, **kwargs):
            if kwargs.get("type") == "bool":
                return Mengine.androidBooleanMethod(ANDROID_PLUGIN_NAME, func_name, *args)
            else:
                return Mengine.androidMethod(ANDROID_PLUGIN_NAME, func_name, *args)

    elif _IOS:
        @staticmethod
        def call(func_name, *args, **kwargs):
            full_func_name = APPLE_METHODS_PREFIX + str(func_name)
            func = getattr(Mengine, full_func_name)

            if func is None:
                Trace.log("System", 0, "Apple applovin method {!r} - not found in Mengine".format(full_func_name))
                return False

            return func(*args)

    else:
        @staticmethod
        def call(func_name, *args, **kwargs):
            Trace.log("System", 0, "!!!! No provider for method {!r} [args: {}]".format(func_name, args))
            return False


class SystemApplovin(System):
    """ Advertisement module 'Applovin' """

    class AdUnitMixin(object):
        ad_type = None
        s_callbacks = {
            "onAdDisplayed": None,
            "onAdDisplayFailed": None,
            "onAdClicked": None,
            "onAdHidden": None,
        }
        s_methods = {
            "init": None,
            "show": None,
            "can_offer": None,
            "is_available": None,
        }

        def _hasMethod(self, name):
            return self.s_methods.get(name) is not None

        def __init__(self, name):
            self._cbs = {}
            self.inited = False
            self.display = False
            self.name = name    # placement
            self.ad_unit_id = Mengine.getConfigString(CREDENTIALS_CONFIG_KEY, "%sAdUnitId" % self.name, "")

        def setCallbacks(self):
            if _ANDROID:
                _addAndroidCallback(self, "onAdDisplayed", self.cbDisplaySuccess)
                _addAndroidCallback(self, "onAdDisplayFailed", self.cbDisplayFailed)
                _addAndroidCallback(self, "onAdClicked", self.cbClicked)
                _addAndroidCallback(self, "onAdHidden", self.cbHidden)
            elif _IOS:
                # we set callbacks in init for provider
                callbacks = {
                    self.s_callbacks["onAdDisplayed"]: self.cbDisplaySuccess,
                    self.s_callbacks["onAdDisplayFailed"]: self.cbDisplayFailed,
                    self.s_callbacks["onAdClicked"]: self.cbClicked,
                    self.s_callbacks["onAdHidden"]: self.cbHidden,
                }
                return callbacks

        def init(self):
            if bool(Mengine.getConfigBool('Advertising', self.ad_type, False)) is False:
                return False
            if self.ad_unit_id == "":
                _Log("[{}] call init failed: ad unit id is not configured or wrong ({})!".format(self.name, self.ad_unit_id), err=True, force=True)
                return False

            _Log("[{}] call init".format(self.name))
            self._initialize()

            self.inited = True

            return True

        def _initialize(self):
            if _IOS:
                callbacks = self.setCallbacks()
                ApplovinMengineProvider.call(self.s_methods["init"], self.ad_unit_id, callbacks)
            elif _ANDROID:
                ApplovinMengineProvider.call(self.s_methods["init"], self.ad_unit_id, type="bool")
            else:
                Trace.log("System", 0, "initialize fail: Unsupported platform")

        def cleanUp(self):
            if _ANDROID:
                for name, cb_id in self._cbs.items():
                    Mengine.removeAndroidCallback(ANDROID_PLUGIN_NAME, self.s_callbacks[name], cb_id)
                self._cbs = {}
            elif _IOS:
                pass    # auto remove

        def canOffer(self):
            """ Call this method only once when you create rewarded button """
            status = False

            if self._hasMethod("can_offer") is False:
                _Log("[{}:{}] available to offer is {} - no method to check!!"
                     .format(self.ad_type, self.name, status), err=True, force=True)
                return status

            status = ApplovinMengineProvider.call(self.s_methods["can_offer"],
                                                  self.ad_unit_id, self.getPlacementName(), type="bool")
            _Log("[{}:{}] available to offer is {}".format(self.ad_type, self.name, status))

            return status

        def isAvailable(self):
            """ Call this method if you 100% will show ad, but want to do something before show """
            status = False

            if self._hasMethod("is_available") is False:
                _Log("[{}:{}] available to show is {} - no method to check!!"
                     .format(self.ad_type, self.name, status), err=True, force=True)
                return status

            status = ApplovinMengineProvider.call(self.s_methods["is_available"],
                                                  self.ad_unit_id, self.getPlacementName(), type="bool")
            _Log("[{}:{}] available to show is {}".format(self.ad_type, self.name, status))

            return status

        def show(self):
            status = False

            if self.__checkInit() is False:
                self._cbDisplayFailed()
                return status

            _Log("[{}:{}] show advertisement...".format(self.ad_type, self.name))

            if self._hasMethod("show") is True:
                status = ApplovinMengineProvider.call(self.s_methods["show"],
                                                      self.ad_unit_id, self.getPlacementName(), type="bool")

            if status is False:
                self._cbDisplayFailed()

            return status

        # utils

        def __checkInit(self, init_if_no=False):
            """ returns True if ad inited else False
                @param init_if_no: if True - tries to init """

            if self.ad_unit_id is None:
                return False

            if self.inited is True:
                return True
            err_msg = "Applovin ad [{}:{}:{}] not inited".format(self.ad_type, self.name, self.ad_unit_id)

            if init_if_no is True:
                err_msg += ". Try init..."
                status = self.init()
                err_msg += " Status {}".format(status)

            _Log(err_msg, err=True, force=True)
            return False

        def getPlacementName(self):
            return self.name

        # callbacks

        @ad_callback
        def cbDisplaySuccess(self):
            self._cbDisplaySuccess()

        def _cbDisplaySuccess(self):
            self.display = True
            Notification.notify(Notificator.onAdvertDisplayed, self.ad_type, self.name)
            _Log("[{} cb] displayed".format(self.name))

        @ad_callback
        def cbDisplayFailed(self):
            self._cbDisplayFailed()

        def _cbDisplayFailed(self):
            Notification.notify(Notificator.onAdvertDisplayFailed, self.ad_type, self.name)
            _Log("[{} cb] !!! display failed".format(self.name), err=True, force=True)

        @ad_callback
        def cbHidden(self):
            self._cbHidden()

        def _cbHidden(self):
            self.display = False
            Notification.notify(Notificator.onAdvertHidden, self.ad_type, self.name)
            _Log("[{} cb] hidden".format(self.name))

        @ad_callback
        def cbClicked(self):
            self._cbClicked()

        def _cbClicked(self):
            Notification.notify(Notificator.onAdvertClicked, self.ad_type, self.name)
            _Log("[{} cb] clicked".format(self.name))

        # devtodebug

        def _getDevToDebugWidgets(self):
            widgets = []

            # descr widget

            is_enable = bool(Mengine.getConfigBool('Advertising', self.ad_type, False))

            def _getDescr():
                text = "### [{}] {}".format(self.ad_type, self.name)
                text += "\nenable in configs.json: `{}`".format(is_enable)
                text += "\ninited: `{}`".format(self.inited)
                return text

            w_descr = Mengine.createDevToDebugWidgetText(self.name + "_descr")
            w_descr.setText(_getDescr)
            widgets.append(w_descr)

            # button widgets

            methods = {"init": self.init, "show": self.show, }
            for key, method in methods.items():
                w_btn = Mengine.createDevToDebugWidgetButton(self.name + "_" + key)
                w_btn.setTitle(key)
                w_btn.setClickEvent(method)
                widgets.append(w_btn)

            return widgets

    class InterstitialAd(AdUnitMixin):
        """ player is obligated to watch these ads """

        ad_type = "Interstitial"
        if _ANDROID:
            s_callbacks = {
                "onAdDisplayed": "onAppLovinInterstitialOnAdDisplayed",
                "onAdDisplayFailed": "onAppLovinInterstitialOnAdDisplayFailed",
                "onAdClicked": "onAppLovinInterstitialOnAdClicked",
                "onAdHidden": "onAppLovinInterstitialOnAdHidden",
            }
            s_methods = {
                "init": "initInterstitial",
                "show": "showInterstitial",
                "is_available": "canYouShowInterstitial",
            }
        elif _IOS:
            s_callbacks = {
                "onAdDisplayed": "onAppleAppLovinInterstitialDidDisplayAd",
                "onAdDisplayFailed": "onAppleAppLovinInterstitialDidFailToDisplayAd",
                "onAdClicked": "onAppleAppLovinInterstitialDidClickAd",
                "onAdHidden": "onAppleAppLovinInterstitialDidHideAd",
                # onAppleAppLovinInterstitialDidStartAdRequestForAdUnitIdentifier
                # onAppleAppLovinInterstitialDidLoadAd
                # onAppleAppLovinInterstitialDidFailToLoadAdForAdUnitIdentifier
                # onAppleAppLovinInterstitialDidPayRevenueForAd
            }
            s_methods = {
                "init": "InitInterstitial",
                "show": "ShowInterstitial",
                "is_available": "CanYouShowInterstitial",
            }

    class RewardedAd(AdUnitMixin):
        """ player could watch ad without skip and get reward after full view """

        ad_type = "Rewarded"
        if _ANDROID:
            s_callbacks = {
                "onAdDisplayed": "onAppLovinRewardedOnAdDisplayed",
                "onAdDisplayFailed": "onAppLovinRewardedOnAdDisplayFailed",
                "onAdClicked": "onAppLovinRewardedOnAdClicked",
                "onAdHidden": "onAppLovinRewardedOnAdHidden",
                "onUserRewarded": "onAppLovinRewardedOnUserRewarded",
            }
            s_methods = {
                "init": "initRewarded",
                "show": "showRewarded",
                "can_offer": "canOfferRewarded",
                "is_available": "canYouShowRewarded",
            }
        elif _IOS:
            s_callbacks = {
                "onAdDisplayed": "onAppleAppLovinRewardedDidDisplayAd",
                "onAdDisplayFailed": "onAppleAppLovinRewardedDidFailToDisplayAd",
                "onAdClicked": "onAppleAppLovinRewardedDidClickAd",
                "onAdHidden": "onAppleAppLovinRewardedDidHideAd",
                "onUserRewarded": "onAppleAppLovinRewardedDidRewardUserForAd",
                # onAppleAppLovinRewardedDidStartAdRequestForAdUnitIdentifier
                # onAppleAppLovinRewardedDidLoadAd
                # onAppleAppLovinRewardedDidFailToLoadAdForAdUnitIdentifier
                # onAppleAppLovinRewardedDidStartRewardedVideoForAd
                # onAppleAppLovinRewardedDidCompleteRewardedVideoForAd
                # onAppleAppLovinRewardedDidPayRevenueForAd
            }
            s_methods = {
                "init": "InitRewarded",
                "show": "ShowRewarded",
                "can_offer": "CanOfferRewarded",
                "is_available": "CanYouShowRewarded",
            }

        def __init__(self, name):
            super(self.__class__, self).__init__(name)
            self.rewarded = False

        def setCallbacks(self):
            if _ANDROID:
                super(self.__class__, self).setCallbacks()
                _addAndroidCallback(self, "onUserRewarded", self.cbUserRewarded)
            elif _IOS:
                callbacks = super(self.__class__, self).setCallbacks()
                callbacks[self.s_callbacks["onUserRewarded"]] = self.cbUserRewarded   # noqa
                return callbacks

        @ad_callback
        def cbUserRewarded(self, label="", reward=1):
            self._cbUserRewarded(label, reward)

        def _cbUserRewarded(self, label, reward):
            self.rewarded = True
            Notification.notify(Notificator.onAdvertRewarded, self.name, label, reward)
            _Log("[{} cb] user rewarded: label={!r}, amount={!r}".format(self.name, label, reward))

        def _cbDisplaySuccess(self):
            self.rewarded = False
            super(self.__class__, self)._cbDisplaySuccess()

        def _cbHidden(self):
            if self.rewarded is False:
                Notification.notify(Notificator.onAdvertSkipped, self.ad_type, self.name)
                _Log("[{} cb] advert {!r} was skipped".format(self.ad_type, self.name))
            super(self.__class__, self)._cbHidden()

    class Banner(AdUnitMixin):
        ad_type = "Banner"
        if _ANDROID:
            s_callbacks = {
                "onAdDisplayed": "onAppLovinBannerOnAdDisplayed",
                "onAdDisplayFailed": "onAppLovinBannerOnAdDisplayFailed",
                "onAdHidden": "onAppLovinBannerOnAdHidden",
                "onAdClicked": "onAppLovinBannerOnAdClicked",
                "onAdExpanded": "onAppLovinBannerOnAdExpanded",
                "onAdCollapsed": "onAppLovinBannerOnAdCollapsed",
                # onAppLovinBannerOnAdLoadFailed
            }
            s_methods = {
                "init": "initBanner",
                "show": "bannerVisible",
                "hide": "bannerVisible",
            }
        elif _IOS:
            s_callbacks = {
                "onAdDisplayed": "onAppleAppLovinInterstitialDidDisplayAd",
                "onAdDisplayFailed": "onAppleAppLovinBannerDidFailToDisplayAd",
                "onAdClicked": "onAppleAppLovinBannerDidClickAd",
                # onAdHidden empty
                "onAdExpanded": "onAppleAppLovinBannerDidExpandAd",
                "onAdCollapsed": "onAppleAppLovinBannerDidCollapseAd",
                # onAppleAppLovinBannerDidStartAdRequestForAdUnitIdentifier
                # onAppleAppLovinBannerDidLoadAd
                # onAppleAppLovinBannerDidFailToLoadAdForAdUnitIdentifier
                # onAppleAppLovinBannerDidPayRevenueForAd
            }
            s_methods = {
                "init": "InitBanner",
                "show": "ShowBanner",
                "hide": "HideBanner",
            }

        def __init__(self, name):
            super(self.__class__, self).__init__(name)
            self.hidden = True

        def _initialize(self):
            if _IOS:
                callbacks = self.setCallbacks()
                ApplovinMengineProvider.call(self.s_methods["init"], self.ad_unit_id, self.getPlacementName(), callbacks)
            elif _ANDROID:
                ApplovinMengineProvider.call(self.s_methods["init"], self.ad_unit_id, self.getPlacementName(), type="bool")
            else:
                Trace.log("System", 0, "initialize fail: Unsupported platform")

        def show(self):
            if self.hidden is False:
                _Log("Banner {!r} is already shown!!".format(self.name), err=True)
                # return True

            if _ANDROID:
                state = True
                result = ApplovinMengineProvider.call(self.s_methods["show"], self.ad_unit_id, state, type="bool")
            else:
                result = ApplovinMengineProvider.call(self.s_methods["show"], self.ad_unit_id)

            return result

        def hide(self):
            if self.hidden is True:
                _Log("Banner {!r} is already hidden!!".format(self.name), err=True)
                # return True

            if _ANDROID:
                state = False
                result = ApplovinMengineProvider.call(self.s_methods["hide"], self.ad_unit_id, state, type="bool")
            else:
                result = ApplovinMengineProvider.call(self.s_methods["hide"], self.ad_unit_id)

            return result

        def setCallbacks(self):
            if _ANDROID:
                _addAndroidCallback(self, "onAdDisplayed", self.cbDisplaySuccess)
                _addAndroidCallback(self, "onAdDisplayFailed", self.cbDisplayFailed)
                _addAndroidCallback(self, "onAdClicked", self.cbClicked)
                _addAndroidCallback(self, "onAdHidden", self.cbHidden)
                _addAndroidCallback(self, "onAdExpanded", self.cbExpanded)
                _addAndroidCallback(self, "onAdCollapsed", self.cbCollapsed)
            elif _IOS:
                # we set callbacks in init for provider
                callbacks = {
                    self.s_callbacks["onAdDisplayed"]: self.cbDisplaySuccess,
                    self.s_callbacks["onAdDisplayFailed"]: self.cbDisplayFailed,
                    self.s_callbacks["onAdClicked"]: self.cbClicked,
                    self.s_callbacks["onAdExpanded"]: self.cbExpanded,
                    self.s_callbacks["onAdCollapsed"]: self.cbCollapsed,
                }
                return callbacks

        @ad_callback
        def cbExpanded(self):
            self._cbExpanded()

        def _cbExpanded(self):
            _Log("[{} cb] {} was expanded".format(self.ad_type, self.name))

        @ad_callback
        def cbCollapsed(self):
            self._cbCollapsed()

        def _cbCollapsed(self):
            _Log("[{} cb] {} was collapsed".format(self.ad_type, self.name))

    # ------------------------------------------------------------------------------------------------------------------

    is_plugin_active = False
    is_sdk_init = False

    def __init__(self):
        super(SystemApplovin, self).__init__()
        self.interstitials = {}
        self.rewardeds = {}
        self.banners = {}

    def _onInitialize(self):
        if _ANDROID:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        elif _IOS:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)

        if self.is_plugin_active is False:
            return

        init_params = [
            ["RewardedUnitNames", ["Rewarded"], self.rewardeds, SystemApplovin.RewardedAd],
            ["InterstitialUnitNames", ["Interstitial"], self.interstitials, SystemApplovin.InterstitialAd],
            ["BannerUnitNames", ["Banner"], self.banners, SystemApplovin.Banner],
        ]

        for config_key, default_values, storage, Type in init_params:
            if Mengine.getConfigBool("Advertising", Type.ad_type, False) is False:
                # this ad type is not active - enable in Configs.json
                continue

            unit_names = Mengine.getConfigStrings("Advertising", config_key)
            if len(unit_names) == 0:
                unit_names = default_values

            for name in unit_names:
                if name in storage:
                    _Log("Duplicate name {} in {}".format(name, Type.ad_type), err=True)
                    continue

                ad_unit = Type(name)
                storage[name] = ad_unit

        for ad_unit in self._getAllAdUnits():
            ad_unit.setCallbacks()

        Mengine.waitSemaphore("AppLovinSdkInitialized", self.__cbSdkInitialized)

        # ads do init in `__cbSdkInitialized`
        self.__addDevToDebug()

    def _onFinalize(self):
        for ad_unit in self._getAllAdUnits():
            ad_unit.cleanUp()
        self.rewardeds = None
        self.interstitials = None
        self.banners = None

    # utils

    def initAds(self):
        for ad_unit in self._getAllAdUnits():
            if ad_unit.init() is False:
                Trace.log("System", 0, "Failed to init advert [{}:{}]".format(ad_unit.ad_type, ad_unit.name))

        provider_methods = dict(
            ShowRewardedAdvert=Functor(self.showAdvert, self.rewardeds),
            ShowInterstitialAdvert=Functor(self.showAdvert, self.interstitials),
            CanOfferRewardedAdvert=Functor(self.canOfferAdvert, self.rewardeds),
            IsRewardedAdvertAvailable=Functor(self.isAdvertAvailable, self.rewardeds),
            IsInterstitialAdvertAvailable=Functor(self.isAdvertAvailable, self.interstitials),
            ShowBanner=Functor(self.showAdvert, self.banners),
            HideBanner=Functor(self.hideBanner, self.banners),
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )
        AdvertisementProvider.setProvider(ANDROID_PLUGIN_NAME, provider_methods)

    @staticmethod
    def isSdkInitialized():
        return SystemApplovin.is_sdk_init is True

    @staticmethod
    def showMediationDebugger():
        if _ANDROID:
            Mengine.androidMethod(ANDROID_PLUGIN_NAME, "showMediationDebugger")
        elif _IOS:
            Mengine.appleAppLovinShowMediationDebugger()

    def showConsentFlow(self):
        if _ANDROID:
            Mengine.androidMethod(ANDROID_PLUGIN_NAME, "showConsentFlow")
        elif _IOS:
            Mengine.appleAppLovinLoadAndShowCMPFlow({
                "onAppleAppLovinConsentFlowShowSuccessful": self.__cbConsentFlowShowSuccessful,
                "onAppleAppLovinConsentFlowShowFailed": self.__cbConsentFlowShowFailed,
            })

    def isConsentFlow(self):
        if _ANDROID:
            return Mengine.androidBooleanMethod(ANDROID_PLUGIN_NAME, "isConsentFlowUserGeographyGDPR")
        elif _IOS:
            return Mengine.appleAppLovinIsConsentFlowUserGeographyGDPR()
        return False

    def _getAllAdUnits(self):
        return self.rewardeds.values() + self.interstitials.values() + self.banners.values()

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemApplovin.is_sdk_init = True
        self.initAds()

        self.__disableDevToDebugInitButton()

    def __cbConsentFlowShowSuccessful(self):
        _Log("[cb] Consent Flow Show Successful")

    def __cbConsentFlowShowFailed(self):
        _Log("[cb] Consent Flow Show Failed", err=True, force=True)

    # provider handling

    def showAdvert(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for showAdvert in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.show()

    def canOfferAdvert(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for canOfferAdvert in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.canOffer()

    def isAdvertAvailable(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for isAdvertAvailable in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.isAvailable()

    def hideBanner(self, ad_unit_name, banners_dict):
        banner = banners_dict.get(ad_unit_name)
        if banner is None:
            Trace.log("System", 0, "Banner {!r} not found for hideBanner in {}".format(
                ad_unit_name, banners_dict.keys()))
            return False
        return banner.hide()

    # debug

    def __disableDevToDebugInitButton(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is False:
            return

        tab = Mengine.getDevToDebugTab(DEVDEBUGGER_TAB_NAME)
        widget = tab.findWidget("run_init")
        if widget:
            widget.setHide(True)

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if self.is_plugin_active is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is True:
            return

        tab = Mengine.addDevToDebugTab(DEVDEBUGGER_TAB_NAME)
        widgets = []

        if self.is_sdk_init is False and _ANDROID:
            w_init = Mengine.createDevToDebugWidgetButton("run_init")
            w_init.setTitle("Run init applovin")
            w_init.setClickEvent(Mengine.androidMethod, ANDROID_PLUGIN_NAME, "initialize")
            widgets.append(w_init)

        w_debug = Mengine.createDevToDebugWidgetButton("show_mediation_debugger")
        w_debug.setTitle("Show Mediation Debugger")
        w_debug.setClickEvent(self.showMediationDebugger)
        widgets.append(w_debug)

        w_consent = Mengine.createDevToDebugWidgetButton("show_consent_flow")
        w_consent.setTitle("Show Consent Flow (isConsentFlow={})".format(self.isConsentFlow()))
        w_consent.setClickEvent(self.showConsentFlow)
        widgets.append(w_consent)

        for ad_unit in self._getAllAdUnits():
            widgets.extend(ad_unit._getDevToDebugWidgets())

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is False:
            return

        Mengine.removeDevToDebugTab(DEVDEBUGGER_TAB_NAME)
