from Foundation.Providers.LocalNotificationsProvider import LocalNotificationsProvider
from Foundation.System import System

PROVIDER_NAME = "iOSUserNotificationCenter"
PLUGIN_NAME = "iOSUserNotificationCenterPlugin"


class SystemiOSUserNotificationCenter(System):
    """ Local notifications module for iOS (UNUserNotificationCenter) """

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemiOSUserNotificationCenter, self)._onInitialize()

        methods = dict(setNotificationDelay=SystemiOSUserNotificationCenter.setNotificationDelay)
        LocalNotificationsProvider.setProvider(PROVIDER_NAME, methods)

    def _onFinalize(self):
        super(SystemiOSUserNotificationCenter, self)._onFinalize()

        if LocalNotificationsProvider.getName() == PROVIDER_NAME:
            LocalNotificationsProvider.removeProvider()

    @staticmethod
    def setNotificationDelay(name, seconds):
        Mengine.iOSUserNotificationCenterSetNotificationDelay(name, float(seconds))
