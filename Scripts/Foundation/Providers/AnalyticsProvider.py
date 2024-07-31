from Foundation.Providers.BaseProvider import BaseProvider


class AnalyticsProvider(BaseProvider):
    """ Check docs at Foundation.System.SystemAnalytics """

    trace_level = 1
    s_allowed_methods = [
        "sendAnalytic",
        "addAnalytic",
        "hasAnalytic",
        "addRelatedAnalytic",
        "eventFlush",
    ]

    @staticmethod
    def sendAnalytic(event_key, send_params):
        return AnalyticsProvider._call("sendAnalytic", event_key, send_params)

    @staticmethod
    def addAnalytic(event_key, identity, check_method=None, params_method=None, service_key=None):
        return AnalyticsProvider._call("addAnalytic", event_key, identity,
                                       check_method=check_method, params_method=params_method, service_key=service_key)

    @staticmethod
    def hasAnalytic(event_key):
        return AnalyticsProvider._call("hasAnalytic", event_key)

    @staticmethod
    def addRelatedAnalytic(this_event_key, related_event_key, Filter=None, Params=None):
        return AnalyticsProvider._call("addRelatedAnalytic", this_event_key, related_event_key,
                                       Filter=Filter, Params=Params)

    @staticmethod
    def eventFlush():
        return AnalyticsProvider._call("eventFlush")
