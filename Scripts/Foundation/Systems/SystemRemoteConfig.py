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

        SystemRemoteConfig.s_configs = self._getRemoteConfig()
        Trace.msg_dev("* SystemRemoteConfig config: %s" % SystemRemoteConfig.s_configs)

        RemoteConfigProvider.setProvider("Firebase", dict(
            getRemoteConfigValueString=SystemRemoteConfig.getRemoteConfigValueString,
            getRemoteConfigValueBoolean=SystemRemoteConfig.getRemoteConfigValueBoolean,
            getRemoteConfigValueFloat=SystemRemoteConfig.getRemoteConfigValueFloat,
            getRemoteConfigValueInt=SystemRemoteConfig.getRemoteConfigValueInt,
            getRemoteConfigValueJSON=SystemRemoteConfig.getRemoteConfigValueJSON,
        ))

    def _onRun(self):
        def _releaseRemoteConfig():
            for key, value in SystemRemoteConfig.s_configs.items():
                Notification.notify(Notificator.onGetRemoteConfig, key, value)

        with self.createTaskChain(Name="RemoteConfig") as tc:
            tc.addListener(Notificator.onRun)
            tc.addFunction(_releaseRemoteConfig)
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
    def _getRemoteConfig():
        """ returns all remote configs, all values are strings (!) """

        if SystemRemoteConfig.isPluginEnable() is False:
            Trace.log("System", 0, "Plugin RemoteConfig is not enable to fetch remote config")
            return {}

        config = {}

        if _ANDROID:
            config = Mengine.androidObjectMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfig")
        elif _IOS:
            config = Mengine.appleGetRemoteConfig()
        else:
            SystemRemoteConfig.__errorNotSupportedOS()

        return config

    @staticmethod
    def getRemoteConfigValueString(key):
        """ returns str value """
        value = None
        if _ANDROID:
            value = Mengine.androidStringMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValueString", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValueConstString(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS()
        return value

    @staticmethod
    def getRemoteConfigValueBoolean(key):
        """ returns bool value """
        value = None
        if _ANDROID:
            value = Mengine.androidBooleanMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValueBoolean", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValueBoolean(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS()
        return value

    @staticmethod
    def getRemoteConfigValueInt(key):
        """ returns int value """
        value = None
        if _ANDROID:
            value = Mengine.androidLongMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValueLong", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValueInteger(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS()
        return value

    @staticmethod
    def getRemoteConfigValueFloat(key):
        """ returns float value """
        value = None
        if _ANDROID:
            value = Mengine.androidDoubleMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValueDouble", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValueDouble(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS()
        return value

    @staticmethod
    def getRemoteConfigValueJSON(key):
        """ returns dict value """
        value = None
        if _ANDROID:
            value = Mengine.androidObjectMethod(SystemRemoteConfig.ANDROID_PLUGIN_NAME, "getRemoteConfigValueLong", key)
        elif _IOS:
            value = Mengine.appleFirebaseRemoteConfigGetValueJSON(key)
        else:
            SystemRemoteConfig.__errorNotSupportedOS()
        return value

    @staticmethod
    def __errorNotSupportedOS():
        Trace.log("System", 0, "RemoteConfig do not work on this OS")

