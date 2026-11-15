from Foundation.Providers.BaseProvider import BaseProvider


class AdminPanelProvider(BaseProvider):
    s_allowed_methods = [
        "isAvailable",
        "addButton",
        "removeTab",
    ]

    @staticmethod
    def isAvailable():
        if AdminPanelProvider.hasProvider() is False:
            return False

        return AdminPanelProvider._call("isAvailable")

    @staticmethod
    def addButton(tab, identifier, title, callback, *args):
        if AdminPanelProvider.isAvailable() is False:
            return False

        return AdminPanelProvider._call("addButton", tab, identifier, title, callback, *args)

    @staticmethod
    def removeTab(tab):
        if AdminPanelProvider.hasProvider() is False:
            return

        AdminPanelProvider._call("removeTab", tab)
        pass
