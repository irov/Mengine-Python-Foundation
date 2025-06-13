from Foundation.Systems.Facebook.BaseFacebook import BaseFacebook

class AndroidFacebook(BaseFacebook):
    name = "Android"
    plugin_name = "MengineFacebook"

    def _onInitialize(self, system):
        super(AndroidFacebook, self)._onInitialize(system)

        def _setCallback(name, cb):
            Mengine.addAndroidCallback(self.plugin_name, name, cb)

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

    def _cbLoginError(self, code, exception):
        self.system.onLoginError(code, exception)

    def _cbLogoutSuccess(self):
        self.system.onLogoutSuccess()

    def _cbLogoutError(self, code, exception):
        self.system.onLogoutError(code, exception)

    def _cbShareSuccess(self, post_id):
        self.system.onShareSuccess(post_id)

    def _cbShareCancel(self):
        self.system.onShareCancel()

    def _cbShareError(self, code, exception):
        self.system.onShareError(code, exception)

    def _cbUserFetchSuccess(self, object_string, response_string):
        self.system.onUserFetchSuccess(object_string, response_string)

    def _cbUserFetchError(self, code, exception):
        self.system.onUserFetchError(code, exception)

    def _cbProfilePictureLinkGetSuccess(self, user_id, picture_url):
        self.system.onProfilePictureLinkGetSuccess(user_id, picture_url)

    def _cbProfilePictureLinkGetError(self, code, exception):
        self.system.onProfilePictureLinkGetError(code, exception)

    def _cbAccessTokenChanged(self, old_access_token, new_access_token):
        pass

    def _cbProfileChanged(self):
        pass
