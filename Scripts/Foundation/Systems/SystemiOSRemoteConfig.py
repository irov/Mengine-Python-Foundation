from Foundation.System import System
from Foundation.Providers.RemoteConfigProvider import RemoteConfigProvider

PLUGIN_NAME = "iOSFirebaseRemoteConfigPlugin"

class SystemiOSRemoteConfig(System):
    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)

    @staticmethod
    def isPluginEnable():
        return SystemiOSRemoteConfig.is_plugin_active

    def _onInitialize(self):
        if self.isPluginEnable() is False:
            return

        RemoteConfigProvider.setProvider("Firebase", dict(
            getRemoteConfigValue=SystemiOSRemoteConfig.getRemoteConfigValue,
        ))

    def _onRun(self):
        return True

    @staticmethod
    def getRemoteConfigValue(key):
        """ returns dict value """
        return Mengine.iOSFirebaseRemoteConfigGetValue(key)
