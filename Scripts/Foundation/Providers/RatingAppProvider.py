from Foundation.Providers.BaseProvider import BaseProvider


class RatingAppProvider(BaseProvider):
    s_allowed_methods = [
        "rateApp"
    ]

    @staticmethod
    def _setDevProvider():
        DummyRatingApp.setProvider()

    @staticmethod
    def rateApp():
        def _NotFoundCb():
            Trace.msg_err("Not found module to show RateApp...")

        return RatingAppProvider._call("rateApp", NotFoundCb=_NotFoundCb)


class DummyRatingApp(object):

    @staticmethod
    def setProvider():
        RatingAppProvider.setProvider("Dummy", dict(rateApp=DummyRatingApp.rateApp))

    @staticmethod
    def rateApp():
        Trace.msg_err("Sent onAppRated for developer, but module for RateApp not found")
        Notification.notify(Notificator.onAppRated)


