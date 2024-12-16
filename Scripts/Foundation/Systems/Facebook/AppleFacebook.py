from Foundation.Systems.Facebook.BaseFacebook import BaseFacebook

"""
def_function_args("appleFacebookSetProvider", &Detail::s_AppleFacebook_setProvider );

def_function("appleFacebookLogin", &Detail::s_AppleFacebook_login );
def_function("appleFacebookLogout", &Detail::s_AppleFacebook_logout );
def_function("appleFacebookIsLoggedIn", &Detail::s_AppleFacebook_isLoggedIn );
def_function("appleFacebookGetAccessToken", &Detail::s_AppleFacebook_getAccessToken );
def_function("appleFacebookShareLink", &Detail::s_AppleFacebook_shareLink );
def_function("appleFacebookGetProfilePictureLink", &Detail::s_AppleFacebook_getProfilePictureLink );

this->call_cbs( "onAppleFacebookLoginSuccess", _token );
this->call_cbs( "onAppleFacebookLoginCancel" );
this->call_cbs( "onAppleFacebookError", _code, _errorMessage );
this->call_cbs( "onAppleFacebookShareSuccess", _postId );
this->call_cbs( "onAppleFacebookShareCancel" );
this->call_cbs( "onAppleFacebookShareError", _code, _errorMessage );
this->call_cbs( "onAppleFacebookProfilePictureLinkGet", _userId, _success, _pictureURL );
"""


class AppleFacebook(BaseFacebook):
    name = "Apple"
    plugin_name = "AppleFacebook"

    def _onInitialize(self, system):
        super(AppleFacebook, self)._onInitialize(system)

        callbacks = {
            "onAppleFacebookLoginSuccess": self._cbLoginSuccess,
            "onAppleFacebookLoginCancel": self._cbLoginCancel,
            "onAppleFacebookError": self._cbFacebookError,
            # "onAppleFacebookLogoutCancel": ...,
            # "onAppleFacebookLogoutSuccess": ...,
            # "onAppleFacebookUserFetchSuccess": ...,
            "onAppleFacebookShareSuccess": self._cbShareSuccess,
            "onAppleFacebookShareCancel": self._cbShareCancel,
            "onAppleFacebookShareError": self._cbShareError,
            "onAppleFacebookProfilePictureLinkGetSuccess": self._cbProfilePictureLinkGetSuccess,
            "onAppleFacebookProfilePictureLinkGetError": self._cbProfilePictureLinkGetError,
        }

        Mengine.appleFacebookSetProvider(callbacks)

    def _onFinalize(self):
        super(AppleFacebook, self)._onFinalize()

    def _getProviderMethods(self):
        return dict(
            getAccessToken=self.getAccessToken,
            isLoggedIn=self.isLoggedIn,
            performLogin=self.performLogin,
            shareLink=self.shareLink,
            logout=self.logout,
            getUser=self.getUser,
            getProfilePictureLink=self.getProfilePictureLink,
            getProfileUserPictureLink=self.getProfileUserPictureLink,
        )

    def _getAccessToken(self):
        access_token = Mengine.appleFacebookGetAccessToken()
        return access_token

    def _isLoggedIn(self):
        is_logged = Mengine.appleFacebookIsLoggedIn()
        return is_logged

    def _login(self, permissions):
        is_limited = Mengine.getConfigBool("Facebook", "LimitedLogin", True)
        Mengine.appleFacebookLogin(is_limited, permissions)

    def _shareLink(self, link, msg):
        Mengine.appleFacebookShareLink(link, msg)

    def _logout(self):
        access_token = self.getAccessToken()
        Mengine.appleFacebookLogout()
        self.system.onLogoutSuccess(access_token)

    def _getUser(self):
        Trace.log("Provider", 0, "AppleFacebook getUser not exists")

    def _getProfilePictureLink(self, type_parameter):
        Trace.log("Provider", 0, "AppleFacebook getProfilePictureLink not exists")

    def _getProfileUserPictureLink(self, user_id, type_parameter):
        Mengine.appleFacebookGetProfilePictureLink(user_id, type_parameter)

    # callbacks

    def _cbLoginSuccess(self, params):
        Trace.msg_dev("[Facebook cb] login success: {!r}".format(params))

        access_token = params.get("accessToken")
        auth_token = params.get("authenticationToken")
        fb_id = params.get("profile.userID")
        picture_url = params.get("profile.imageURL")

        self.system.onLoginSuccess(access_token)

    def _cbLoginCancel(self):
        Trace.msg_dev("[Facebook cb] login cancel")
        self.system.onLoginCancel()

    def _cbFacebookError(self, code, message):
        """
            ERROR_LOGIN_TOKEN_FAIL = -1
            ERROR_LOGIN_ERROR = -2
        """
        Mengine.logError("[Facebook] error [{}]: {}".format(code, message))
        self.system.onLoginError(code, message)

    def _cbShareSuccess(self, post_id):
        Trace.msg_dev("[Facebook cb] share success post_id={}".format(post_id))
        self.system.onShareSuccess(post_id)

    def _cbShareCancel(self):
        Trace.msg_dev("[Facebook cb] share cancel")
        self.system.onShareCancel()

    def _cbShareError(self, code, message):
        """
            ERROR_EMPTY_DATA = -1
            ERROR_PICTURE_URL = -2
            ERROR_PICTURE_DATA = -3
            ERROR_PICTURE_CONVERT = -4
        """

        Mengine.logError("[Facebook] Share error [{}]: {}".format(code, message))
        self.system.onShareError(code, message)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        Trace.msg_dev("[Facebook cb] ProfilePictureLinkGet success [{}] {}".format(user_id, picture_url))
        self.system.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, message):
        Mengine.logError("[Facebook] ProfilePictureLinkGet error [{}]: {}".format(code, message))
        self.system.onProfilePictureLinkGetError(code, message)
