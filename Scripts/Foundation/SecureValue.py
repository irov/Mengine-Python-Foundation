class SecureValue(object):
    s_secure_values = {}

    def __init__(self, value_id, value):
        self.id = self.__setupID(value_id)
        self.value = self.__makeSecureValue(value)  # print SecureValue.s_secure_values

    def __makeSecureValue(self, value):
        if isinstance(value, int) is False:
            Trace.log("Manager", 0, "SecureValue {!r}: you can use only int for create: value={!r} {}".format(self.id, value, type(value)))
            return Menge.makeSecureUnsignedValue(0)
        return Menge.makeSecureUnsignedValue(value)

    def getValue(self):
        integrity_check, value = self.value.getUnprotectedValue()
        if integrity_check is False:
            # todo: resolve this
            Trace.log("Manager", 0, "Integrity of SecureValue {!r} has been broken".format(self.id))
            return False
        return value

    def getSecureValue(self):
        return self.value

    def setValue(self, value):
        """ value: int """
        secure_value = self.__makeSecureValue(value)
        self.setSecureValue(secure_value)

    def setSecureValue(self, secure_value):
        self.value.setupSecureValue(secure_value)

    def additiveValue(self, value):
        """ value: int or SecureValue """
        if isinstance(value, type(self.value)) is False:
            value = self.__makeSecureValue(value)
        self.value.additiveSecureValue(value)

    def subtractValue(self, value):
        """ value: int or SecureValue """
        if isinstance(value, type(self.value)) is False:
            value = self.__makeSecureValue(value)
        self.value.substractSecureValue(value)

    def isEqual(self, secure_value):
        if isinstance(secure_value, type(self.value)) is False:
            secure_value = self.__makeSecureValue(secure_value)
        integrity_check, result = self.value.cmpSecureValue(secure_value)
        if integrity_check is False:
            Trace.log("Manager", 0, "Integrity of SecureValue {!r} has been broken".format(self.id))
            return False
        return result == 0

    def getSave(self):
        save = self.value.saveHexadecimal()
        return save

    def loadSave(self, save):
        if save == "":
            return
        if self.value.loadHexadecimal(save) is False:
            Trace.log("Utils", 0, "SecureValue {} - your save {!r} is broken!!!".format(self.id, save))

    def __setupID(self, value_id):
        if value_id in SecureValue.s_secure_values.keys():
            tmp = 1
            new_id = value_id + str(tmp)
            while new_id in SecureValue.s_secure_values.keys():
                tmp += 1
                new_id = value_id[:-1] + str(tmp)
            value_id = new_id
        SecureValue.s_secure_values[value_id] = self
        return value_id

    @staticmethod
    def getById(value_id):
        value = SecureValue.s_secure_values.get(value_id, None)
        return value

    @staticmethod
    def getValueFromSecure(secure_value):
        integrity_check, value = secure_value.getUnprotectedValue()
        if integrity_check is False:
            Trace.log("Manager", 0, "Integrity of input SecureValue has been broken")
            return False
        return value