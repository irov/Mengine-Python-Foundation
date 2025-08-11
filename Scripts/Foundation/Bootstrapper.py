from Foundation.BuildModeManager import BuildModeManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager
from Foundation.Managers import Managers
from Foundation.SystemManager import SystemManager


def checkBuildMode(Name, Survey, CE, BuildModeTags):
    """ :returns: True if build mode not match """
    BuildModeVersion = Mengine.getGameParamUnicode("BuildModeCheckVersion")
    BuildMode = Mengine.getGameParamUnicode("BuildMode")

    def _reportFail(build_mode, object_name):
        Trace.msg_dev("[Bootstrapper] (BuildModeCheckVersion {}, BuildMode {!r}) FAIL {!r}"
                      .format(BuildModeVersion, build_mode, object_name))

    # New version of builds resources separations for any type of BuildMode
    # Check BuildModeCheckVersion in Configs.json
    if BuildModeVersion == u"2.0":
        # Check for empty list
        if len(BuildModeTags) == 0:
            return False

        # Get dict BuildMode from BuildModes.xlsx
        resources_tags = BuildModeManager.getBuildResourceConfig(BuildMode)

        # Checking for intersection of sets between [ResourceTags] (BuildModes.xlsx) and [BuildModeTags] (__Any.xlsx)
        if len(set(resources_tags) & set(BuildModeTags)) == 0:
            _reportFail(BuildMode, Name)
            return True

    # Old version of builds resources separations for Survey & CollectorEdition
    else:
        if Mengine.getGameParamBool("Survey", False) is True and Survey == 0:
            _reportFail("Survey", Name)
            return True
        if Mengine.getGameParamBool("CollectorEdition", False) is False and CE == 1:
            _reportFail("StandardEdition", Name)
            return True
        # other cases (CE) are OK (returns False)

    return False


def checkPlatform(platform):
    """ :returns: True if platform is supported """
    if platform is None:
        return True

    # option: -touchpad
    if platform == "MOBILE" or _DEVELOPMENT and platform in ["ANDROID", "IOS"]:
        return Mengine.hasTouchpad() is True
    elif platform == "PC":
        return Mengine.hasTouchpad() is False

    if Mengine.hasPlatformTag(platform) is True:
        return True

    return False


class Bootstrapper(object):
    s_sessionSystems = []

    @staticmethod
    def loadManagers(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            Module = record.get("Module")
            Name = record.get("Name")
            Database = record.get("Database")
            Param = record.get("Param")
            Platform = record.get("Platform")
            Development = record.get("Development")
            Enable = bool(record.get("Enable", True))

            if Enable is False:
                continue

            if Development is not None:
                Development = bool(Development)

            if Database is None:
                Database = "Database"

            if checkPlatform(Platform) is False:
                continue

            if Development is _DEVELOPMENT or Development is None:
                Manager = Managers.importManager(Module, Name)

                if Manager is None:
                    Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s invalid import %s.%s" % (Name, Module, Name))
                    return False

                Trace.msg_dev("Manager.loadParams %s %s" % (Name, Param))

                if Param is not None:
                    result = Manager.loadParams(Database, Param)

                    if isinstance(result, bool) is False:
                        Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s load params mast be return Bool [True|False] but return %s" % (Name, result))
                        return False

                    if result is False:
                        Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s invalid load param %s" % (Name, Param))
                        return False
                    pass
                pass
            pass

        return True

    @staticmethod
    def loadSystems(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        if Managers.importManager("Foundation", "SystemManager") is None:
            Trace.log("Manager", 0, "Bootstrapper.loadSystems invalid initialize system manager")
            return False

        for record in records:
            Module = record.get("Module")
            Name = record.get("Name")
            Global = bool(record.get("Global", False))
            Enable = bool(record.get("Enable", True))
            Development = record.get("Development")
            Platform = record.get("Platform")
            Survey = record.get("Survey", None)
            CE = record.get("CE", None)
            BuildModeTags = record.get("BuildModeTags", [])

            if Enable is False:
                continue

            if checkBuildMode(Name, Survey, CE, BuildModeTags) is True:
                continue

            if checkPlatform(Platform) is False:
                continue

            Trace.msg_dev("load system %s global (%s) development (%s) platform (%s)" % (Name, Global, Development, Platform))

            if SystemManager.importSystem(Module, Name) is None:
                Trace.log("Manager", 0, "Bootstrapper.loadSystems system %s invalid import %s:%s" % (Name, Module, Name))
                return False

            if Development is not None:
                Development = bool(Development)

            if Development is not _DEVELOPMENT and Development is not None:
                continue

            if Global is False:
                Bootstrapper.s_sessionSystems.append(Name)
            else:
                if SystemManager.availableSystem(Name) is False:
                    continue

                if SystemManager.runSystem(Name, Name) is False:
                    Trace.log("Manager", 0, "Bootstrapper.loadSystems system %s invalid run" % Name)
                    return False

        return True

    @staticmethod
    def getSessionSystems():
        return Bootstrapper.s_sessionSystems

    @staticmethod
    def shutdown():
        Bootstrapper.s_sessionSystems = []