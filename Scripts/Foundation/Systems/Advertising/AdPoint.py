from Foundation.Initializer import Initializer


class AdPointParams(object):
    def __init__(self, params):
        self.name = params["name"]
        self.enable = params.get("enable", True)
        self.ad_type = params.get("ad_type", "Interstitial")
        self.ad_unit_name = params.get("ad_unit_name", self.ad_type)

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
        self.name = None
        self.params = None
        self.active = False

    def _onInitialize(self, params):
        self.params = AdPointParams(params)
        self.name = self.params.name

        self.params.validate()

    def onActivate(self):  # todo
        self.active = True
        return

    def _onFinalize(self):
        if self.active is False:
            Trace.log("System", 0, "AdPoint '{}' finalize before activate".format(self.name))

        self.params = None
        self.name = None
        self.active = False

    def check(self):  # todo
        return False

    def trigger(self):  # todo
        return False

    def start(self):  # todo
        return False




