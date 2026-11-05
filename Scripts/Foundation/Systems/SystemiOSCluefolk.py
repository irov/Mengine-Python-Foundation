from Foundation.Providers.SupportProvider import SupportProvider
from Foundation.System import System

PROVIDER_NAME = "iOSCluefolk"
PLUGIN_NAME = "iOSCluefolkPlugin"


class SystemiOSCluefolk(System):
    """ Support module 'Cluefolk' for iOS """

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemiOSCluefolk, self)._onInitialize()

        SupportProvider.setProvider(PROVIDER_NAME, dict(openSupport=SystemiOSCluefolk.openSupport))

    def _onFinalize(self):
        super(SystemiOSCluefolk, self)._onFinalize()

        if SupportProvider.getName() == PROVIDER_NAME:
            SupportProvider.removeProvider()

    @staticmethod
    def openSupport(subject, body, technical_info):
        if Mengine.iOSCluefolkIsReady() is False:
            return False

        Mengine.iOSCluefolkSetLanguage(Mengine.getLocale())
        Mengine.iOSCluefolkOpen()
        return True
