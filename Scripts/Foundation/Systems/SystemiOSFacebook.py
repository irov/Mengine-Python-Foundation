from Foundation.System import System
from Foundation.Providers.FacebookProvider import FacebookProvider

PLUGIN_NAME = "iOSFacebookPlugin"

class SystemiOSFacebook(System):
    is_plugin_active = Mengine.isAvailablePlugin(PLUGIN_NAME)

    onLoginSuccess = Event("onLoginSuccess")
    onLoginCancel = Event("onLoginCancel")
    onLoginError = Event("onLoginError")

    onLogoutSuccess = Event("onLogoutSuccess")
    onLogoutError = Event("onLogoutError")

    onShareSuccess = Event("onShareSuccess")
    onShareCancel = Event("onShareCancel")
    onShareError = Event("onShareError")

    onUserFetchSuccess = Event("onUserFetchSuccess")
    onUserFetchError = Event("onUserFetchError")

    onProfilePictureLinkGetSuccess = Event("onProfilePictureLinkGetSuccess")  # <- user_id, is_logged, picture_url
    onProfilePictureLinkGetError = Event("onProfilePictureLinkGetError")

    callbacks = {}

    def __init__(self):
        super(SystemiOSFacebook, self).__init__()

    @staticmethod
    def _onAvailable(params):
        return SystemiOSFacebook.is_plugin_active

    def _onInitialize(self):
        callbacks = {
            "oniOSFacebookLoginSuccess": self._cbLoginSuccess,
            "oniOSFacebookLoginCancel": self._cbLoginCancel,
            "oniOSFacebookError": self._cbFacebookError,
            "oniOSFacebookShareSuccess": self._cbShareSuccess,
            "oniOSFacebookShareCancel": self._cbShareCancel,
            "oniOSFacebookShareError": self._cbShareError,
            "oniOSFacebookProfilePictureLinkGetSuccess": self._cbProfilePictureLinkGetSuccess,
            "oniOSFacebookProfilePictureLinkGetError": self._cbProfilePictureLinkGetError,
        }

        Mengine.iOSFacebookSetProvider(callbacks)

        FacebookProvider.setProvider("iOSFacebook", dict(
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
        pass

    def isLoggedIn(self):
        is_logged = Mengine.iOSFacebookIsLoggedIn()
        return is_logged

    def getAccessToken(self):
        token = Mengine.iOSFacebookGetAccessToken()
        return token

    def performLogin(self, permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemiOSFacebook.onLoginSuccess: _cb_success,
            SystemiOSFacebook.onLoginCancel: _cb_cancel,
            SystemiOSFacebook.onLoginError: _cb_error
        }

        SystemiOSFacebook.addCallbacks(callbacks)

        Mengine.iOSFacebookLogin(permissions)

    def shareLink(self, link=None, msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemiOSFacebook.onShareSuccess: _cb_success,
            SystemiOSFacebook.onShareCancel: _cb_cancel,
            SystemiOSFacebook.onShareError: _cb_error
        }

        SystemiOSFacebook.addCallbacks(callbacks)

        Mengine.iOSFacebookShareLink(link, "")

    def logout(self, _cb_success=None, _cb_error=None):
        callbacks = {
            SystemiOSFacebook.onLogoutSuccess: _cb_success,
            SystemiOSFacebook.onLogoutError: _cb_error,
        }

        SystemiOSFacebook.addCallbacks(callbacks)

        access_token = self.getAccessToken()
        Mengine.iOSFacebookLogout()
        self.onLogoutSuccess(access_token)

    def getUser(self, _cb_success=None, _cb_error=None):
        user = Mengine.iOSFacebookGetUser()

        if user is None or user.get("id") is None or user.get("name") is None:
            if _cb_error is not None:
                _cb_error(-1, "iOSFacebook user profile not available")

            return

        picture_url = user.pop("pictureURL", None)

        if picture_url is not None:
            user["picture"] = {
                "data": {
                    "url": picture_url,
                },
            }

        if _cb_success is not None:
            _cb_success(Mengine.encodeJSON(user), "")

    def getProfilePictureLink(self, type_parameter="large", _cb_success=None, _cb_error=None):
        callbacks = {
            SystemiOSFacebook.onProfilePictureLinkGetSuccess: _cb_success,
            SystemiOSFacebook.onProfilePictureLinkGetError: _cb_error
        }

        SystemiOSFacebook.addCallbacks(callbacks)

        Mengine.iOSFacebookGetProfilePictureLink()

    def getProfileUserPictureLink(self, user_id, type_parameter="large", _cb_success=None, _cb_error=None):
        picture_url = "https://graph.facebook.com/{}/picture?type={}".format(user_id, type_parameter)

        if _cb_success is not None:
            _cb_success(user_id, picture_url)

    def _cbLoginSuccess(self, params):
        Trace.msg_dev("[Facebook cb] login success: {!r}".format(params))
        access_token = params.get("authentication.token", self.getAccessToken())
        self.onLoginSuccess(access_token)

    def _cbLoginCancel(self):
        Trace.msg_dev("[Facebook cb] login cancel")
        self.onLoginCancel()

    def _cbFacebookError(self, code, exception):
        Mengine.logError("[Facebook] error [{}]: {}".format(code, exception))
        self.onLoginError(code, exception)

    def _cbShareSuccess(self, post_id):
        Trace.msg_dev("[Facebook cb] share success post_id={}".format(post_id))
        self.onShareSuccess(post_id)

    def _cbShareCancel(self):
        Trace.msg_dev("[Facebook cb] share cancel")
        self.onShareCancel()

    def _cbShareError(self, code, exception):
        Mengine.logError("[Facebook] Share error [{}]: {}".format(code, exception))
        self.onShareError(code, exception)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        Trace.msg_dev("[Facebook cb] ProfilePictureLinkGet success [{}] {}".format(user_id, picture_url))
        self.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, exception):
        Mengine.logError("[Facebook] ProfilePictureLinkGet error [{}]: {}".format(code, exception))
        self.onProfilePictureLinkGetError(code, exception)

    @staticmethod
    def addCallback(event, fn):
        if fn is None:
            return

        def _cb(*args, **kwargs):
            callbacks = SystemiOSFacebook.callbacks.pop(event, None)
            if callbacks is None:
                return

            for cb in callbacks:
                event.removeObserver(cb)

            fn(*args, **kwargs)

        if event not in SystemiOSFacebook.callbacks:
            SystemiOSFacebook.callbacks[event] = []
        SystemiOSFacebook.callbacks[event].append(_cb)
        event += _cb

    @staticmethod
    def addCallbacks(callbacks):
        for event, fn in callbacks.iteritems():
            SystemiOSFacebook.addCallback(event, fn)
