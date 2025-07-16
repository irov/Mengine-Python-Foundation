from Foundation.Manager import Manager

class SettingsManager(Manager):
    @staticmethod
    def _onInitialize(*args):
        SettingsManager.__updateSettings()

        SettingsManager.addObserver(Notificator.onSettingChange, SettingsManager.__onSettingChange)
        pass

    @staticmethod
    def _onFinalize():
        Mengine.removeGlobalModule("SETTINGS")
        pass

    @staticmethod
    def __onSettingChange(setting_name, setting_value):
        SettingsManager.__updateSettings()
        return False

    @staticmethod
    def __updateSettings():
        settings = Mengine.getSettings()

        settings_struct = Utils.dictToStruct(settings)

        Mengine.addGlobalModule("SETTINGS", settings_struct)
        pass
    pass