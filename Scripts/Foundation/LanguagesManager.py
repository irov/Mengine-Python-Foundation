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
        if Mengine.hasLocale(locale) is False:
            return None

        language_orm_record = DatabaseManager.find(LanguagesManager.s_languagesORM, Language=locale)

        if language_orm_record is None:
            Trace.msg("Locale {!r} not found".format(locale))
            return None

        if LanguagesManager.validateTextId(language_orm_record.TextId) is False:
            Trace.msg("Text id {!r} for localization {!r} not found".format(
                          language_orm_record.TextId, locale))
            return None

        return language_orm_record.TextId

    @staticmethod
    def getLocale():
        locale = Mengine.getLocale()
        if locale is None:
            Trace.msg("Locale {!r} is not found!".format(locale))

        return locale

    @staticmethod
    def setLocale(locale):
        if Mengine.hasLocale(locale) is False:
            Trace.msg("Locale {!r} is not found!".format(locale))
            return

        Mengine.setLocale(locale)
        Trace.msg("Locale changed to {!r}".format(locale))

    @staticmethod
    def getLocales():
        locales = Mengine.getLocales()
        if locales is None:
            Trace.msg("No localization found!")

        return locales

    @staticmethod
    def hasLocale(locale):
        if locale is None:
            Trace.msg("LanguagesManager.hasLocale got empty argument!")
            return None

        return Mengine.hasLocale(locale)
