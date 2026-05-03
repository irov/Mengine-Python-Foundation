from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Systems.SystemAppleAd import SystemAppleAd

_Log = SimpleLogger("SystemAppleAdMob")

PLUGIN_NAME = "AppleAdMobPlugin"

class SystemAppleAdMob(SystemAppleAd):
    """ Advertisement module 'AdMob' for iOS """

    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        return SystemAppleAdMob.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("AppleAdMob", methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemAppleAdMob.is_sdk_init is True

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAdMobPluginOnSdkInitialized")
        SystemAppleAdMob.is_sdk_init = True
        self._setAdServiceReady()