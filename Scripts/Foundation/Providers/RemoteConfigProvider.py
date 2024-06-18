from Foundation.Providers.BaseProvider import BaseProvider


class RemoteConfigProvider(BaseProvider):
    s_allowed_methods = [
        "getRemoteConfigValueString",
        "getRemoteConfigValueBoolean",
        "getRemoteConfigValueFloat",
        "getRemoteConfigValueInt",
        "getRemoteConfigValueJSON",
    ]

    @staticmethod
    def getRemoteConfigValueString(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueString", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def getRemoteConfigValueBoolean(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueBoolean", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def getRemoteConfigValueFloat(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueFloat", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def getRemoteConfigValueInt(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueInt", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def getRemoteConfigValueJSON(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueJSON", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def __returnValueOrDefault(value, default):
        if value is not None:
            return value
        return default
