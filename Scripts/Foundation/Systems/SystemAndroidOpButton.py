from Foundation.Providers.AdminPanelProvider import AdminPanelProvider
from Foundation.Systems.SystemAndroid import SystemAndroid


class SystemAndroidOpButton(SystemAndroid):
    PROVIDER_NAME = "AndroidOpButton"
    PLUGIN_NAME = "AndroidOpButtonPlugin"

    def __init__(self):
        super(SystemAndroidOpButton, self).__init__()

        self.__commands = {}
        self.__panels = {}
        pass

    @staticmethod
    def _onAvailable(params):
        return Mengine.isAvailablePlugin(SystemAndroidOpButton.PLUGIN_NAME)

    def _onInitialize(self):
        super(SystemAndroidOpButton, self)._onInitialize()

        self._addAndroidCallback(self.PLUGIN_NAME, "onOpButtonCommand", self.__onCommand)
        self._addAndroidCallback(self.PLUGIN_NAME, "onOpButtonPanelCommand", self.__onPanelCommand)

        AdminPanelProvider.setProvider(self.PROVIDER_NAME, dict(
            isAvailable=SystemAndroidOpButton.isAvailable,
            addButton=self.addButton,
            setTab=self.setTab,
            removeTab=self.removeTab,
        ))
        pass

    def _onFinalize(self):
        super(SystemAndroidOpButton, self)._onFinalize()

        tabs = set(tab for tab, identifier in self.__commands)
        tabs.update(self.__panels)
        for tab in tabs:
            self.removeTab(tab)
            pass

        self._removeAndroidCallbacks(self.PLUGIN_NAME)

        if AdminPanelProvider.getName() == self.PROVIDER_NAME:
            AdminPanelProvider.removeProvider()
            pass
        pass

    @staticmethod
    def isAvailable():
        return Mengine.androidBooleanMethod(SystemAndroidOpButton.PLUGIN_NAME, "isInitialized")

    def addButton(self, tab, identifier, title, callback, *args):
        Mengine.androidMethod(self.PLUGIN_NAME, "addCommandButton", tab, identifier, title)
        self.__commands[(tab, identifier)] = (callback, args)
        return True

    def setTab(self, tab, layout, callback, *args):
        Mengine.androidMethod(self.PLUGIN_NAME, "setCommandTab", tab, layout)
        self.__commands.remove_if(lambda key, value: key[0] == tab)
        self.__panels[tab] = (callback, args)
        return True

    def removeTab(self, tab):
        Mengine.androidMethod(self.PLUGIN_NAME, "removeCommandTab", tab)

        self.__commands.remove_if(lambda key, value: key[0] == tab)
        self.__panels.pop(tab, None)
        pass

    def __onPanelCommand(self, tab, identifier, value):
        panel = self.__panels.get(tab)
        if panel is None:
            return

        callback, args = panel
        callback(identifier, value, *args)
        pass

    def __onCommand(self, tab, identifier):
        command = self.__commands.get((tab, identifier))
        if command is None:
            return

        callback, args = command
        callback(*args)
        pass
