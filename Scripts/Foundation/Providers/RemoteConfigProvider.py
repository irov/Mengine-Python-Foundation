from Foundation.Providers.BaseProvider import BaseProvider


class RemoteConfigProvider(BaseProvider):
    s_allowed_methods = [
        "getRemoteConfigValue",
    ]

    @staticmethod
    def getRemoteConfigValue(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValue", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def __returnValueOrDefault(value, default):
        if value is not None:
            return value
        return default
