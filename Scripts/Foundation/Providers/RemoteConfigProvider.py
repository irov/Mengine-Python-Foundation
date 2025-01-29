from Foundation.Providers.BaseProvider import BaseProvider


class RemoteConfigProvider(BaseProvider):
    s_allowed_methods = [
        "getRemoteConfigValueJSON",
    ]

    @staticmethod
    def getRemoteConfigValueJSON(key, default=None):
        remote_value = RemoteConfigProvider._call("getRemoteConfigValueJSON", key)
        return RemoteConfigProvider.__returnValueOrDefault(remote_value, default)

    @staticmethod
    def __returnValueOrDefault(value, default):
        if value is not None:
            return value
        return default
