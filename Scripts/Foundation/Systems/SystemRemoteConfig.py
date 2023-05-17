from Foundation.System import System

class SystemRemoteConfig(System):
    PLUGIN_NAME = "FirebaseRemoteConfig"
    s_configs = {}

    @staticmethod
    def isPluginEnable():
        return _PLUGINS.get(SystemRemoteConfig.PLUGIN_NAME, False) is True

    def _onInitialize(self):
        if self.isPluginEnable():
            SystemRemoteConfig.s_configs = self._getRemoteConfig()

    def _onRun(self):
        for key, value in SystemRemoteConfig.s_configs.items():
            Notification.notify(Notificator.onGetRemoteConfig, key, value)
        return True

    @staticmethod
    def getConfig(key, default=None, cast_to=None):
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
        if SystemRemoteConfig.isPluginEnable() is False:
            Trace.log("System", 0, "'{}' is not enable to fetch remote config".format(SystemRemoteConfig.PLUGIN_NAME))
            return {}

        config = {}

        if _ANDROID:
            config = Mengine.androidObjectMethod(SystemRemoteConfig.PLUGIN_NAME, "getRemoteConfig")
        else:
            Trace.log("System", 0, "'{}' do not work on this OS".format(SystemRemoteConfig.PLUGIN_NAME))

        return config