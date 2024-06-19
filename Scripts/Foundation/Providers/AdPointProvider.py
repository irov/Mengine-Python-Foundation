from Foundation.Providers.BaseProvider import BaseProvider


class AdPointProvider(BaseProvider):
    trace_level = 0
    s_allowed_methods = [
        "hasAdPoint",
        "getAdPoint",
        "checkAdPoint",
        "triggerAdPoint",
        "startAdPoint",
    ]

    @staticmethod
    def hasAdPoint(ad_point_name):
        return AdPointProvider._call("hasAdPoint", ad_point_name)

    @staticmethod
    def getAdPoint(ad_point_name):
        return AdPointProvider._call("getAdPoint", ad_point_name)

    @staticmethod
    def getAdPointParams(ad_point_name):
        ad_point = AdPointProvider.getAdPoint(ad_point_name)
        return ad_point.params

    @staticmethod
    def isEnabledAdPoint(ad_point_name):
        """ returns False if ad_point is not enabled or not found """
        if AdPointProvider.hasAdPoint(ad_point_name) is False:
            return False
        ad_point_params = AdPointProvider.getAdPointParams(ad_point_name)
        return ad_point_params.enable is True

    @staticmethod
    def checkAdPoint(ad_point_name):
        """ must be called before `startAdPoint` - check if ad point is ready to be shown """
        return AdPointProvider._call("checkAdPoint", ad_point_name)

    @staticmethod
    def triggerAdPoint(ad_point_name):
        """ trigger ad point, increase trigger counter if this feature is enabled in ad point """
        return AdPointProvider._call("triggerAdPoint", ad_point_name)

    @staticmethod
    def startAdPoint(ad_point_name):
        """ reset trigger counter, update time view, starts ad point
        """
        return AdPointProvider._call("startAdPoint", ad_point_name)


