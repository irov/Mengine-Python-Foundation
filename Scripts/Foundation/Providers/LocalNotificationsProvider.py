from Foundation.Providers.BaseProvider import BaseProvider


class LocalNotificationsProvider(BaseProvider):
    """ Project notifications are scheduled when the application goes to background.
        Script notifications require a delay. A delay also overrides a configured notification's trigger. """

    s_allowed_methods = [
        "setNotificationDelay",  # (name, seconds) - fire 'name' in seconds from now; seconds <= 0 clears the override
    ]

    @staticmethod
    def setNotificationDelay(name, seconds):
        if LocalNotificationsProvider.hasProvider() is False:
            return False

        LocalNotificationsProvider._call("setNotificationDelay", name, seconds)
        return True

    @staticmethod
    def _setNotificationDelayExceptionCb(ex, name, seconds):
        Trace.log_exception("Provider", 0, "LocalNotificationsProvider {!r} setNotificationDelay {!r}: {}".format(
            LocalNotificationsProvider.getName(), name, ex))
        return False
