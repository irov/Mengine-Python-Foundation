from Foundation.Providers.LocalNotificationsProvider import LocalNotificationsProvider
from Foundation.Systems.SystemAndroid import SystemAndroid

PROVIDER_NAME = "AndroidLocalNotifications"
PLUGIN_NAME = "AndroidLNotificationsPlugin"


class SystemAndroidLocalNotifications(SystemAndroid):
    """ Local notifications module for Android (LocalNotifications plugin) """

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemAndroidLocalNotifications, self)._onInitialize()

        methods = dict(setNotificationDelay=SystemAndroidLocalNotifications.setNotificationDelay)
        LocalNotificationsProvider.setProvider(PROVIDER_NAME, methods)

    def _onFinalize(self):
        super(SystemAndroidLocalNotifications, self)._onFinalize()

        if LocalNotificationsProvider.getName() == PROVIDER_NAME:
            LocalNotificationsProvider.removeProvider()

    @staticmethod
    def setNotificationDelay(name, seconds):
        # Java int parameter: python int maps to 'I' in the JNI signature
        SystemAndroid._androidMethod(PLUGIN_NAME, "setNotificationDelay", name, int(max(seconds, 0)))
