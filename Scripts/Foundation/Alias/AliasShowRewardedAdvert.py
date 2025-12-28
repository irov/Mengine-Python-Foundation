from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.TaskAlias import TaskAlias

class AliasShowRewardedAdvert(TaskAlias):
    in_processing = False

    def _onParams(self, params):
        self.AdPlacement = params.get("AdPlacement")
        self.Timeout = params.get("TimeoutInSeconds", 30) * 1000.0
        self.SuccessCallback = params.get("SuccessCallback")  # starts after show success (not rewarded, just shown)
        self.FailCallback = params.get("FailCallback")  # starts after show if show failed
        self.WhileShowScope = params.get("WhileShowScope")  # runs in parallel with showAdvert
        self.Bypass = params.get("Bypass", False)
        self._semaphore_ad_display_ok = Semaphore(False, "AdvertDisplaySuccess")
        self._semaphore_ad_display_fail = Semaphore(False, "AdvertDisplayFailed")

    @staticmethod
    def setInProcessing(state):
        AliasShowRewardedAdvert.in_processing = bool(state)

    def _displayRespondError(self, msg):
        Trace.msg_err("AliasShowRewardedAdvert [{}] display [{}] respond failed: {}".format(self.AdPlacement, AdvertisementProvider.getName(), msg))
        self._semaphore_ad_display_fail.setValue(True)

    def _showAd(self):
        AdvertisementProvider.showRewardedAdvert(self.AdPlacement)

    def _scopeShowAdvert(self, source):
        with source.addParallelTask(2) as (display_respond, show):
            # check is advert shown
            with display_respond.addRaceTask(2) as (completed, reached_limit):
                completed.addListener(Notificator.onAdShowCompleted)
                reached_limit.addListener(Notificator.onAvailableAdsEnded)

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
        if AliasShowRewardedAdvert.in_processing is True:
            if self.Bypass is True:
                Trace.msg_err("AliasShowRewardedAdvert warning [{}] [{}] - already in processing, but Bypass is True"
                              .format(self.AdPlacement, AdvertisementProvider.getName()))
            else:
                Trace.log("Task", 0, "AliasShowRewardedAdvert failed [{}] [{}] - already in processing".format(self.AdPlacement, AdvertisementProvider.getName()))
                source.addDummy()
                return

        source.addPrint("AliasShowRewardedAdvert [{}] display start [{}]".format(self.AdPlacement, AdvertisementProvider.getName()))

        source.addFunction(AliasShowRewardedAdvert.setInProcessing, True)

        with source.addParallelTask(2) as (tc_extra, tc_main):
            tc_extra.addScope(self._scopeWhileShow)
            tc_main.addScope(self._scopeShowAdvert)

        source.addFunction(AliasShowRewardedAdvert.setInProcessing, False)

        source.addPrint("AliasShowRewardedAdvert [{}] display complete [{}]".format(self.AdPlacement, AdvertisementProvider.getName()))

        source.addFunction(self._runCallback)
