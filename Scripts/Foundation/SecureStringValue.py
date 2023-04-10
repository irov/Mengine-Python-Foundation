class SecureStringValue(object):

    def __init__(self, value_id, value):
        self.id = value_id
        self.value = self.__makeSecureValue(value)

    def __makeSecureValue(self, value):
        if isinstance(value, str) is False:
            Trace.log("Manager", 0, "SecureStringValue {!r}: you can use only str for create: value={!r} {}".format(self.id, value, type(value)))
            return Mengine.makeSecureStringValue("NULL")
        return Mengine.makeSecureStringValue(value)

    def getValue(self):
        integrity_check, value = self.value.getUnprotectedValue()
        if integrity_check is False:
            Trace.log("Manager", 0, "Integrity of SecureStringValue {!r} has been broken".format(self.id))
            return False
        return value

    def getSecureValue(self):
        return self.value

    def setValue(self, value):
        """ value: str """
        secure_value = self.__makeSecureValue(value)
        self.setSecureValue(secure_value)

    def setSecureValue(self, secure_value):
        self.value = secure_value  # self.value.setupSecureValue(secure_value)

    def isEqual(self, secure_string):
        """ value: str or SecureStringValue """
        if isinstance(secure_string, type(self.value)) is False:
            secure_string = self.__makeSecureValue(secure_string)
        integrity_check, result = self.value.cmpSecureValue(secure_string)
        if integrity_check is False:
            Trace.log("Manager", 0, "Integrity of SecureStringValue {!r} has been broken".format(self.id))
            return False
        return result == 0

    def getSave(self):
        save = self.value.saveHexadecimal()
        return save

    def loadSave(self, save):
        if save == "":
            return
        if self.value.loadHexadecimal(save) is False:
            Trace.log("Utils", 0, "SecureStringValue {} - your save {!r} is broken!!!".format(self.id, save))

    @staticmethod
    def getValueFromSecure(secure_value):
        integrity_check, value = secure_value.getUnprotectedValue()
        if integrity_check is False:
            Trace.log("Manager", 0, "Integrity of input SecureStringValue has been broken")
            return False
        return value
