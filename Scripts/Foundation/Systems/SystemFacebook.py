from Foundation.System import System
from Foundation.Providers.FacebookProvider import FacebookProvider
from Foundation.Systems.Facebook.AppleFacebook import AppleFacebook
from Foundation.Systems.Facebook.AndroidFacebook import AndroidFacebook


class SystemFacebook(System):

    onLoginSuccess = Event("onLoginSuccess")  # <- token
    onLoginCancel = Event("onLoginCancel")
    onLoginError = Event("onLoginError")  # <- message

    onLogoutCancel = Event("onLogoutCancel")
    onLogoutSuccess = Event("onLogoutSuccess")  # <- token

    onShareSuccess = Event("onShareSuccess")  # <- post_id
    onShareCancel = Event("onShareCancel")
    onShareError = Event("onShareError")  # <- message

    onUserFetchSuccess = Event("onUserFetchSuccess")  # <- object_string, response_string
    onProfilePictureLinkGet = Event("onProfilePictureLinkGet")  # <- user_id, is_logged, picture_url

    callbacks = {}

    def __init__(self):
        super(SystemFacebook, self).__init__()
        self.provider = None

    def _onInitialize(self):
        if Mengine.isAvailablePlugin(AppleFacebook.plugin_name):
            self.provider = AppleFacebook()
        elif Mengine.isAvailablePlugin(AndroidFacebook.plugin_name):
            self.provider = AndroidFacebook()
        else:
            return

        self.provider.onInitialize(self)

        FacebookProvider.setProvider(self.provider.name, dict(
            getAccessToken=self.getAccessToken,
            isLoggedIn=self.isLoggedIn,
            performLogin=self.performLogin,
            shareLink=self.shareLink,
            logout=self.logout,
            getUser=self.getUser,
            getProfilePictureLink=self.getProfilePictureLink,
            getProfileUserPictureLink=self.getProfileUserPictureLink,
        ))

    def _onFinalize(self):
        if self.provider is not None:
            self.provider.onFinalize()
            self.provider = None

    def isLoggedIn(self):
        is_logged = self.provider.isLoggedIn()
        return is_logged

    def getAccessToken(self):
        token = self.provider.getAccessToken()
        return token

    def performLogin(self, permissions=('email', 'public_profile'),
                     _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemFacebook.onLoginSuccess: _cb_success,
            SystemFacebook.onLoginCancel: _cb_cancel,
            SystemFacebook.onLoginError: _cb_error
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)

        self.provider.performLogin(permissions)

    def shareLink(self, link=None, msg='',
                  _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemFacebook.onShareSuccess: _cb_success,
            SystemFacebook.onShareCancel: _cb_cancel,
            SystemFacebook.onShareError: _cb_error
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)

        self.provider.shareLink(link, msg)

    def logout(self, _cb_success=None, _cb_cancel=None):
        callbacks = {
            SystemFacebook.onLogoutSuccess: _cb_success,
            SystemFacebook.onLogoutCancel: _cb_cancel,
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)

        self.provider.logout()

    def getUser(self, _cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onUserFetchSuccess, _cb)
        self.provider.getUser()

    def getProfilePictureLink(self, type_parameter="?type=large", _cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onProfilePictureLinkGet, _cb)
        self.provider.getProfilePictureLink(type_parameter)

    def getProfileUserPictureLink(self, user_id, type_parameter="?type=large", _cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onProfilePictureLinkGet, _cb)
        self.provider.getProfileUserPictureLink(user_id, type_parameter)

    # utils

    @staticmethod
    def addCallback(event, fn):
        def _cb(*args, **kwargs):
            callbacks = SystemFacebook.callbacks[event]
            for cb in callbacks:
                event.removeObserver(cb)
            SystemFacebook.callbacks.pop(event)
            fn(*args, **kwargs)

        if event not in SystemFacebook.callbacks:
            SystemFacebook.callbacks[event] = []
        SystemFacebook.callbacks[event].append(_cb)
        event += _cb
