from Foundation.DefaultManager import DefaultManager

class AccountManager(object):
    @staticmethod
    def onCreateAccount(accountID, isGlobal):
        pass

    @staticmethod
    def onCreateDefaultAccount():
        DefaultAccount = Mengine.createAccount()

        Mengine.selectAccount(DefaultAccount)
        Mengine.setDefaultAccount(DefaultAccount)

        Mengine.changeCurrentAccountSettingBool("Default", True)
        Mengine.changeCurrentAccountSetting("Name", u"Default")

        DefaultMusicVolume = DefaultManager.getDefaultFloat("DefaultMusicVolume", "0.5")
        Mengine.changeCurrentAccountSetting("MusicVolume", unicode(DefaultMusicVolume))

        DefaultSoundVolume = DefaultManager.getDefaultFloat("DefaultSoundVolume", "0.5")
        Mengine.changeCurrentAccountSetting("SoundVolume", unicode(DefaultSoundVolume))

        DefaultVoiceVolume = DefaultManager.getDefaultFloat("DefaultVoiceVolume", "0.5")
        Mengine.changeCurrentAccountSetting("VoiceVolume", unicode(DefaultVoiceVolume))

        DefaultAccountFullscreen = DefaultManager.getDefaultBool("DefaultAccountFullscreen", False)
        Mengine.changeCurrentAccountSetting("Fullscreen", unicode(DefaultAccountFullscreen))
        #
        DefaultAccountCursor = DefaultManager.getDefaultBool("DefaultAccountCursor", False)
        Mengine.changeCurrentAccountSetting("Cursor", unicode(DefaultAccountCursor))
        #
        DefaultAccountMute = DefaultManager.getDefaultBool("DefaultAccountMute", False)
        Mengine.changeCurrentAccountSetting("Mute", unicode(DefaultAccountMute))

        return DefaultAccount
        pass

    @staticmethod
    def onCreateGlobalAccount():
        GlobalAccount = Mengine.createGlobalAccount()
        Mengine.setGlobalAccount(GlobalAccount)

        Mengine.addGlobalSetting("Name", u"Global", None)
        Mengine.addGlobalSetting("GameVersion", u"1", None)
        Mengine.addGlobalSetting("VersionFiles", u'', None)
        Mengine.addGlobalSetting("VersionDate", u'', None)

        return GlobalAccount
        pass

    @staticmethod
    def onLoadAccounts():
        pass

    staticmethod_onCreateAccount = onCreateAccount
    staticmethod_onCreateAccountExtra = []
    staticmethod_onCreateDefaultAccount = onCreateDefaultAccount
    staticmethod_onCreateDefaultAccountExtra = []
    staticmethod_onCreateGlobalAccount = onCreateGlobalAccount
    staticmethod_onCreateGlobalAccountExtra = []
    staticmethod_onLoadAccounts = onLoadAccounts
    staticmethod_onLoadAccountsExtra = []

    @staticmethod
    def callCreateAccount(accountID, isGlobal):
        AccountManager.staticmethod_onCreateAccount(accountID, isGlobal)

        for method in AccountManager.staticmethod_onCreateAccountExtra:
            method(accountID, isGlobal)
            pass
        pass

    @staticmethod
    def callCreateDefaultAccount():
        AccountID = AccountManager.staticmethod_onCreateDefaultAccount()

        for method in AccountManager.staticmethod_onCreateDefaultAccountExtra:
            method(AccountID)
            pass
        pass

    @staticmethod
    def callCreateGlobalAccount():
        AccountID = AccountManager.staticmethod_onCreateGlobalAccount()

        for method in AccountManager.staticmethod_onCreateGlobalAccountExtra:
            method(AccountID)
            pass
        pass

    @staticmethod
    def callLoadAccounts():
        AccountManager.staticmethod_onLoadAccounts()

        for method in AccountManager.staticmethod_onLoadAccountsExtra:
            method()
            pass
        pass

    @staticmethod
    def setCreateAccount(method):
        AccountManager.staticmethod_onCreateAccount = staticmethod(method)
        pass

    @staticmethod
    def addCreateAccountExtra(method):
        AccountManager.staticmethod_onCreateAccountExtra.append(method)
        pass

    @staticmethod
    def setCreateDefaultAccount(method):
        AccountManager.staticmethod_onCreateDefaultAccount = staticmethod(method)
        pass

    @staticmethod
    def addCreateDefaultAccountExtra(method):
        AccountManager.staticmethod_onCreateDefaultAccountExtra.append(method)
        pass

    @staticmethod
    def setCreateGlobalAccount(method):
        AccountManager.staticmethod_onCreateGlobalAccount = staticmethod(method)
        pass

    @staticmethod
    def addCreateGlobalAccountExtra(method):
        AccountManager.staticmethod_onCreateGlobalAccountExtra.append(method)
        pass

    @staticmethod
    def setLoadAccounts(method):
        AccountManager.staticmethod_onLoadAccounts = staticmethod(method)
        pass

    @staticmethod
    def addLoadAccounts(method):
        AccountManager.staticmethod_onLoadAccountsExtra.append(method)
        pass

    @staticmethod
    def getGameVersion():
        return Mengine.getGlobalSetting('GameVersion')
        pass

    @staticmethod
    def setGameVersion(version):
        Mengine.changeGlobalSetting('GameVersion', version)
        pass

    @staticmethod
    def getVersionFiles():
        return Mengine.getGlobalSettingStrings('VersionFiles')
        pass

    @staticmethod
    def setVersionFiles(version):
        Mengine.changeGlobalSettingStrings('VersionFiles', version)
        pass

    @staticmethod
    def getVersionDate():
        return Mengine.getGlobalSetting('VersionDate')
        pass

    @staticmethod
    def setVersionDate(value):
        Mengine.changeGlobalSetting('VersionDate', value)
        pass
    pass