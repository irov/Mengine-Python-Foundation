from Foundation.Providers.BaseProvider import BaseProvider

class ConsentProvider(BaseProvider):
    """
    Provider for Consent Flow (GDPR/CCPA)
    """

    s_allowed_methods = [
        "ShowConsentFlow",
        "IsConsentFlow",
    ]

    @staticmethod
    def _setDevProvider():
        from Foundation.Providers.DummyConsent import DummyConsent
        DummyConsent.setProvider()

    @staticmethod
    def showConsentFlow():
        return ConsentProvider._call("ShowConsentFlow")

    @staticmethod
    def isConsentFlow():
        return ConsentProvider._call("IsConsentFlow")

