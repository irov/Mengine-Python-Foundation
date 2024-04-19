from Foundation.Systems.Facebook.BaseFacebook import BaseFacebook


class AppleFacebook(BaseFacebook):
    name = "Apple"

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
        pass    # todo

    def _isLoggedIn(self):
        pass    # todo

    def _performLogin(self, permissions, _cb_success, _cb_cancel, _cb_error):
        pass    # todo

    def _shareLink(self, link, msg, _cb_success, _cb_cancel, _cb_error):
        pass    # todo

    def _logout(self, _cb_success, _cb_cancel):
        pass    # todo

    def _getUser(self, _cb):
        pass    # todo

    def _getProfilePictureLink(self, type_parameter, _cb):
        pass    # todo

    def _getProfileUserPictureLink(self, user_id, type_parameter, _cb):
        pass    # todo

