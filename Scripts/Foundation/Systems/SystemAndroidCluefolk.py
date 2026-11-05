from Foundation.Providers.SupportProvider import SupportProvider
from Foundation.Systems.SystemAndroid import SystemAndroid

PROVIDER_NAME = "AndroidCluefolk"
PLUGIN_NAME = "AndroidCluefolkPlugin"


class SystemAndroidCluefolk(SystemAndroid):
    """ Support module 'Cluefolk' for Android """

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemAndroidCluefolk, self)._onInitialize()

        SupportProvider.setProvider(PROVIDER_NAME, dict(openSupport=SystemAndroidCluefolk.openSupport))

    def _onFinalize(self):
        super(SystemAndroidCluefolk, self)._onFinalize()

        if SupportProvider.getName() == PROVIDER_NAME:
            SupportProvider.removeProvider()

    @staticmethod
    def openSupport(subject, body, technical_info):
        if SystemAndroid._androidBooleanMethod(PLUGIN_NAME, "isReady") is False:
            return False

        SystemAndroid._androidMethod(PLUGIN_NAME, "setLanguage", Mengine.getLocale())
        SystemAndroid._androidMethod(PLUGIN_NAME, "open")
        return True
