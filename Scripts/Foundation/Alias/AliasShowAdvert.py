from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.TaskAlias import TaskAlias


class AliasShowAdvert(TaskAlias):
    in_processing = False

    def _onParams(self, params):
        self.AdType = params.get("AdType", "Rewarded")
        self.AdUnitName = params.get("AdUnitName", self.AdType)
        self.Timeout = params.get("TimeoutInSeconds", 30) * 1000.0
        self.SuccessCallback = params.get("SuccessCallback")  # starts after show success (not rewarded, just shown)
        self.FailCallback = params.get("FailCallback")  # starts after show if show failed
        self.WhileShowScope = params.get("WhileShowScope")  # runs in parallel with showAdvert
        self.Bypass = params.get("Bypass", False)
        self._semaphore_ad_display_ok = Semaphore(False, "AdvertDisplaySuccess")
        self._semaphore_ad_display_fail = Semaphore(False, "AdvertDisplayFailed")

    @staticmethod
    def setInProcessing(state):
        AliasShowAdvert.in_processing = bool(state)

    def _displayRespondError(self, msg):
        Trace.msg_err("AliasShowAdvert [{}:{}] display [{}] respond failed: {}".format(
            self.AdType, self.AdUnitName, AdvertisementProvider.getName(), msg))
        self._semaphore_ad_display_fail.setValue(True)

    def _showAd(self):
        AdvertisementProvider.showAdvert(AdType=self.AdType, AdUnitName=self.AdUnitName)

    def _scopeShowAdvert(self, source):
        with source.addParallelTask(2) as (display_respond, show):
            # check is advert shown
            with display_respond.addRaceTask(4) as (ok, fail, timeout, reached_limit):
                with ok.addParallelTask(2) as (ok_display, ok_hide):
                    ok_display.addListener(Notificator.onAdvertDisplayed)
                    ok_display.addSemaphore(self._semaphore_ad_display_ok, To=True)
                    ok_hide.addListener(Notificator.onAdvertHidden)

                fail.addListener(Notificator.onAdvertDisplayFailed)
                fail.addFunction(self._displayRespondError, "display failed")

                timeout.addDelay(self.Timeout)
                with timeout.addIfSemaphore(self._semaphore_ad_display_ok, True) as (_, error):
                    # if after timeout delay ad not displayed - send error
                    error.addFunction(self._displayRespondError, "timeout {} seconds".format(self.Timeout / 1000))

                reached_limit.addListener(Notificator.onAvailableAdsEnded)
                reached_limit.addFunction(self._displayRespondError, "reached ads limit")

            show.addFunction(self._showAd)

    def _scopeWhileShow(self, source):
        if callable(self.WhileShowScope) is False:
            source.addDummy()
            return

        with source.addRaceTask(2) as (tc_while, tc_skip):
            tc_while.addScope(self.WhileShowScope)
            tc_skip.addSemaphore(self._semaphore_ad_display_fail, From=True)

    def _runCallback(self):
        if self._semaphore_ad_display_fail.getValue() is True:
            cb = self.FailCallback
        else:
            cb = self.SuccessCallback

        if callable(cb):
            cb()

    def _onGenerate(self, source):
        if self.in_processing is True:
            if self.Bypass is True:
                Trace.msg_err("AliasShowAdvert warning [{}:{}] [{}] - already in processing, but Bypass is True"
                              .format(self.AdType, self.AdUnitName, AdvertisementProvider.getName()))
            else:
                Trace.log("Task", 0, "AliasShowAdvert failed [{}:{}] [{}] - already in processing"
                          .format(self.AdType, self.AdUnitName, AdvertisementProvider.getName()))
                source.addDummy()
                return

        source.addPrint("AliasShowAdvert [{}:{}] display start [{}]".format(
            self.AdType, self.AdUnitName, AdvertisementProvider.getName()))

        source.addFunction(self.setInProcessing, True)

        with source.addParallelTask(2) as (tc_extra, tc_main):
            tc_extra.addScope(self._scopeWhileShow)
            tc_main.addScope(self._scopeShowAdvert)

        source.addFunction(self._runCallback)

        source.addPrint("AliasShowAdvert [{}:{}] display complete [{}]".format(
            self.AdType, self.AdUnitName, AdvertisementProvider.getName()))

        source.addFunction(self.setInProcessing, False)
