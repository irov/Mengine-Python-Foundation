from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.TaskAlias import TaskAlias


class AliasShowAdvert(TaskAlias):
    in_processing = False

    def _onParams(self, params):
        self.AdType = params.get("AdType", "Rewarded")
        self.AdUnitName = params.get("AdUnitName", self.AdType)
        self.Timeout = params.get("TimeoutInSeconds", 30) * 1000
        self.SuccessCallback = params.get("SuccessCallback")  # starts after show success (not rewarded, just shown)
        self.FailCallback = params.get("FailCallback")  # starts after show if show failed
        self.WhileShowScope = params.get("WhileShowScope")  # runs in parallel with showAdvert
        self._ad_displayed = False
        self._ad_display_failed = False

    @staticmethod
    def setInProcessing(state):
        AliasShowAdvert.in_processing = bool(state)

    def _setAdDisplayed(self, state):
        self._ad_displayed = bool(state)

    def _displayRespondError(self, msg):
        Trace.msg_err("AliasShowAdvert [{}:{}] display [{}] respond failed: {}".format(
            self.AdType, self.AdUnitName, AdvertisementProvider.getName(), msg))
        self._ad_display_failed = True

    def _showAd(self):
        AdvertisementProvider.showAdvert(AdType=self.AdType, AdUnitName=self.AdUnitName)

    def _scopeShowAdvert(self, source):
        with source.addParallelTask(2) as (display_respond, show):
            # check is advert shown
            with display_respond.addRaceTask(4) as (ok, fail, timeout, reached_limit):
                with ok.addParallelTask(2) as (ok_display, ok_hide):
                    ok_display.addListener(Notificator.onAdvertDisplayed)
                    ok_display.addFunction(self._setAdDisplayed, True)
                    ok_hide.addListener(Notificator.onAdvertHidden)

                fail.addListener(Notificator.onAdvertDisplayFailed)
                fail.addFunction(self._displayRespondError, "display failed")

                timeout.addDelay(self.Timeout)
                with timeout.addIfTask(lambda: self._ad_displayed is False) as (error, _):
                    # if after timeout delay ad not displayed - send error
                    error.addFunction(self._displayRespondError, "timeout {} seconds".format(self.Timeout / 1000))

                reached_limit.addListener(Notificator.onAvailableAdsEnded)
                reached_limit.addFunction(self._displayRespondError, "reached ads limit")

            show.addFunction(self._showAd)

    def _scopeWhileShow(self, source):
        if callable(self.WhileShowScope) is True:
            source.addScope(self.WhileShowScope)
        else:
            source.addDummy()

    def _runCallback(self):
        if self._ad_display_failed is True:
            cb = self.FailCallback
        else:
            cb = self.SuccessCallback

        if callable(cb):
            cb()

    def _onGenerate(self, source):
        if self.in_processing is True:
            Trace.log("Task", 0, "AliasShowAdvert failed - already in processing")
            source.addDummy()
            return

        if _DEVELOPMENT is True:
            Trace.msg("AliasShowAdvert [{}:{}] display [{}]".format(
                self.AdType, self.AdUnitName, AdvertisementProvider.getName()))

        source.addFunction(self.setInProcessing, True)

        with source.addParallelTask(2) as (extra, show):
            extra.addScope(self._scopeWhileShow)
            show.addScope(self._scopeShowAdvert)

        source.addFunction(self._runCallback)

        source.addFunction(self.setInProcessing, False)
