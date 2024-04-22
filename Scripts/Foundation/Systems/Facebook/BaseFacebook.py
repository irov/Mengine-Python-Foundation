from Foundation.Initializer import Initializer


class BaseFacebook(Initializer):
    name = None     # type: str
    plugin_name = None   # type: str

    def __init__(self):
        super(BaseFacebook, self).__init__()
        self.system = None

    def _onInitialize(self, system):
        self.system = system

    def _onFinalize(self):
        pass

    def getProviderMethods(self):  # type: () -> dict
        return self._getProviderMethods()

    def _getProviderMethods(self):
        raise NotImplementedError

    def getAccessToken(self):  # type: () -> str
        return self._getAccessToken()

    def _getAccessToken(self):
        raise NotImplementedError

    def isLoggedIn(self):  # type: () -> bool
        return self._isLoggedIn()

    def _isLoggedIn(self):
        raise NotImplementedError

    def performLogin(self, permissions=('email', 'public_profile')):
        return self._performLogin(permissions)

    def _performLogin(self, permissions):
        raise NotImplementedError

    def shareLink(self, link=None, msg=''):
        return self._shareLink(link, msg)

    def _shareLink(self, link, msg):
        raise NotImplementedError

    def logout(self):
        return self._logout()

    def _logout(self):
        raise NotImplementedError

    def getUser(self):
        return self._getUser()

    def _getUser(self, ):
        raise NotImplementedError

    def getProfilePictureLink(self, type_parameter="?type=large"):
        return self._getProfilePictureLink(type_parameter)

    def _getProfilePictureLink(self, type_parameter):
        raise NotImplementedError

    def getProfileUserPictureLink(self, user_id, type_parameter="?type=large"):
        return self._getProfileUserPictureLink(user_id, type_parameter)

    def _getProfileUserPictureLink(self, user_id, type_parameter):
        raise NotImplementedError
