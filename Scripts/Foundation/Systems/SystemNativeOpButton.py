from Foundation.Providers.AdminPanelProvider import AdminPanelProvider
from Foundation.System import System


class SystemNativeOpButton(System):
    def __init__(self):
        super(SystemNativeOpButton, self).__init__()

        self._tabs = set()
        pass

    def _onInitialize(self):
        super(SystemNativeOpButton, self)._onInitialize()

        AdminPanelProvider.setProvider(self.PROVIDER_NAME, dict(
            isAvailable=Mengine.opButtonIsInitialized,
            addButton=self.addButton,
            removeTab=self.removeTab,
        ))
        pass

    def _onFinalize(self):
        super(SystemNativeOpButton, self)._onFinalize()

        for tab in self._tabs.copy():
            self.removeTab(tab)
            pass

        if AdminPanelProvider.getName() == self.PROVIDER_NAME:
            AdminPanelProvider.removeProvider()
            pass
        pass

    def addButton(self, tab, identifier, title, callback, *args):
        if Mengine.opButtonAddButton(tab, identifier, title, callback, *args) is False:
            return False

        self._tabs.add(tab)
        return True

    def removeTab(self, tab):
        Mengine.opButtonRemoveTab(tab)
        self._tabs.discard(tab)
        pass
