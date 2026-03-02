from Foundation.System import System
from Foundation.Providers.FacebookProvider import FacebookProvider

ANDROID_PLUGIN_NAME = "AndroidFacebookPlugin"

class SystemAndroidFacebook(System):
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
        super(SystemAndroidFacebook, self).__init__()

    @staticmethod
    def _onAvailable(params):
        return builtins.Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)

    def _onInitialize(self):
        def _setCallback(name, cb):
            builtins.Mengine.addAndroidCallback(ANDROID_PLUGIN_NAME, name, cb)

        _setCallback("onFacebookLoginSuccess", self._cbLoginSuccess)
        _setCallback("onFacebookLoginCancel", self._cbLoginCancel)
        _setCallback("onFacebookLoginError", self._cbLoginError)
        _setCallback("onFacebookLogoutSuccess", self._cbLogoutSuccess)
        _setCallback("onFacebookLogoutError", self._cbLogoutError)
        _setCallback("onFacebookShareSuccess", self._cbShareSuccess)
        _setCallback("onFacebookShareCancel", self._cbShareCancel)
        _setCallback("onFacebookShareError", self._cbShareError)
        _setCallback("onFacebookUserFetchSuccess", self._cbUserFetchSuccess)
        _setCallback("onFacebookUserFetchError", self._cbUserFetchError)
        _setCallback("onFacebookProfilePictureLinkGetSuccess", self._cbProfilePictureLinkGetSuccess)
        _setCallback("onFacebookProfilePictureLinkGetError", self._cbProfilePictureLinkGetError)
        _setCallback("onFacebookCurrentAccessTokenChanged", self._cbAccessTokenChanged)
        _setCallback("onFacebookCurrentProfileChanged", self._cbProfileChanged)

        FacebookProvider.setProvider("AndroidFacebook", dict(
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
        is_logged = builtins.Mengine.androidBooleanMethod(ANDROID_PLUGIN_NAME, "isLoggedIn")
        return is_logged

    def getAccessToken(self):
        token = builtins.Mengine.androidStringMethod(ANDROID_PLUGIN_NAME, "getAccessToken")
        return token

    def performLogin(self, permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onLoginSuccess: _cb_success,
            SystemAndroidFacebook.onLoginCancel: _cb_cancel,
            SystemAndroidFacebook.onLoginError: _cb_error
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "performLogin", list(permissions))

    def shareLink(self, link=None, msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onShareSuccess: _cb_success,
            SystemAndroidFacebook.onShareCancel: _cb_cancel,
            SystemAndroidFacebook.onShareError: _cb_error
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "shareLink", link, '', msg)

    def logout(self, _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onLogoutSuccess: _cb_success,
            SystemAndroidFacebook.onLogoutError: _cb_error,
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "logout")

    def getUser(self, _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onUserFetchSuccess: _cb_success,
            SystemAndroidFacebook.onUserFetchError: _cb_error,
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "getUser")

    def getProfilePictureLink(self, type_parameter="large", _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onProfilePictureLinkGetSuccess: _cb_success,
            SystemAndroidFacebook.onProfilePictureLinkGetError: _cb_error
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "getProfilePictureLink", type_parameter)

    def getProfileUserPictureLink(self, user_id, type_parameter="large", _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAndroidFacebook.onProfilePictureLinkGetSuccess: _cb_success,
            SystemAndroidFacebook.onProfilePictureLinkGetError: _cb_error
        }

        SystemAndroidFacebook.addCallbacks(callbacks)

        builtins.Mengine.androidMethod(ANDROID_PLUGIN_NAME, "getProfileUserPictureLink", user_id, type_parameter)

    def _cbLoginSuccess(self):
        self.onLoginSuccess()

    def _cbLoginCancel(self):
        self.onLoginCancel()

    def _cbLoginError(self, code, exception):
        self.onLoginError(code, exception)

    def _cbLogoutSuccess(self):
        self.onLogoutSuccess()

    def _cbLogoutError(self, code, exception):
        self.onLogoutError(code, exception)

    def _cbShareSuccess(self, post_id):
        self.onShareSuccess(post_id)

    def _cbShareCancel(self):
        self.onShareCancel()

    def _cbShareError(self, code, exception):
        self.onShareError(code, exception)

    def _cbUserFetchSuccess(self, object_string, response_string):
        self.onUserFetchSuccess(object_string, response_string)

    def _cbUserFetchError(self, code, exception):
        self.onUserFetchError(code, exception)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        self.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, exception):
        self.onProfilePictureLinkGetError(code, exception)

    def _cbAccessTokenChanged(self, old_access_token, new_access_token):
        pass

    def _cbProfileChanged(self):
        pass

    @staticmethod
    def addCallback(event, fn):
        if fn is None:
            return

        def _cb(*args, **kwargs):
            callbacks = SystemAndroidFacebook.callbacks.pop(event, None)
            if callbacks is None:
                return

            for cb in callbacks:
                event.removeObserver(cb)

            fn(*args, **kwargs)

        if event not in SystemAndroidFacebook.callbacks:
            SystemAndroidFacebook.callbacks[event] = []
        SystemAndroidFacebook.callbacks[event].append(_cb)
        event += _cb

    @staticmethod
    def addCallbacks(callbacks):
        for event, fn in callbacks.iteritems():
            SystemAndroidFacebook.addCallback(event, fn)
