import builtins

from Event import Event
from Foundation.System import System
from Foundation.Providers.FacebookProvider import FacebookProvider

APPLE_PLUGIN_NAME = "AppleFacebookPlugin"

class SystemAppleFacebook(System):
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
        super(SystemAppleFacebook, self).__init__()

    @staticmethod
    def _onAvailable(params):
        return builtins.Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)

    def _onInitialize(self):
        callbacks = {
            "onAppleFacebookLoginSuccess": self._cbLoginSuccess,
            "onAppleFacebookLoginCancel": self._cbLoginCancel,
            "onAppleFacebookError": self._cbFacebookError,
            "onAppleFacebookShareSuccess": self._cbShareSuccess,
            "onAppleFacebookShareCancel": self._cbShareCancel,
            "onAppleFacebookShareError": self._cbShareError,
            "onAppleFacebookProfilePictureLinkGetSuccess": self._cbProfilePictureLinkGetSuccess,
            "onAppleFacebookProfilePictureLinkGetError": self._cbProfilePictureLinkGetError,
        }

        builtins.Mengine.appleFacebookSetProvider(callbacks)

        FacebookProvider.setProvider("AppleFacebook", dict(
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
        is_logged = builtins.Mengine.appleFacebookIsLoggedIn()
        return is_logged

    def getAccessToken(self):
        token = builtins.Mengine.appleFacebookGetAccessToken()
        return token

    def performLogin(self, permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onLoginSuccess: _cb_success,
            SystemAppleFacebook.onLoginCancel: _cb_cancel,
            SystemAppleFacebook.onLoginError: _cb_error
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        is_limited = builtins.Mengine.getConfigBool("Facebook", "LimitedLogin", True)
        builtins.Mengine.appleFacebookLogin(is_limited, permissions)

    def shareLink(self, link=None, msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onShareSuccess: _cb_success,
            SystemAppleFacebook.onShareCancel: _cb_cancel,
            SystemAppleFacebook.onShareError: _cb_error
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        builtins.Mengine.appleFacebookShareLink(link, msg)

    def logout(self, _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onLogoutSuccess: _cb_success,
            SystemAppleFacebook.onLogoutError: _cb_error,
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        access_token = self.getAccessToken()
        builtins.Mengine.appleFacebookLogout()
        self.onLogoutSuccess(access_token)

    def getUser(self, _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onUserFetchSuccess: _cb_success,
            SystemAppleFacebook.onUserFetchError: _cb_error,
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        builtins.Trace.log("Provider", 0, "AppleFacebook getUser not exists")

    def getProfilePictureLink(self, type_parameter="large", _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onProfilePictureLinkGetSuccess: _cb_success,
            SystemAppleFacebook.onProfilePictureLinkGetError: _cb_error
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        builtins.Trace.log("Provider", 0, "AppleFacebook getProfilePictureLink not exists")

    def getProfileUserPictureLink(self, user_id, type_parameter="large", _cb_success=None, _cb_error=None):
        callbacks = {
            SystemAppleFacebook.onProfilePictureLinkGetSuccess: _cb_success,
            SystemAppleFacebook.onProfilePictureLinkGetError: _cb_error
        }

        SystemAppleFacebook.addCallbacks(callbacks)

        builtins.Mengine.appleFacebookGetProfilePictureLink(user_id, type_parameter)

    def _cbLoginSuccess(self, params):
        builtins.Trace.msg_dev("[Facebook cb] login success: {!r}".format(params))
        self.onLoginSuccess()

    def _cbLoginCancel(self):
        builtins.Trace.msg_dev("[Facebook cb] login cancel")
        self.onLoginCancel()

    def _cbFacebookError(self, code, exception):
        builtins.Mengine.logError("[Facebook] error [{}]: {}".format(code, exception))
        self.onLoginError(code, exception)

    def _cbShareSuccess(self, post_id):
        builtins.Trace.msg_dev("[Facebook cb] share success post_id={}".format(post_id))
        self.onShareSuccess(post_id)

    def _cbShareCancel(self):
        builtins.Trace.msg_dev("[Facebook cb] share cancel")
        self.onShareCancel()

    def _cbShareError(self, code, exception):
        builtins.Mengine.logError("[Facebook] Share error [{}]: {}".format(code, exception))
        self.onShareError(code, exception)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        builtins.Trace.msg_dev("[Facebook cb] ProfilePictureLinkGet success [{}] {}".format(user_id, picture_url))
        self.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, exception):
        builtins.Mengine.logError("[Facebook] ProfilePictureLinkGet error [{}]: {}".format(code, exception))
        self.onProfilePictureLinkGetError(code, exception)

    @staticmethod
    def addCallback(event, fn):
        if fn is None:
            return

        def _cb(*args, **kwargs):
            callbacks = SystemAppleFacebook.callbacks.pop(event, None)
            if callbacks is None:
                return

            for cb in callbacks:
                event.removeObserver(cb)

            fn(*args, **kwargs)

        if event not in SystemAppleFacebook.callbacks:
            SystemAppleFacebook.callbacks[event] = []
        SystemAppleFacebook.callbacks[event].append(_cb)
        event += _cb

    @staticmethod
    def addCallbacks(callbacks):
        for event, fn in callbacks.iteritems():
            SystemAppleFacebook.addCallback(event, fn)
