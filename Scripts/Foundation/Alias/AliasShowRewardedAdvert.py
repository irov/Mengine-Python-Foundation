from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.TaskAlias import TaskAlias

class AliasShowRewardedAdvert(TaskAlias):
    def _onParams(self, params):
        self.AdPlacement = params.get("AdPlacement")
        self.SuccessCallback = params.get("SuccessCallback")  # starts after show completed successfully
        self.FailCallback = params.get("FailCallback")  # starts if show request or display failed
        self.WhileShowScope = params.get("WhileShowScope")  # runs in parallel with showAdvert
        self._semaphore_ad_display_fail = Semaphore(False, "AdvertDisplayFailed")

    def _setDisplayFailed(self, msg):
        Trace.msg_err("AliasShowRewardedAdvert [{}] display [{}] failed: {}".format(self.AdPlacement, AdvertisementProvider.getName(), msg))
        self._semaphore_ad_display_fail.setValue(True)

    def _showAd(self):
        return AdvertisementProvider.showRewardedAdvert(self.AdPlacement)

    def _onShowCompleted(self, success, params):
        if success is False:
            self._setDisplayFailed("show failed")

        return True

    def _onAvailableAdsEnded(self, placement):
        return placement == self.AdPlacement

    def _scopeShowAdvert(self, source):
        with source.addParallelTask(2) as (display_respond, show):
            # check is advert shown
            with display_respond.addRaceTask(3) as (completed, reached_limit, show_failed):
                completed.addListener(Notificator.onRewardedAdShowCompleted, Filter=self._onShowCompleted)
                reached_limit.addListener(Notificator.onAvailableAdsEnded, Filter=self._onAvailableAdsEnded)
                show_failed.addSemaphore(self._semaphore_ad_display_fail, From=True)

            with show.addIfTask(self._showAd) as (show_accepted, show_rejected):
                show_accepted.addDummy()
                show_rejected.addFunction(self._setDisplayFailed, "show request rejected")

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
        source.addPrint("AliasShowRewardedAdvert [{}] display start [{}]".format(self.AdPlacement, AdvertisementProvider.getName()))

        with source.addParallelTask(2) as (tc_extra, tc_main):
            tc_extra.addScope(self._scopeWhileShow)
            tc_main.addScope(self._scopeShowAdvert)

        source.addPrint("AliasShowRewardedAdvert [{}] display complete [{}]".format(self.AdPlacement, AdvertisementProvider.getName()))

        source.addFunction(self._runCallback)
