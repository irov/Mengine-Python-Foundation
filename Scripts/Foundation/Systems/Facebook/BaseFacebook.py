from Foundation.Initializer import Initializer


class BaseFacebook(Initializer):
    name = None     # type: str

    def __init__(self):
        super(BaseFacebook, self).__init__()
        pass

    def _onInitialize(self, *args, **kwds):
        pass

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

    def performLogin(self, permissions=('email', 'public_profile'),
                     _cb_success=None, _cb_cancel=None, _cb_error=None):
        return self._performLogin(permissions, _cb_success, _cb_cancel, _cb_error)

    def _performLogin(self, permissions, _cb_success, _cb_cancel, _cb_error):
        raise NotImplementedError

    def shareLink(self, link=None, msg='',
                  _cb_success=None, _cb_cancel=None, _cb_error=None):
        return self._shareLink(link, msg, _cb_success, _cb_cancel, _cb_error)

    def _shareLink(self, link, msg, _cb_success, _cb_cancel, _cb_error):
        raise NotImplementedError

    def logout(self, _cb_success=None, _cb_cancel=None):
        return self._logout(_cb_success, _cb_cancel)

    def _logout(self, _cb_success, _cb_cancel):
        raise NotImplementedError

    def getUser(self, _cb=None):
        return self._getUser(_cb)

    def _getUser(self, _cb):
        raise NotImplementedError

    def getProfilePictureLink(self, type_parameter="?type=large", _cb=None):
        return self._getProfilePictureLink(type_parameter, _cb)

    def _getProfilePictureLink(self, type_parameter, _cb):
        raise NotImplementedError

    def getProfileUserPictureLink(self, user_id, type_parameter="?type=large", _cb=None):
        return self._getProfileUserPictureLink(user_id, type_parameter, _cb)

    def _getProfileUserPictureLink(self, user_id, type_parameter, _cb):
        raise NotImplementedError
