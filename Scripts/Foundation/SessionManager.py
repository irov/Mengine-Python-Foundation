from Foundation.Manager import Manager

from Foundation.DefaultManager import DefaultManager
from Foundation.GroupManager import GroupManager
from Foundation.SaveManager import SaveManager
from Foundation.TaskManager import TaskManager

from Session import Session

class SessionManager(Manager):
    s_sessionType = None
    s_currentSession = None
    s_invalidLoad = False
    s_selectAccount = None

    @staticmethod
    def _onInitialize():
        SessionManager.addObserver(Notificator.onSelectAccount, SessionManager.__onSelectAccount)
        SessionManager.addObserver(Notificator.onUnselectAccount, SessionManager.__onUnselectAccount)
        SessionManager.addObserver(Notificator.onDeleteAccount, SessionManager.__onDeleteProfile)

        if Mengine.hasCurrentAccount() is False:
            return

        currentAccountName = Mengine.getCurrentAccountName()
        SessionManager.__onSelectAccount(currentAccountName)
        pass

    @staticmethod
    def _onFinalize():
        pass

    @staticmethod
    def isInvalidLoad():
        return SessionManager.s_invalidLoad

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
        hasSaveStage = Mengine.getCurrentAccountSettingBool("Save")
        if hasSaveStage is False:
            return

        pickleTypes = SaveManager.getPickleTypes()

        AccountID = Mengine.getCurrentAccountName()

        load_session = Mengine.loadAccountPickleFile(AccountID, u"session.dat", pickleTypes)

        if load_session is None:
            Trace.log("Manager", 0, "SessionManager.loadSession pickle_account 'session.dat' is None")

            SessionManager.s_invalidLoad = True

            Notification.notify(Notificator.onSessionLoadInvalid)
            return

        SessionManager.loadSaveData(load_session)
        pass

    @staticmethod
    def removeCurrentSession():
        if SessionManager.s_currentSession is None:
            return False

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

        AccountID = Mengine.getCurrentAccountName()

        if Mengine.writeAccountPickleFile(AccountID, u"session.dat", save_session, pickleTypes) is False:
            Trace.log("Manager", 0, "SessionManager.removeSession write 'session.dat'")

            return False

        Mengine.changeCurrentAccountSettingBool("SessionSave", True)
        Mengine.changeCurrentAccountSettingBool("Save", True)

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

    @staticmethod
    def saveSession():
        if SessionManager.s_currentSession is None:
            Trace.log("Manager", 0, "SessionManager not setup current session")
            return False

        save_session, save_types = SessionManager.getSaveData()

        AccountID = Mengine.getCurrentAccountName()

        if Mengine.writeAccountPickleFile(AccountID, u"session.dat", save_session, save_types) is False:
            Trace.log("Manager", 0, "SessionManager.saveSession can't write 'session.dat'")
            return False

        SessionManager.s_invalidLoad = False

        Mengine.changeCurrentAccountSettingBool("SessionSave", True)
        Mengine.changeCurrentAccountSettingBool("Save", True)

        Mengine.saveAccounts()

        return True

    @staticmethod
    def __onSelectAccount(accountID):
        check = DefaultManager.getDefaultBool("SessionLoadCheck", True)

        if check is False:
            return False

        if accountID == SessionManager.s_selectAccount:
            return False

        SessionManager.selectAccount(accountID, True)

        Notification.notify(Notificator.onSessionNew, accountID)

        return False

    @staticmethod
    def selectAccount(accountID, isLoad):
        Default = Mengine.getCurrentAccountSettingBool("Default")

        if Default is True:
            return False

        if SessionManager.s_sessionType is None:
            return False

        newSession = SessionManager.s_sessionType()

        SessionManager.s_currentSession = newSession

        if newSession.onInitialize(accountID) is False:
            return False

        newSession.onRun()

        SessionManager.s_selectAccount = accountID

        if isLoad is True:
            if Mengine.hasCurrentAccountSetting("SessionSave") is True:
                SessionSave = Mengine.getCurrentAccountSettingBool("SessionSave")
                if SessionSave is True:
                    SessionManager.loadSession()
                    pass
                pass
            pass

        return False

    @staticmethod
    def __onDeleteProfile(accountID):
        SessionManager.removeCurrentSession()

        return False

    @staticmethod
    def __onUnselectAccount(accountID):
        SessionManager.removeCurrentSession()

        return False

    @staticmethod
    def setSessionType(type):
        if issubclass(type, Session) is False:
            Trace.log("Manager", 0, "SessionManager.setSessionType: not subclass of session !!!!")
            pass

        SessionManager.s_sessionType = type
        pass
    pass