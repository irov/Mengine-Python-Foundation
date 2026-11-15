from Foundation.Systems.SystemNativeOpButton import SystemNativeOpButton


class SystemiOSOpButton(SystemNativeOpButton):
    PROVIDER_NAME = "iOSOpButton"

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin("iOSOpButtonPlugin")
