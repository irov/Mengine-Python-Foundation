from GOAP2.DefaultManager import DefaultManager
from GOAP2.GroupManager import GroupManager
from GOAP2.SaveManager import SaveManager
from GOAP2.TaskManager import TaskManager
from Notification import Notification
from Session import Session

class SessionManager(object):
    s_onSelectAccountObserver = None
    s_onUnselectAccountObserver = None
    s_onDeleteProfileObserver = None
    s_sessionType = None
    s_currentSession = None
    s_invalidLoad = False
    s_selectAccount = None

    @staticmethod
    def onInitialize():
        SessionManager.s_onSelectAccountObserver = Notification.addObserver(Notificator.onSelectAccount, SessionManager.__onSelectAccount)
        SessionManager.s_onUnselectAccountObserver = Notification.addObserver(Notificator.onUnselectAccount, SessionManager.__onUnselectAccount)
        SessionManager.s_onDeleteProfileObserver = Notification.addObserver(Notificator.onDeleteAccount, SessionManager.__onDeleteProfile)

        if Menge.hasCurrentAccount() is False:
            return
            pass

        currentAccountName = Menge.getCurrentAccountName()
        SessionManager.__onSelectAccount(currentAccountName)
        pass

    @staticmethod
    def onFinalize():
        Notification.removeObserver(SessionManager.s_onSelectAccountObserver)
        Notification.removeObserver(SessionManager.s_onUnselectAccountObserver)
        Notification.removeObserver(SessionManager.s_onDeleteProfileObserver)

        SessionManager.s_onSelectAccountObserver = None
        SessionManager.s_onSelectAccountObserver = None
        SessionManager.s_onDeleteProfileObserver = None
        pass

    @staticmethod
    def isInvalidLoad():
        return SessionManager.s_invalidLoad
        pass

    @staticmethod
    def loadSaveData(load_session):
        load_global, load_groups = load_session

        dict_global = SaveManager._loadParams(load_global)
        Notification.notify(Notificator.onSessionLoad, dict_global)

        for load_group in load_groups:
            SaveManager.loadGroup(load_group)
            pass

        Notification.notify(Notificator.onSessionLoadComplete)
        pass

    @staticmethod
    def loadSession():
        hasSaveStage = Menge.getCurrentAccountSettingBool("Save")
        if hasSaveStage is False:
            return
            pass

        pickleTypes = SaveManager.getPickleTypes()

        AccountID = Menge.getCurrentAccountName()

        load_session = Menge.loadAccountPickleFile(AccountID, u"session.dat", pickleTypes)

        if load_session is None:
            Trace.log("Manager", 0, "SessionManager.loadSession pickle_account 'session.dat' is None")

            SessionManager.s_invalidLoad = True

            Notification.notify(Notificator.onSessionLoadInvalid)
            return
            pass

        SessionManager.loadSaveData(load_session)
        pass

    @staticmethod
    def removeCurrentSession():
        if SessionManager.s_currentSession is None:
            return False
            pass

        Notification.notify(Notificator.onSessionRemove)

        # dict_systems = {}
        # SystemManager.saveSystems(dict_systems)

        # save_systems = SaveManager._saveParams(dict_systems)

        dict_global = {}
        Notification.notify(Notificator.onSessionSave, dict_global)

        save_global = SaveManager._saveParams(dict_global)

        SessionManager.s_currentSession.onStop()
        SessionManager.s_currentSession.onFinalize()
        SessionManager.s_currentSession = None

        save_groups = SaveManager.saveGroups()

        save_session = (save_global, save_groups)

        SessionManager.s_invalidLoad = False

        pickleTypes = SaveManager.getPickleTypes()

        AccountID = Menge.getCurrentAccountName()

        if Menge.writeAccountPickleFile(AccountID, u"session.dat", save_session, pickleTypes) is False:
            Trace.log("Manager", 0, "SessionManager.removeSession write 'session.dat'")

            return False
            pass

        Menge.changeCurrentAccountSetting("SessionSave", unicode(True))
        Menge.changeCurrentAccountSetting("Save", unicode(True))

        GroupManager.reloadGroups()
        SessionManager.s_selectAccount = None

        TaskManager.skipTasks(skipGlobal=False)

        Notification.notify(Notificator.onSessionRemoveComplete)
        pass

    @staticmethod
    def getSaveData():
        dict_global = {}
        Notification.notify(Notificator.onSessionSave, dict_global)

        save_global = SaveManager._saveParams(dict_global)
        save_groups = SaveManager.saveGroups()
        save_session = (save_global, save_groups)

        save_types = SaveManager.getPickleTypes()

        return (save_session, save_types)
        pass

    @staticmethod
    def saveSession():
        if SessionManager.s_currentSession is None:
            # Trace.log("Manager", 0, "SessionManager not setup current session")
            return False
            pass

        save_session, save_types = SessionManager.getSaveData()

        AccountID = Menge.getCurrentAccountName()

        if Menge.writeAccountPickleFile(AccountID, u"session.dat", save_session, save_types) is False:
            Trace.log("Manager", 0, "SessionManager.saveSession can't write 'session.dat'")
            return False
            pass

        SessionManager.s_invalidLoad = False

        Menge.changeCurrentAccountSetting("SessionSave", unicode(True))
        Menge.changeCurrentAccountSetting("Save", unicode(True))

        Menge.saveAccounts()

        return True
        pass

    @staticmethod
    def __onSelectAccount(accountID):
        check = DefaultManager.getDefaultBool("SessionLoadCheck", True)

        if check is False:
            return False
            pass

        if accountID == SessionManager.s_selectAccount:
            return False
            pass

        SessionManager.selectAccount(accountID, True)

        Notification.notify(Notificator.onSessionNew, accountID)

        return False
        pass

    @staticmethod
    def selectAccount(accountID, isLoad):
        Default = Menge.getCurrentAccountSettingBool("Default")

        if Default is True:
            return False
            pass

        if SessionManager.s_sessionType is None:
            return False
            pass

        newSession = SessionManager.s_sessionType()

        SessionManager.s_currentSession = newSession

        if newSession.onInitialize(accountID) is False:
            return False
            pass

        newSession.onRun()

        SessionManager.s_selectAccount = accountID

        if isLoad is True:
            if Menge.hasCurrentAccountSetting("SessionSave") is True:
                SessionSave = Menge.getCurrentAccountSettingBool("SessionSave")
                if SessionSave is True:
                    SessionManager.loadSession()
                    pass
                pass
            pass

        return False
        pass

    @staticmethod
    def __onDeleteProfile(accountID):
        SessionManager.removeCurrentSession()

        return False
        pass

    @staticmethod
    def __onUnselectAccount(accountID):
        SessionManager.removeCurrentSession()

        return False
        pass

    @staticmethod
    def setSessionType(type):
        if issubclass(type, Session) is False:
            Trace.log("Manager", 0, "SessionManager.setSessionType: not subclass of session !!!!")
            pass

        SessionManager.s_sessionType = type
        pass
    pass