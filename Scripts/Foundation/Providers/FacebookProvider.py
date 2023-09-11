from Foundation.Providers.BaseProvider import BaseProvider


class FacebookProvider(BaseProvider):
    s_allowed_methods = [
        "getAccessToken"
        , "isLoggedIn"
        , "performLogin"
        , "shareLink"
        , "logout"
        , "getUser"
        , "getProfilePictureLink"
        , "getProfileUserPictureLink"
    ]

    @staticmethod
    def _setDevProvider():
        DummyFacebook.setProvider()

    @staticmethod
    def getConfigShareLink():
        return Mengine.getConfigString("Facebook", "ShareLink", "https://www.wonderland-games.com")

    @staticmethod
    def getAccessToken():
        return FacebookProvider._call("getAccessToken")

    @staticmethod
    def isLoggedIn():
        return FacebookProvider._call("isLoggedIn")

    @staticmethod
    def performLogin(permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        return FacebookProvider._call("performLogin", permissions, _cb_success, _cb_cancel, _cb_error)

    @staticmethod
    def shareLink(link=None, msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        if link is None:
            link = FacebookProvider.getConfigShareLink()
        return FacebookProvider._call("shareLink", link, msg, _cb_success, _cb_cancel, _cb_error)

    @staticmethod
    def logout(_cb_success=None, _cb_cancel=None):
        return FacebookProvider._call("logout", _cb_success, _cb_cancel)

    @staticmethod
    def getUser(_cb=None):
        return FacebookProvider._call("getUser", _cb)

    @staticmethod
    def getProfilePictureLink(type_parameter="?type=large", _cb=None):
        return FacebookProvider._call("getProfilePictureLink", type_parameter, _cb)

    @staticmethod
    def getProfileUserPictureLink(user_id, type_parameter="?type=large", _cb=None):
        return FacebookProvider._call("getProfileUserPictureLink", user_id, type_parameter, _cb)


class DummyFacebook(object):

    _logged_in = False
    SHARE_POST_ID = "DUMMY_POST_ID"

    class User(object):
        ACCESS_TOKEN = Mengine.getConfigString("Facebook", "DebugAccessToken", "123456789token")
        AVATAR_URL = Mengine.getConfigString("Facebook", "DebugAvatarUrl", "https://bluewaveboats.com/content/test/example-jpeg.jpg")
        USER_ID = Mengine.getConfigString("Facebook", "DebugUserId", "123456789")
        USER_EMAIL = Mengine.getConfigString("Facebook", "DebugUserEmail", "wonderland.playfab@gmail.com")
        USER_NAME = Mengine.getConfigString("Facebook", "DebugUserName", "Test User")

    @staticmethod
    def setProvider():
        FacebookProvider.setProvider("Dummy", dict(
            getAccessToken=DummyFacebook.getAccessToken,
            isLoggedIn=DummyFacebook.isLoggedIn,
            performLogin=DummyFacebook.performLogin,
            shareLink=DummyFacebook.shareLink,
            logout=DummyFacebook.logout,
            getUser=DummyFacebook.getUser,
            getProfilePictureLink=DummyFacebook.getProfilePictureLink,
            getProfileUserPictureLink=DummyFacebook.getProfileUserPictureLink,
        ))

        DummyFacebook._logged_in = Mengine.getConfigBool("Facebook", "DebugStartLoggedIn", False)

    @staticmethod
    def getAccessToken():
        return DummyFacebook.User.ACCESS_TOKEN

    @staticmethod
    def isLoggedIn():
        return DummyFacebook._logged_in

    @staticmethod
    def performLogin(permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        # onFacebookLoginSuccess
        if _cb_success:
            _cb_success(DummyFacebook.User.ACCESS_TOKEN)
        DummyFacebook._logged_in = True

    @staticmethod
    def shareLink(link=None, msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        if link is None:
            link = FacebookProvider.getConfigShareLink()
        # onFacebookShareSuccess
        if _cb_success:
            _cb_success(DummyFacebook.SHARE_POST_ID)

    @staticmethod
    def logout(_cb_success=None, _cb_cancel=None):
        if _cb_success:
            _cb_success()
        DummyFacebook._logged_in = False

    @staticmethod
    def getUser(_cb=None):
        # onFacebookUserFetchSuccess
        if _cb:
            response = """{
  "id": "{%id%}",
  "name": "{%username%}",
  "email": "{%email%}",
  "picture": {
    "data": {
      "height": 50,
      "is_silhouette": false,
      "url": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid={%id%}&height=50&width=50&ext=1558537422&hash=AeQECYFQWfJdaYGp",
      "width": 50
    }
  }
}"""
            response = response.replace("{%id%}", DummyFacebook.User.USER_ID)
            response = response.replace("{%username%}", DummyFacebook.User.USER_NAME)
            response = response.replace("{%email%}", DummyFacebook.User.USER_EMAIL)
            _cb(response, "")

    @staticmethod
    def getProfilePictureLink(type_parameter="?type=large", _cb=None):
        # onFacebookProfilePictureLinkGet
        if _cb:
            _cb("", False, DummyFacebook.User.AVATAR_URL)

    @staticmethod
    def getProfileUserPictureLink(user_id, type_parameter="?type=large", _cb=None):
        if _cb:
            _cb("", False, DummyFacebook.User.AVATAR_URL)


