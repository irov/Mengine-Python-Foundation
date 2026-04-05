from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Providers.ConsentProvider import ConsentProvider
from Foundation.Systems.SystemAppleAd import SystemAppleAd

_Log = SimpleLogger("SystemAppleAppLovin")

APPLE_PLUGIN_NAME = "AppleAppLovinPlugin"


class SystemAppleAppLovin(SystemAppleAd):
    """ Advertisement module 'AppLovin' for iOS """

    is_plugin_active = False
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        SystemAppleAppLovin.is_plugin_active = Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)
        return SystemAppleAppLovin.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("AppleAppLovin", methods)

        consent_methods = dict(
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )

        ConsentProvider.setProvider("AppleAppLovin", consent_methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemAppleAppLovin.is_sdk_init is True

    def showConsentFlow(self):
        def __cbConsentFlowShowSuccess(self):
            _Log("[cb] Consent Flow Show Successful")

        def __cbConsentFlowShowFailed(self):
            _Log("[cb] Consent Flow Show Failed", err=True, force=True)

        Mengine.appleAppLovinLoadAndShowCMPFlow(dict(
            onAppleAppLovinConsentFlowShowSuccess=__cbConsentFlowShowSuccess,
            onAppleAppLovinConsentFlowShowFailed=__cbConsentFlowShowFailed,
        ))

    def isConsentFlow(self):
        return Mengine.appleAppLovinIsConsentFlowUserGeographyGDPR()

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemAppleAppLovin.is_sdk_init = True
        self._setAdServiceReady()
