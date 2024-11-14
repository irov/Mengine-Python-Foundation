from Foundation.Systems.Facebook.BaseFacebook import BaseFacebook

"""
pythonCall("onFacebookCurrentAccessTokenChanged", oldTokenString, newTokenString);
pythonCall("onFacebookCurrentProfileChanged");

pythonCall("onFacebookLoginSuccess", token);
pythonCall("onFacebookLoginCancel");
pythonCall("onFacebookLoginError", message);

pythonCall("onFacebookLogoutSuccess");
pythonCall("onFacebookLogoutError", message);

pythonCall("onFacebookUserFetchSuccess", objectString, responseString);
pythonCall("onFacebookUserFetchError", message);

pythonCall("onFacebookShareSuccess", postId);
pythonCall("onFacebookShareCancel");
pythonCall("onFacebookShareError", error_message)
;
pythonCall("onFacebookProfilePictureLinkGet", m_facebookUserId, false, "");
pythonCall("onFacebookProfilePictureLinkGet", user_id, false, "");
pythonCall("onFacebookProfilePictureLinkGet", user_id, true, pictureURL);
"""


class AndroidFacebook(BaseFacebook):
    name = "Android"
    plugin_name = "MengineFacebook"

    def _onInitialize(self, system):
        super(AndroidFacebook, self)._onInitialize(system)

        def _setCallback(name, cb):
            Mengine.setAndroidCallback(self.plugin_name, "onFacebook"+name, cb)

        _setCallback("LoginSuccess", self._cbLoginSuccess)
        _setCallback("LoginCancel", self._cbLoginCancel)
        _setCallback("LoginError", self._cbLoginError)
        _setCallback("LogoutSuccess", self._cbLogoutSuccess)
        _setCallback("LogoutError", self._cbLogoutError)
        _setCallback("ShareSuccess", self._cbShareSuccess)
        _setCallback("ShareCancel", self._cbShareCancel)
        _setCallback("ShareError", self._cbShareError)
        _setCallback("UserFetchSuccess", self._cbUserFetchSuccess)
        _setCallback("UserFetchError", self._cbUserFetchError)
        _setCallback("ProfilePictureLinkGetSuccess", self._cbProfilePictureLinkGetSuccess)
        _setCallback("ProfilePictureLinkGetError", self._cbProfilePictureLinkGetError)
        _setCallback("CurrentAccessTokenChanged", self._cbAccessTokenChanged)
        _setCallback("CurrentProfileChanged", self._cbProfileChanged)

    def _onFinalize(self):
        super(AndroidFacebook, self)._onFinalize()

    # provider

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
        token = Mengine.androidStringMethod(self.plugin_name, "getAccessToken")
        return token

    def _isLoggedIn(self):
        is_logged = Mengine.androidBooleanMethod(self.plugin_name, "isLoggedIn")
        return is_logged

    def _login(self, permissions):
        Mengine.androidMethod(self.plugin_name, "performLogin", list(permissions))

    def _shareLink(self, link, msg):
        Mengine.androidMethod(self.plugin_name, "shareLink", link, '', msg)

    def _logout(self):
        Mengine.androidMethod(self.plugin_name, "logout")

    def _getUser(self):
        Mengine.androidMethod(self.plugin_name, "getUser")

    def _getProfilePictureLink(self, type_parameter):
        Mengine.androidMethod(self.plugin_name, "getProfilePictureLink", type_parameter)

    def _getProfileUserPictureLink(self, user_id, type_parameter):
        Mengine.androidMethod(self.plugin_name, "getProfileUserPictureLink", user_id, type_parameter)

    # callbacks

    def _cbLoginSuccess(self, access_token):
        self.system.onLoginSuccess(access_token)

    def _cbLoginCancel(self):
        self.system.onLoginCancel()

    def _cbLoginError(self, code, message):
        self.system.onLoginError(code, message)

    def _cbLogoutSuccess(self):
        self.system.onLogoutSuccess()

    def _cbLogoutError(self, code, message):
        self.system.onLogoutError(code, message)

    def _cbShareSuccess(self, post_id):
        self.system.onShareSuccess(post_id)

    def _cbShareCancel(self):
        self.system.onShareCancel()

    def _cbShareError(self, code, message):
        self.system.onShareError(code, message)

    def _cbUserFetchSuccess(self, object_string, response_string):
        self.system.onUserFetchSuccess(object_string, response_string)

    def _cbUserFetchError(self, code, message):
        self.system.onUserFetchError(code, message)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        self.system.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, message):
        self.system.onProfilePictureLinkGetError(code, message)

    def _cbAccessTokenChanged(self, old_access_token, new_access_token):
        pass

    def _cbProfileChanged(self):
        pass
