from Foundation.System import System
from Foundation.Providers.RemoteConfigProvider import RemoteConfigProvider


class SystemRemoteConfig(System):
    ANDROID_PLUGIN_NAME = "MengineFBRemoteConfig"
    APPLE_PLUGIN_NAME = "AppleFirebaseRemoteConfig"
    s_configs = {}

    @staticmethod
    def isPluginEnable():
        if _ANDROID:
            return Mengine.isAvailablePlugin(SystemRemoteConfig.ANDROID_PLUGIN_NAME) is True
        elif _IOS:
            return Mengine.isAvailablePlugin(SystemRemoteConfig.APPLE_PLUGIN_NAME) is True
        return False

    def _onInitialize(self):
        if self.isPluginEnable() is False:
            return

        RemoteConfigProvider.setProvider("Firebase", dict(
            getRemoteConfigValue=SystemRemoteConfig.getRemoteConfigValue,
        ))

    def _onRun(self):
        return True

    @staticmethod
    def getConfig(key, default=None, cast_to=None):     # DEPRECATED
        """
            returns config value and cast it to `cast_to` type if exists or `default`
        Args:
            key (str): lookup field
            default: default value if lookup field not exists
            cast_to (object|None): cast to input type or do nothing
        """
        Trace.msg_err("DEPRECATED, use getRemoteConfigValue<Type>({}) instead".format(key))

        if key not in SystemRemoteConfig.s_configs:
            return default
        else:
            raw = SystemRemoteConfig.s_configs[key]

            if callable(cast_to) is True:
                value = cast_to(raw)
            else:
                value = raw  # use default config type

            return value

    @staticmethod
    def getRemoteConfigValue(key):
        """ returns dict value """
        value = None
        if _ANDROID:
            value = Mengine.androidObjectMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValue", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValue(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS("getRemoteConfigValue")
        return value

    @staticmethod
    def __errorNotSupportedOS(caller_name):
        Trace.log("System", 0, "RemoteConfig {} do not work on this OS".format(caller_name))

