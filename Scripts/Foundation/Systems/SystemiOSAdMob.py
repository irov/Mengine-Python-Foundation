from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Systems.SystemiOSAd import SystemiOSAd

_Log = SimpleLogger("SystemiOSAdMob")

PLUGIN_NAME = "iOSAdMobPlugin"

class SystemiOSAdMob(SystemiOSAd):
    """ Advertisement module 'AdMob' for iOS """

    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        return SystemiOSAdMob.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("iOSAdMob", methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemiOSAdMob.is_sdk_init is True

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAdMobPluginOnSdkInitialized")
        SystemiOSAdMob.is_sdk_init = True
        self._setAdServiceReady()
