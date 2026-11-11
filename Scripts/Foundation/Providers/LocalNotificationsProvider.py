from Foundation.Providers.BaseProvider import BaseProvider


class LocalNotificationsProvider(BaseProvider):
    """ Local notifications are configured per project in the deploy (iOS Info.plist, Android res/xml).
        The platform plugin schedules them when the game goes to background and cancels them when it returns.
        Notifications marked as 'script' fire only after the game sets their delay here. """

    s_allowed_methods = [
        "setNotificationDelay",  # (name, seconds) - fire 'name' in seconds from now; seconds <= 0 cancels it
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
