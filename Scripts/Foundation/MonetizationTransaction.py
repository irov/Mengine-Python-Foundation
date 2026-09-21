class MonetizationTransaction(object):
    """Prepare account changes without side effects, then persist one account snapshot."""

    active = False

    def __init__(self, storage):
        self.storage = storage
        self.values = {}
        self.settings = {}
        self.callbacks = []
        self.account_id = Mengine.getCurrentAccountName()

    def getValue(self, key):
        return self.values[key] if key in self.values else self.storage[key].getValue()

    def setValue(self, key, value):
        self.values[key] = value

    def addListValue(self, key, value):
        items = self.getValue(key).strip(", ").split(", ")
        if str(value) not in items:
            self.setValue(key, self.getValue(key) + "{}, ".format(value))

    def removeListValue(self, key, value):
        items = self.getValue(key).strip(", ").split(", ")
        self.setValue(key, "".join("{}, ".format(item) for item in items if item and item != str(value)))

    def getSetting(self, key, default):
        return self.settings.get(key, default)

    def setSetting(self, key, value):
        self.settings[key] = unicode(value)

    def afterCommit(self, fn, *args):
        self.callbacks.append((fn, args))

    def commit(self):
        if Mengine.hasCurrentAccount() is False or Mengine.getCurrentAccountName() != self.account_id:
            raise RuntimeError("Purchase account changed before commit")

        settings = self.settings.copy()
        for key, value in self.values.items():
            stored_value = type(self.storage[key])(key, value)
            settings[key] = unicode(stored_value.getSave())

        previous = {}
        MonetizationTransaction.active = True
        try:
            for key, value in settings.items():
                if Mengine.hasCurrentAccountSetting(key) is False:
                    if Mengine.addCurrentAccountSetting(key, u'None', None) is not True:
                        raise RuntimeError("Unable to create purchase setting {!r}".format(key))

                previous[key] = Mengine.getCurrentAccountSetting(key)
                if Mengine.changeCurrentAccountSetting(key, value) is not True:
                    raise RuntimeError("Unable to write purchase setting {!r}".format(key))

            # saveAccount replaces this account's settings file and reports the actual write result.
            if settings and Mengine.saveAccount() is False:
                raise RuntimeError("Unable to commit purchase account {!r}".format(self.account_id))
        except Exception:
            for key, value in previous.items():
                Mengine.changeCurrentAccountSetting(key, value)
            raise
        finally:
            MonetizationTransaction.active = False

        for key, value in self.values.items():
            self.storage[key].setValue(value)

        # Presentation and analytics cannot turn a persisted purchase back into a failed delivery.
        for fn, args in self.callbacks:
            try:
                fn(*args)
            except Exception as ex:
                Trace.log_exception("System", 0, "Purchase committed, callback failed: {}".format(ex))

        return True
