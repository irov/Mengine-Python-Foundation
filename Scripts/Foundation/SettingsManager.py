from Foundation.Manager import Manager

class SettingsManager(Manager):
    @classmethod
    def _onInitialize(cls, *args):
        SettingsManager.__updateSettings()

        cls.addObserver(Notificator.onSettingChange, SettingsManager.__onSettingChange)
        pass

    @classmethod
    def _onFinalize(cls):
        Mengine.removeGlobalModule("SETTINGS")
        pass

    @staticmethod
    def __onSettingChange(setting_name, setting_value):
        SettingsManager.__updateSettings()
        pass

    @staticmethod
    def __updateSettings():
        settings = Mengine.getSettings()

        settings_struct = Utils.dictToStruct(settings)

        Mengine.addGlobalModule("SETTINGS", settings_struct)
        pass
    pass