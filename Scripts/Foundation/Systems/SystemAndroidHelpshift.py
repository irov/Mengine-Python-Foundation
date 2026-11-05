from Foundation.Providers.SupportProvider import SupportProvider
from Foundation.Systems.SystemAndroid import SystemAndroid

PROVIDER_NAME = "AndroidHelpshift"
PLUGIN_NAME = "AndroidHelpshiftPlugin"


class SystemAndroidHelpshift(SystemAndroid):
    """ Support module 'Helpshift' for Android """

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemAndroidHelpshift, self)._onInitialize()

        SupportProvider.setProvider(PROVIDER_NAME, dict(openSupport=SystemAndroidHelpshift.openSupport))

    def _onFinalize(self):
        super(SystemAndroidHelpshift, self)._onFinalize()

        if SupportProvider.getName() == PROVIDER_NAME:
            SupportProvider.removeProvider()

    @staticmethod
    def openSupport(subject, body, technical_info):
        SystemAndroid._androidMethod(PLUGIN_NAME, "setLanguage", Mengine.getLocale())
        SystemAndroid._androidMethod(PLUGIN_NAME, "showConversation")
        return True
