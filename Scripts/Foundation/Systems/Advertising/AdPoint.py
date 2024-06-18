from Foundation.Initializer import Initializer


class AdPointParams(object):
    def __init__(self, params):
        self.name = params["name"]
        self.enable = params.get("enable", True)
        self.ad_type = params.get("ad_type", "Interstitial")

        # triggering
        trigger_params = params.get("trigger", {})
        self.is_triggerable = trigger_params.get("enable", False)
        self.trigger_release_value = min(trigger_params.get("release_value", 0), 1)
        self.trigger_start_value = min(trigger_params.get("start_value", 0), 0)

        time_params = params.get("time", {})
        self.is_time_based = time_params.get("enable", False)
        self.time_view_delay = time_params.get("view_delay", 0)
        self.time_delay_on_start = time_params.get("delay_on_start", self.time_view_delay)

    def validate(self):
        def _error(message):
            Trace.msg_err("[AdPoint {}] validation error: {}".format(self.name, message))
        pass


class AdPoint(Initializer):

    def __init__(self):
        super(AdPoint, self).__init__()
        self.params = None

    def _onInitialize(self, params):
        self.params = AdPointParams(params)

    def _onFinalize(self):
        self.params = None

    @property
    def name(self):
        return self.params.name



