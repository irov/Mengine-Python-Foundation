class SecureException(BaseException):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
        pass
    pass

class SecureAttribute(object):
    def __init__(self, value=None):
        self.__value = None
        self.__hash = None

        self.set(value)

    def isCurrupted(self):
        return self.__hash != self.hashValue()

    def set(self, value):
        self.__value = value
        self.__hash = self.hashValue()

    def add(self, value):
        self._add(value)

    def _add(self, value):
        old_value = self.get()
        new_value = old_value + value
        self.set(new_value)

    def addSecureAttribute(self, secure_attribute):
        self._addSecureAttribute(secure_attribute)

    def _addSecureAttribute(self, secure_attribute):
        sa_value = secure_attribute.get()
        self.add(sa_value)

    def get(self):
        try:
            value = self._get()
        except SecureException as ex:
            self._onGetValueFailed(ex)
            return None

        return value

    def _get(self):
        if self.isCurrupted() is True:
            raise SecureException("Attribute value corrupted")
        return self.__value

    def _onGetValueFailed(self, ex):
        Trace.log("Object", 0, "SecureAttribute._onGetFailed {}".format(ex))

    def hashValue(self):
        return self._hashValue(self.__value)

    def _hashValue(self, value):
        return None

    def __str__(self):
        return str(self.__value)