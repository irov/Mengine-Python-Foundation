class SupportMail(object):
    """ Default support: a mail to the game param TechnicalSupportEmail """

    @staticmethod
    def open(subject, body, technical_info):
        receiver = Mengine.getGameParamUnicode("TechnicalSupportEmail")

        if _DEVELOPMENT is True:
            Trace.msg("DUMMY send support mail:\n  Receiver: {!r}\n  Subject: {!r}"
                      "\n{}\n{}\n  (Include player save)".format(receiver, subject, body, technical_info))

        try:
            Mengine.openMail(receiver, subject, body, technical_info)
        except Exception as ex:
            Trace.log_exception("Provider", 0, "SupportMail.open: %s" % ex)
            return False

        return True
