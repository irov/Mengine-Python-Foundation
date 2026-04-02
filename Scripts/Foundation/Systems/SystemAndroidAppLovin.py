from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Providers.ConsentProvider import ConsentProvider
from Foundation.Systems.SystemAndroidAd import SystemAndroidAd

_Log = SimpleLogger("SystemAndroidAppLovin")

ANDROID_PLUGIN_NAME = "AndroidAppLovinPlugin"


class SystemAndroidAppLovin(SystemAndroidAd):
    """ Advertisement module 'AppLovin' for Android """

    is_plugin_active = False
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        SystemAndroidAppLovin.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        return SystemAndroidAppLovin.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("AndroidAppLovin", methods)

        consent_methods = dict(
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )

        ConsentProvider.setProvider("AndroidAppLovin", consent_methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemAndroidAppLovin.is_sdk_init is True

    def showConsentFlow(self):
        self._androidMethod(ANDROID_PLUGIN_NAME, "showConsentFlow")

    def isConsentFlow(self):
        return self._androidBooleanMethod(ANDROID_PLUGIN_NAME, "isConsentFlowUserGeographyGDPR")

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemAndroidAppLovin.is_sdk_init = True
        self._setAdServiceReady()
