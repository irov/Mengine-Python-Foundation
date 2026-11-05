from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.Providers.SupportMail import SupportMail


class SupportProvider(BaseProvider):
    """ Player support: a support SDK (Cluefolk, Helpshift, ...) set by its system,
        or the support mail when no SDK is set or the SDK is not ready """

    s_allowed_methods = [
        "openSupport",  # (subject, body, technical_info) -> True if the support screen opened
    ]

    @staticmethod
    def openSupport(subject, body, technical_info):
        if SupportProvider.hasProvider() is True:
            if SupportProvider._call("openSupport", subject, body, technical_info) is True:
                return True

            Trace.msg_warn("SupportProvider: {!r} is not ready, send support mail".format(SupportProvider.getName()))

        return SupportMail.open(subject, body, technical_info)

    @staticmethod
    def _openSupportExceptionCb(ex, subject, body, technical_info):
        Trace.log_exception("Provider", 0, "SupportProvider {!r} openSupport: {}".format(SupportProvider.getName(), ex))
        return False
