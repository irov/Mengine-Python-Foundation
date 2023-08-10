from Foundation.AccountManager import AccountManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Systems.SystemAnalytics import SystemAnalytics
from Foundation.System import System

GDPR_ACCOUNT_KEY = "AgreeWithGDPR"


class SystemGDPR(System):
    """ General Data Protection Regulation """

    privacy_policy_link = None
    gdpr_group_name = None
    is_default_provider = True

    def __initAccountParam(self):
        def __addExtraAccountSettings(accountID, isGlobal):
            if isGlobal is True:
                return
            Mengine.addCurrentAccountSetting(GDPR_ACCOUNT_KEY, u'False', None)

        AccountManager.addCreateAccountExtra(__addExtraAccountSettings)

    def _onInitialize(self):
        SystemGDPR.is_default_provider = DefaultManager.getDefaultBool("UseDefaultGDPRProvider", True)

        if SystemGDPR.is_default_provider is False:
            return

        SystemGDPR.privacy_policy_link = Mengine.getGameParamUnicode("PrivacyPolicyLink") or None
        if SystemGDPR.privacy_policy_link is None:
            self.initializeFailed("SystemGDPR needs PrivacyPolicyLink in Configs.json in section 'Params'")

        SystemGDPR.gdpr_group_name = DefaultManager.getDefault("DefaultGDPRComplianceGroupName", "GDPRCompliance")
        if SystemGDPR.gdpr_group_name is None:
            self.initializeFailed("SystemGDPR GroupName is None")

        self.__initAccountParam()

    @staticmethod
    def isUserAgreeWithGDPR():
        agree = Mengine.getCurrentAccountSettingBool(GDPR_ACCOUNT_KEY)
        return agree

    @staticmethod
    def _setUserAgreeWithGDPR(state):
        Mengine.changeCurrentAccountSettingBool(GDPR_ACCOUNT_KEY, state)
        Mengine.saveAccounts()
        if state is True:
            SystemAnalytics.sendCustomAnalytic("gdpr_agree", {})
        else:
            SystemAnalytics.sendCustomAnalytic("gdpr_disagree", {})

    def _onRun(self):
        if SystemGDPR.is_default_provider is False:
            return True

        self.addObserver(Notificator.onSceneActivate, self._cbSceneActivate)
        self.addObserver(Notificator.onGetRemoteConfig, self._cbGetRemoteConfig)
        return True

    def _cbGetRemoteConfig(self, key, url):
        if key != "privacy_policy_link":
            return False

        if isinstance(url, str) is False:
            return False
        if url.startswith("http://") is False and url.startswith("https://") is False:
            return False

        SystemGDPR.privacy_policy_link = url

        return False

    def _cbSceneActivate(self, scene_name):
        if scene_name != "Menu":
            return False

        if self.isUserAgreeWithGDPR() is True:
            return True

        self.runTaskChain()
        return False

    def runTaskChain(self):
        alpha_time = 250.0

        SystemAnalytics.sendCustomAnalytic("gdpr_request", {
            "GroupName": self.gdpr_group_name,
            "Link": str(self.privacy_policy_link),
        })

        if self.existTaskChain(Name="GDPRCompliance"):
            self.removeTaskChain(Name="GDPRCompliance")
        with self.createTaskChain(Name="GDPRCompliance") as tc:
            with tc.addParallelTask(2) as (fade, ui):
                fade.addTask("AliasFadeIn", FadeGroupName="FadeUI", To=1, Time=1)
                ui.addTask("TaskSceneLayerGroupEnable", LayerName=self.gdpr_group_name, Value=True)

            event_button_click = Event("onButtonClick")
            with tc.addParallelTask(2) as (buttons, link):
                buttons.addScope(self._scopeButtonsHandler, event_button_click)
                link.addScope(self._scopeLinkHandler, event_button_click)

            with tc.addParallelTask(2) as (fade, ui):
                fade.addTask("AliasFadeOut", FadeGroupName="FadeUI", From=1, Time=alpha_time)
                ui.addTask("TaskSceneLayerGroupEnable", LayerName=self.gdpr_group_name, Value=False)

    def _scopeButtonsHandler(self, source, event_button_click):
        with source.addRaceTask(2) as (yes, no):
            yes.addTask("TaskMovie2ButtonClick", GroupName=self.gdpr_group_name, Movie2ButtonName="Movie2Button_Ok")
            yes.addFunction(event_button_click)
            yes.addFunction(self._setUserAgreeWithGDPR, True)

            no.addTask("TaskMovie2ButtonClick", GroupName=self.gdpr_group_name, Movie2ButtonName="Movie2Button_No")
            no.addFunction(event_button_click)
            no.addFunction(self._setUserAgreeWithGDPR, False)
            no.addTask("TaskQuitApplication")

    def _scopeLinkHandler(self, source, event_button_click):
        with source.addRepeatTask() as (repeat, until):
            repeat.addTask("TaskMovie2SocketClick", GroupName=self.gdpr_group_name,
                           Movie2Name="Movie2_Window", SocketName="link")
            repeat.addFunction(SystemAnalytics.sendCustomAnalytic, "gdpr_read", {"link": self.privacy_policy_link})
            repeat.addFunction(Mengine.openUrlInDefaultBrowser, self.privacy_policy_link)

            until.addEvent(event_button_click)
