from Foundation.System import System
from Foundation.Providers.FacebookProvider import FacebookProvider
from Event import Event


PLUGIN_NAME = "Facebook"


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

    def _onInitialize(self):
        if Mengine.isAvailablePlugin(PLUGIN_NAME) is False:
            return

        if _ANDROID:
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookLoginSuccess", self.onLoginSuccess)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookLoginCancel", self.onLoginCancel)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookLoginError", self.onLoginError)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookLogoutCancel", self.onLogoutCancel)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookLogoutSuccess", self.onLogoutSuccess)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookUserFetchSuccess", self.onUserFetchSuccess)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookShareSuccess", self.onShareSuccess)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookShareCancel", self.onShareCancel)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookShareError", self.onShareError)
            Mengine.setAndroidCallback(PLUGIN_NAME, "onFacebookProfilePictureLinkGet", self.onProfilePictureLinkGet)

            FacebookProvider.setProvider("Android", dict(
                getAccessToken=SystemFacebook.getAccessToken,
                isLoggedIn=SystemFacebook.isLoggedIn,
                performLogin=SystemFacebook.performLogin,
                shareLink=SystemFacebook.shareLink,
                logout=SystemFacebook.logout,
                getUser=SystemFacebook.getUser,
                getProfilePictureLink=SystemFacebook.getProfilePictureLink,
                getProfileUserPictureLink=SystemFacebook.getProfileUserPictureLink,
            ))

    @staticmethod
    def isLoggedIn():
        is_logged = Mengine.androidBooleanMethod(PLUGIN_NAME, "isLoggedIn")
        return is_logged

    @staticmethod
    def getAccessToken():
        token = Mengine.androidStringMethod(PLUGIN_NAME, "getAccessToken")
        return token

    @staticmethod
    def performLogin(permissions=('email', 'public_profile'),
                     _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemFacebook.onLoginSuccess: _cb_success,
            SystemFacebook.onLoginCancel: _cb_cancel,
            SystemFacebook.onLoginError: _cb_error
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)

        Mengine.androidMethod(PLUGIN_NAME, "performLogin", list(permissions))

    @staticmethod
    def shareLink(link=None, msg='',
                  _cb_success=None, _cb_cancel=None, _cb_error=None):
        callbacks = {
            SystemFacebook.onShareSuccess: _cb_success,
            SystemFacebook.onShareCancel: _cb_cancel,
            SystemFacebook.onShareError: _cb_error
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)
        Mengine.androidMethod(PLUGIN_NAME, "shareLink", link, '', msg)

    @staticmethod
    def logout(_cb_success=None, _cb_cancel=None):
        callbacks = {
            SystemFacebook.onLogoutSuccess: _cb_success,
            SystemFacebook.onLogoutCancel: _cb_cancel,
        }

        for _event, _cb in callbacks.iteritems():
            if _cb is not None:
                SystemFacebook.addCallback(_event, _cb)
        Mengine.androidMethod(PLUGIN_NAME, "logout")

    @staticmethod
    def getUser(_cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onUserFetchSuccess, _cb)
        Mengine.androidMethod(PLUGIN_NAME, "getUser")

    @staticmethod
    def getProfilePictureLink(type_parameter="?type=large", _cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onProfilePictureLinkGet, _cb)
        Mengine.androidMethod(PLUGIN_NAME, "getProfilePictureLink", type_parameter)

    @staticmethod
    def getProfileUserPictureLink(user_id, type_parameter="?type=large", _cb=None):
        if _cb is not None:
            SystemFacebook.addCallback(SystemFacebook.onProfilePictureLinkGet, _cb)
        Mengine.androidMethod(PLUGIN_NAME, "getProfileUserPictureLink", user_id, type_parameter)

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
