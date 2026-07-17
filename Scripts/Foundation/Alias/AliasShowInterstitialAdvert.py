from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.TaskAlias import TaskAlias


class AliasShowInterstitialAdvert(TaskAlias):
    def _onParams(self, params):
        self.AdPlacement = params.get("AdPlacement")
        self._semaphore_ad_display_fail = Semaphore(False, "InterstitialAdvertDisplayFailed")

    def _setDisplayFailed(self, msg):
        Trace.msg_err("AliasShowInterstitialAdvert [{}] display [{}] failed: {}"
                      .format(self.AdPlacement, AdvertisementProvider.getName(), msg))
        self._semaphore_ad_display_fail.setValue(True)

    def _showAd(self):
        return AdvertisementProvider.showInterstitialAdvert(self.AdPlacement)

    def _onShowCompleted(self, success, params):
        if success is False:
            self._setDisplayFailed("show failed")

        return True

    def _scopeShowAdvert(self, source):
        with source.addParallelTask(2) as (response, request):
            with response.addRaceTask(2) as (completed, show_failed):
                completed.addListener(Notificator.onInterstitialAdShowCompleted, Filter=self._onShowCompleted)
                show_failed.addSemaphore(self._semaphore_ad_display_fail, From=True)

            with request.addIfTask(self._showAd) as (show_accepted, show_rejected):
                show_accepted.addDummy()
                show_rejected.addFunction(self._setDisplayFailed, "show request rejected")

    def _onGenerate(self, source):
        source.addPrint("AliasShowInterstitialAdvert [{}] display start [{}]"
                        .format(self.AdPlacement, AdvertisementProvider.getName()))

        source.addScope(self._scopeShowAdvert)

        source.addPrint("AliasShowInterstitialAdvert [{}] display complete [{}]"
                        .format(self.AdPlacement, AdvertisementProvider.getName()))
