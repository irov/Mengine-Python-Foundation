from Foundation.Providers.BaseProvider import BaseProvider


class RateAppProvider(BaseProvider):
    s_allowed_methods = [
        "rateApp"
    ]

    @staticmethod
    def _setDevProvider():
        DummyRatingApp.setProvider()

    @staticmethod
    def rateApp():
        return RateAppProvider._call("rateApp")

    @staticmethod
    def _rateAppNotFoundCb():
        Trace.msg_err("Not found module to show RateApp...")


class DummyRatingApp(object):

    @staticmethod
    def setProvider():
        RateAppProvider.setProvider("Dummy", dict(rateApp=DummyRatingApp.rateApp))

    @staticmethod
    def rateApp():
        Trace.msg_err("Sent onAppRated for developer, but module for RateApp not found")
        Notification.notify(Notificator.onAppRated)


