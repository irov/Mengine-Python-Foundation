from Foundation.System import System
from Foundation.Providers.RemoteConfigProvider import RemoteConfigProvider

PLUGIN_NAME = "AndroidFBRemoteConfigPlugin"

class SystemAndroidRemoteConfig(System):
    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)

    @staticmethod
    def isPluginEnable():
        return SystemAndroidRemoteConfig.is_plugin_active

    def _onInitialize(self):
        if self.isPluginEnable() is False:
            return

        RemoteConfigProvider.setProvider("Firebase", dict(
            getRemoteConfigValue=SystemAndroidRemoteConfig.getRemoteConfigValue,
        ))

    def _onRun(self):
        return True

    @staticmethod
    def getRemoteConfigValue(key):
        """ returns dict value """
        return Mengine.androidObjectMethod(PLUGIN_NAME, "getRemoteConfigValue", key)
