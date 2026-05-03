from Foundation.System import System
from Foundation.Providers.RemoteConfigProvider import RemoteConfigProvider

PLUGIN_NAME = "AppleFirebaseRemoteConfigPlugin"

class SystemAppleRemoteConfig(System):
    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)

    @staticmethod
    def isPluginEnable():
        return SystemAppleRemoteConfig.is_plugin_active

    def _onInitialize(self):
        if self.isPluginEnable() is False:
            return

        RemoteConfigProvider.setProvider("Firebase", dict(
            getRemoteConfigValue=SystemAppleRemoteConfig.getRemoteConfigValue,
        ))

    def _onRun(self):
        return True

    @staticmethod
    def getRemoteConfigValue(key):
        """ returns dict value """
        return Mengine.appleFirebaseRemoteConfigGetValue(key)
