from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager

class LanguagesManager(Manager):
    s_languagesORM = []

    @staticmethod
    def loadParams(module, param):
        LanguagesManager.s_languagesORM = DatabaseManager.getDatabaseORMs(module, param)

        return True

    @staticmethod
    def validateTextId(text_id):
        if Mengine.existText(text_id) is False:
            return False
        return True


    @staticmethod
    def getLanguageTextId(locale):
        result = DatabaseManager.find(LanguagesManager.s_languagesORM, Language=locale)

        if result is None:
            Trace.log("Manager", 0, "Locale {!r} not found".format(locale))
            return None

        if LanguagesManager.validateTextId(result.TextId) is False:
            Trace.log("Manager", 0, "Text id {!r} does not localization".format(result.TextId))
            return None

        return result.TextId

    @staticmethod
    def getLocale():
        locale = Mengine.getLocale()

        return locale

    @staticmethod
    def setLocale(locale):
        Mengine.setLocale(locale)
        Trace.msg("Locale changed to {!r}".format(locale))

    @staticmethod
    def getLocales():
        locales = Mengine.getLocales()

        return locales

    @staticmethod
    def hasLocale(locale):
        if locale is not None:
            return Mengine.hasLocale(locale)