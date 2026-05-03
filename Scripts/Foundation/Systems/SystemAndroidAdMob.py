from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Systems.SystemAndroidAd import SystemAndroidAd

_Log = SimpleLogger("SystemAndroidAdMob")

PLUGIN_NAME = "AndroidAdMobPlugin"

class SystemAndroidAdMob(SystemAndroidAd):
    """ Advertisement module 'AdMob' for Android """

    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        return SystemAndroidAdMob.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("AndroidAdMob", methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemAndroidAdMob.is_sdk_init is True

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAdMobPluginOnSdkInitialized")
        SystemAndroidAdMob.is_sdk_init = True
        self._setAdServiceReady()