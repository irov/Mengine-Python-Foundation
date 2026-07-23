from Secure.SecureAttribute import SecureAttribute

class CRCSecureAttribute(SecureAttribute):
    def _hashValue(self, value):
        crc = Mengine.makeCRC32(str(value))
        result = "%X" % (crc & 0xFFFFFFFF)
        return result