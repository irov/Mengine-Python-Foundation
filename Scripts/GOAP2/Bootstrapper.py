from GOAP2.BuildModeManager import BuildModeManager
from GOAP2.DatabaseManager import DatabaseManager
from GOAP2.Manager import Manager
from GOAP2.SystemManager import SystemManager

def checkBuildMode(Name, Survey, CE, BuildModeTags):
    BuildModeVersion = Menge.getGameParamUnicode("BuildModeCheckVersion")
    BuildMode = Menge.getGameParamUnicode("BuildMode")

    def printBuildMode(Mode, Name):
        if _DEVELOPMENT is True:
            Trace.msg("-=| BuildMode {} {}: disable {}".format(BuildModeVersion, Mode, Name))

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
            printBuildMode(BuildMode, Name)
            return True

    # Old version of builds resources separations for Survey & CollectorEdition
    else:
        survey_build = Menge.getGameParamBool("Survey", False)
        ce_build = Menge.getGameParamBool("CollectorEdition", False)

        # For Survey
        if survey_build is True and Survey == 0:
            printBuildMode("Survey", Name)
            return True

        # For StandartEdition
        if ce_build is False and CE == 1:
            printBuildMode("StandartEdition", Name)
            return True

    return False

def checkPlatform(platform):
    if platform is None:
        return True

    # option: -touchpad
    if platform == "MOBILE" or _DEVELOPMENT and platform in ["ANDROID", "IOS"]:
        return Menge.hasTouchpad() is True
    elif platform == "PC":
        return Menge.hasTouchpad() is False

    if Menge.hasPlatformTag(platform) is True:
        return True

    return False

class Bootstrapper(object):
    s_sessionSystems = []
    s_managers = {}

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
                Manager = Bootstrapper.__importManager(Module, Name)

                if Manager is None:
                    Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s invalid import %s.%s" % (Name, Module, Name))
                    return False

                if _DEVELOPMENT is True:
                    print
                    "Manager.loadParams %s %s" % (Name, Param)

                if Param is not None:
                    result = Manager.loadParams(Database, Param)

                    if isinstance(result, bool) is False:
                        Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s load params mast be return Bool [True|False] but return %s" % (Name, result))
                        return False

                    if result is False:
                        Trace.log("Manager", 0, "Bootstrapper.loadManagers manager %s invalid load param %s" % (Name, Param))
                        return False

        return True

    @staticmethod
    def __importManager(module, name):
        manager = Bootstrapper.s_managers.get(name)

        if manager is not None:
            return manager

        new_manager = Utils.importType(module, name)

        if new_manager is None:
            Trace.log("Manager", 0, "Bootstrapper.importManager: invalid import %s:%s" % (module, name))

            return None

        if issubclass(new_manager, Manager) is True:
            if new_manager.onInitialize() is False:
                Trace.log("Manager", 0, "Bootstrapper.importManager: manager '%s' invalid initialize" % name)

                return None

        Bootstrapper.s_managers[name] = new_manager

        return new_manager

    @staticmethod
    def loadSystems(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        if SystemManager.onInitialize() is False:
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

            if _DEVELOPMENT is True:
                print
                "load system %s global (%s) development (%s) platform (%s)" % (Name, Global, Development, Platform)

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
                if SystemManager.runSystem(Name, Name) is None:
                    Trace.log("Manager", 0, "Bootstrapper.loadSystems system %s invalid run" % Name)
                    return False

        return True

    @staticmethod
    def getSessionSystems():
        return Bootstrapper.s_sessionSystems

    @staticmethod
    def shutdown():
        for name, manager in Bootstrapper.s_managers.iteritems():
            if issubclass(manager, Manager) is True:
                manager.onFinalize()

        Bootstrapper.s_managers = {}
        Bootstrapper.s_sessionSystems = []