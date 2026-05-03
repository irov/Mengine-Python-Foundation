from Foundation.BuildModeManager import BuildModeManager
from Foundation.Managers import Managers
from Foundation.SystemManager import SystemManager

def checkBuildMode(Name, Survey, CE, BuildModeTags):
    """ :returns: True if build mode not match """
    BuildModeVersion = Mengine.getGameParamUnicode("BuildModeCheckVersion")
    BuildMode = Mengine.getGameParamUnicode("BuildMode")

    def _reportFail(build_mode, object_name):
        Trace.msg_dev("[Bootstrapper] (BuildModeCheckVersion {}, BuildMode {!r}) FAIL {!r}".format(BuildModeVersion, build_mode, object_name))
        pass

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
    @staticmethod
    def loadEntities(ModuleName, Types):
        if Mengine.getGameParamBool("NotUseDefaultEntitiesList.{}".format(ModuleName), False) is True:
            Types = []

            from Foundation.DatabaseManager import DatabaseManager
            records = DatabaseManager.getDatabaseRecordsFilterBy("Database", "Entities", Module=ModuleName)

            for record in records:
                Types.append({"Type": record.get("Type"), "Override": record.get("Override", False)})

        for Desc in Types:
            if isinstance(Desc, dict):
                EntityType = Desc.get("Type")
                Override = bool(Desc.get("Override", False))
            else:
                EntityType = Desc
                Override = False

            if EntityType is None:
                Trace.log("Bootstrapper", 0, "Bootstrapper.loadEntities invalid type %s for module %s" % (EntityType, ModuleName))
                return False

            ImportName = "{}.Entities.{}".format(ModuleName, EntityType)

            try:
                EntityModule = __import__(ImportName, fromlist=[ImportName])
            except ImportError:
                Trace.log_exception("Bootstrapper", 0, "Bootstrapper.loadEntities invalid import %s for type %s" % (ImportName, EntityType))
                return False

            if hasattr(EntityModule, "onInitialize") is True:
                result = getattr(EntityModule, "onInitialize")()

                if isinstance(result, bool) is False:
                    Trace.log("Bootstrapper", 0, "Bootstrapper.loadEntities invalid initialize for import %s for type %s mast be return Bool [True|False] but return %s" % (ImportName, EntityType, result))
                    return False

                if result is False:
                    Trace.log("Bootstrapper", 0, "Bootstrapper.loadEntities invalid initialize for import %s for type %s" % (ImportName, EntityType))
                    return False
            else:
                from Foundation.EntityManager import EntityManager
                from Foundation.ObjectManager import ObjectManager

                if EntityManager.importEntity(ImportName, EntityType, Override=Override) is False:
                    Trace.log("Bootstrapper", 0, "Bootstrapper.loadEntities invalid import %s for type %s" % (ImportName, EntityType))
                    return False

                if ObjectManager.importObject(ImportName, EntityType, Override=Override) is False:
                    Trace.log("Bootstrapper", 0, "Bootstrapper.loadEntities invalid import %s for type %s" % (ImportName, EntityType))
                    return False

        return True

    @staticmethod
    def loadManagers(module, param):
        from Foundation.DatabaseManager import DatabaseManager

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
                Manager = Managers.getManager(Module, Name)

                if Manager is None:
                    Trace.log("Bootstrapper", 0, "Bootstrapper.loadManagers not found manager %s.%s" % (Module, Name))
                    return False

                if Param is not None:
                    result = Manager.loadParams(Database, Param)

                    if isinstance(result, bool) is False:
                        Trace.log("Bootstrapper", 0, "Bootstrapper.loadManagers manager %s.%s load params mast be return Bool [True|False] but return %s" % (Module, Name, result))
                        return False

                    if result is False:
                        Trace.log("Bootstrapper", 0, "Bootstrapper.loadManagers manager %s.%s invalid load param %s" % (Module, Name, Param))
                        return False
                    pass

                Trace.msg_dev("Bootstrapper.loadManagers manager {}.{} loaded".format(Module, Name))
                pass
            pass

        return True

    @staticmethod
    def loadSystems(module, param):
        from Foundation.DatabaseManager import DatabaseManager

        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            Module = record.get("Module")
            Name = record.get("Name")
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

            if SystemManager.importSystem(Module, Name) is None:
                Trace.log("Bootstrapper", 0, "Bootstrapper.loadSystems system %s invalid import %s:%s" % (Name, Module, Name))
                return False

            if Development is not None:
                Development = bool(Development)

            if Development is not _DEVELOPMENT and Development is not None:
                continue

            if SystemManager.availableSystem(Name) is False:
                continue

            if SystemManager.runSystem(Name, Name) is False:
                Trace.log("Bootstrapper", 0, "Bootstrapper.loadSystems system %s invalid run" % Name)
                return False

            Trace.msg_dev("Bootstrapper.loadSystems system {}.{} loaded".format(Module, Name))
            pass

        return True