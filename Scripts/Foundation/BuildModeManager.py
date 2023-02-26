from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager

class BuildModeManager(Manager):
    s_build_config = {}
    s_current_build = None

    @staticmethod
    def loadParams(module, param):
        if Mengine.getGameParamUnicode("BuildModeCheckVersion") != u"2.0":
            return True

        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            build_mode = record.get("BuildMode")
            resource_tags = record.get("ResourceTags")

            BuildModeManager.s_build_config[build_mode] = resource_tags

        return True

    @staticmethod
    def getBuildResourceConfig(build_name):
        return BuildModeManager.s_build_config.get(build_name)