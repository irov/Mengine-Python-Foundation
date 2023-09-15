from Foundation.Providers.BaseProvider import BaseProvider


class AuthProvider(BaseProvider):
    s_allowed_methods = [
        "login",
        "logout",
        "isLoggedIn",
        "switchAccount",
    ]

    @staticmethod
    def _setDevProvider():
        DummyAuth.setProvider()

    @staticmethod
    def login():
        return AuthProvider._call("login")

    @staticmethod
    def logout():
        return AuthProvider._call("logout")

    @staticmethod
    def isLoggedIn():
        return bool(AuthProvider._call("isLoggedIn"))

    @staticmethod
    def switchAccount():
        return AuthProvider._call("switchAccount")

    @staticmethod
    def _switchAccountNotFoundCb():
        if AuthProvider.isLoggedIn() is True:
            AuthProvider.logout()
        AuthProvider.login()
        return True


class DummyAuth(object):

    s_logged_in = False

    @staticmethod
    def setProvider():
        AuthProvider.setProvider("Dummy", dict(
            login=DummyAuth.login,
            logout=DummyAuth.logout,
            isLoggedIn=DummyAuth.isLoggedIn
        ))

    @staticmethod
    def login():
        DummyAuth.s_logged_in = True
        Notification.notify(Notificator.onUserLoggedIn)
        return True

    @staticmethod
    def logout():
        DummyAuth.s_logged_in = False
        Notification.notify(Notificator.onUserLoggedOut)
        return True

    @staticmethod
    def isLoggedIn():
        return DummyAuth.s_logged_in is True


