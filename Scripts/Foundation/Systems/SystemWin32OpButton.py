from Foundation.Systems.SystemNativeOpButton import SystemNativeOpButton


class SystemWin32OpButton(SystemNativeOpButton):
    PROVIDER_NAME = "Win32OpButton"

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin("Win32OpButton")
