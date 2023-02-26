from Foundation.DefaultManager import DefaultManager

class AccountManager(object):
    @staticmethod
    def onCreateAccount(accountID, isGlobal):
        pass

    @staticmethod
    def onCreateDefaultAccount():
        DefaultAccount = Menge.createAccount()

        Menge.selectAccount(DefaultAccount)
        Menge.setDefaultAccount(DefaultAccount)

        Menge.changeCurrentAccountSettingBool("Default", True)
        Menge.changeCurrentAccountSetting("Name", u"Default")

        DefaultMusicVolume = DefaultManager.getDefaultFloat("DefaultMusicVolume", "0.5")
        Menge.changeCurrentAccountSetting("MusicVolume", unicode(DefaultMusicVolume))

        DefaultSoundVolume = DefaultManager.getDefaultFloat("DefaultSoundVolume", "0.5")
        Menge.changeCurrentAccountSetting("SoundVolume", unicode(DefaultSoundVolume))

        DefaultVoiceVolume = DefaultManager.getDefaultFloat("DefaultVoiceVolume", "0.5")
        Menge.changeCurrentAccountSetting("VoiceVolume", unicode(DefaultVoiceVolume))

        DefaultAccountFullscreen = DefaultManager.getDefaultBool("DefaultAccountFullscreen", False)
        Menge.changeCurrentAccountSetting("Fullscreen", unicode(DefaultAccountFullscreen))
        #
        DefaultAccountCursor = DefaultManager.getDefaultBool("DefaultAccountCursor", False)
        Menge.changeCurrentAccountSetting("Cursor", unicode(DefaultAccountCursor))
        #
        DefaultAccountMute = DefaultManager.getDefaultBool("DefaultAccountMute", False)
        Menge.changeCurrentAccountSetting("Mute", unicode(DefaultAccountMute))

        return DefaultAccount
        pass

    @staticmethod
    def onCreateGlobalAccount():
        GlobalAccount = Menge.createGlobalAccount()
        Menge.setGlobalAccount(GlobalAccount)

        Menge.addGlobalSetting("Name", u"Global", None)
        Menge.addGlobalSetting("GameVersion", u"1", None)
        Menge.addGlobalSetting("VersionFiles", u'', None)
        Menge.addGlobalSetting("VersionDate", u'', None)

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
        return Menge.getGlobalSetting('GameVersion')
        pass

    @staticmethod
    def setGameVersion(version):
        Menge.changeGlobalSetting('GameVersion', version)
        pass

    @staticmethod
    def getVersionFiles():
        return Menge.getGlobalSettingStrings('VersionFiles')
        pass

    @staticmethod
    def setVersionFiles(version):
        Menge.changeGlobalSettingStrings('VersionFiles', version)
        pass

    @staticmethod
    def getVersionDate():
        return Menge.getGlobalSetting('VersionDate')
        pass

    @staticmethod
    def setVersionDate(value):
        Menge.changeGlobalSetting('VersionDate', value)
        pass
    pass