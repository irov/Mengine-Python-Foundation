from Foundation.Providers.ConsentProvider import ConsentProvider

class DummyConsent(object):
    """ Dummy Consent Provider """

    @staticmethod
    def showConsentFlow():
        Trace.msg("<DummyConsent> DUMMY show consent flow...")
        return

    @staticmethod
    def isConsentFlow():
        return Mengine.getConfigBool("Advertising", "DummyConsentFlow", False) is True

    @staticmethod
    def setProvider():
        def _ShowConsentFlow():
            return DummyConsent.showConsentFlow()
        def _IsConsentFlow():
            return DummyConsent.isConsentFlow()

        methods = dict(
            ShowConsentFlow=_ShowConsentFlow,
            IsConsentFlow=_IsConsentFlow,
        )

        ConsentProvider.setProvider("Dummy", methods)

