from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Systems.SystemAndroidAd import SystemAndroidAd

_Log = SimpleLogger("SystemAndroidAdMob")

ANDROID_PLUGIN_NAME = "AndroidAdMobPlugin"

class SystemAndroidAdMob(SystemAndroidAd):
    """ Advertisement module 'AdMob' for Android """

    is_plugin_active = False
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        SystemAndroidAdMob.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        return SystemAndroidAdMob.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("AndroidAdMob", methods)
        Mengine.waitSemaphore("AdServiceReady", self.__onAdServiceReady)

    @staticmethod
    def isSdkInitialized():
        return SystemAndroidAdMob.is_sdk_init is True

    def __onAdServiceReady(self):
        SystemAndroidAdMob.is_sdk_init = self._androidBooleanMethod(ANDROID_PLUGIN_NAME, "isSdkInitialized")
        _Log("[AdService] ready, SDK initialized: {}".format(SystemAndroidAdMob.is_sdk_init))
        self._setAdServiceReady()
