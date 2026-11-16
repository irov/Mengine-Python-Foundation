from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.Providers.AdminPanelBuilder import AdminPanelTabBuilder


class AdminPanelProvider(BaseProvider):
    s_allowed_methods = [
        "isAvailable",
        "addButton",
        "setTab",
        "removeTab",
    ]

    @staticmethod
    def isAvailable():
        if AdminPanelProvider.hasProvider() is False:
            return False

        return AdminPanelProvider._call("isAvailable")

    @staticmethod
    def addTab(tab):
        return AdminPanelTabBuilder(tab)

    @staticmethod
    def addButton(tab, identifier, title, callback, *args):
        if AdminPanelProvider.isAvailable() is False:
            return False

        return AdminPanelProvider._call("addButton", tab, identifier, title, callback, *args)

    @staticmethod
    def setTab(tab, layout, callback, *args):
        if AdminPanelProvider.isAvailable() is False:
            return False

        if isinstance(tab, basestring) is False or len(tab) == 0:
            raise ValueError("OpButton tab must be a nonempty string")

        if callable(callback) is False:
            raise ValueError("OpButton panel callback must be callable")

        return AdminPanelProvider._call("setTab", tab, Mengine.encodeJSON(layout), callback, *args)

    @staticmethod
    def removeTab(tab):
        if AdminPanelProvider.hasProvider() is False:
            return

        AdminPanelProvider._call("removeTab", tab)
        pass
