from Foundation.System import System


class SystemAutoLanguage(System):

    def __init__(self):
        super(SystemAutoLanguage, self).__init__()
        self.disabled = False

    def _onSave(self):
        save = {"disabled": self.disabled}
        return save

    def _onLoad(self, save):
        if Mengine.hasOption("locale") is True:
            self.disabled = True
            return

        if Mengine.hasCurrentAccountSetting("AutoLanguageDisable"):
            self.disabled = Mengine.getCurrentAccountSettingBool("AutoLanguageDisable")
        else:
            self.disabled = save.get("disabled", False)

    def _onRun(self):
        self.addObserver(Notificator.onSelectAccount, self._cbSelectAccount)
        return True

    def _cbSelectAccount(self, account_id):
        if self.disabled is False:
            self.setGameLangAsDevice()
        return True

    def disable(self):
        self.disabled = True
        if Mengine.hasCurrentAccountSetting("AutoLanguageDisable"):
            Mengine.changeCurrentAccountSetting("AutoLanguageDisable", u'True')
            Mengine.saveAccounts()

    @staticmethod
    def getFullDeviceLang():
        """ Returns current device full language code like 'en-US' """
        lang = Mengine.getDeviceLanguage()
        return lang

    @staticmethod
    def getDeviceLangCode():
        """ Returns current device language code like 'en' """
        full_lang = SystemAutoLanguage.getFullDeviceLang()
        locale = full_lang[:2]
        return locale

    def setGameLangAsDevice(self):
        locale = self.getDeviceLangCode()

        if Mengine.getLocale() == locale:
            # already set to this locale
            return

        if Mengine.hasLocale(locale) is False:
            Trace.log("System", 2, "Can't set locale to {} - not exists in game".format(locale))
            return

        # set locale can only work when current scene is None
        if Mengine.getCurrentScene() is None:
            Mengine.setLocale(locale)
        else:
            def cbOnSceneRestartChangeLocale(scene, isActive, isError):
                if scene is None:
                    Mengine.setLocale(locale)

            Mengine.restartCurrentScene(True, cbOnSceneRestartChangeLocale)
