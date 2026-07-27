from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Utils import SimpleLogger
from Foundation.Providers.ConsentProvider import ConsentProvider
from Foundation.Systems.SystemiOSAd import SystemiOSAd

_Log = SimpleLogger("SystemiOSAppLovin")

PLUGIN_NAME = "iOSAppLovinPlugin"

class SystemiOSAppLovin(SystemiOSAd):
    """ Advertisement module 'AppLovin' for iOS """

    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)
    is_sdk_init = False

    @staticmethod
    def _onAvailable(params):
        return SystemiOSAppLovin.is_plugin_active

    def _onInitialize(self):
        methods = self.initAds()
        AdvertisementProvider.setProvider("iOSAppLovin", methods)

        consent_methods = dict(
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )

        ConsentProvider.setProvider("iOSAppLovin", consent_methods)
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

    @staticmethod
    def isSdkInitialized():
        return SystemiOSAppLovin.is_sdk_init is True

    def showConsentFlow(self):
        def __cbConsentFlowShowSuccess():
            _Log("[cb] Consent Flow Show Successful")

        def __cbConsentFlowShowFailed():
            _Log("[cb] Consent Flow Show Failed", err=True, force=True)

        Mengine.iOSAppLovinLoadAndShowCMPFlow(dict(
            oniOSAppLovinConsentFlowShowSuccessful=__cbConsentFlowShowSuccess,
            oniOSAppLovinConsentFlowShowFailed=__cbConsentFlowShowFailed,
        ))

    def isConsentFlow(self):
        return Mengine.iOSAppLovinIsConsentFlowUserGeographyGDPR()

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemiOSAppLovin.is_sdk_init = True
        self._setAdServiceReady()
