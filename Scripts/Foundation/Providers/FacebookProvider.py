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
    def getAccessToken():
        return FacebookProvider._call("getAccessToken")

    @staticmethod
    def isLoggedIn():
        return FacebookProvider._call("isLoggedIn")

    @staticmethod
    def performLogin(permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        return FacebookProvider._call("performLogin", permissions, _cb_success, _cb_cancel, _cb_error)

    @staticmethod
    def shareLink(link='www.wonderland-games.com', msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
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

    SHARE_POST_ID = "DUMMY_POST_ID"

    class User(object):
        ACCESS_TOKEN = "EAAePSM9uFS4BACZAukJN8n35wZBiKgy09V1Ceg5SpvJDonqGvMdAdPMpiEPOB6hueO8ZAH0ZAZBZAUfDoUfHH6oKVDbRSDc8hTRwHwMp55larG8Cl4liVCmMmD7WcimnPvq5Nv9ySPetwaf2gyA4fmbQLCMtreDrS0ksTEHXdwbJH58sqYwhyOgF9tkM8IZAXNdarWmcNWwgwZDZD"
        AVATAR_URL = "https://bluewaveboats.com/content/test/example-jpeg.jpg"
        USER_ID = "880675035455483"
        USER_EMAIL = "john.snow@gmail.com"
        USER_NAME = "Анатолий Мещеряк"

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

    @staticmethod
    def getAccessToken():
        return DummyFacebook.User.ACCESS_TOKEN

    @staticmethod
    def isLoggedIn():
        return False

    @staticmethod
    def performLogin(permissions=('email', 'public_profile'), _cb_success=None, _cb_cancel=None, _cb_error=None):
        # onFacebookLoginSuccess
        if _cb_success:
            _cb_success(DummyFacebook.User.ACCESS_TOKEN)

    @staticmethod
    def shareLink(link='www.wonderland-games.com', msg='', _cb_success=None, _cb_cancel=None, _cb_error=None):
        # onFacebookShareSuccess
        if _cb_success:
            _cb_success(DummyFacebook.SHARE_POST_ID)

    @staticmethod
    def logout(_cb_success=None, _cb_cancel=None):
        if _cb_success:
            _cb_success()

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
            response.replace("{%id%}", DummyFacebook.User.USER_ID)
            response.replace("{%username%}", DummyFacebook.User.USER_NAME)
            response.replace("{%email%}", DummyFacebook.User.USER_EMAIL)
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


