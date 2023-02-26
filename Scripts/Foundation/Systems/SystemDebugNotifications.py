from Foundation.DebugNotificationsManager import DebugNotificationsManager
from Foundation.System import System
from Foundation.Systems.SystemQALogger import SystemQALogger

class SystemDebugNotifications(System):
    # Confluence doc: https://wonderland-games.atlassian.net/wiki/spaces/SCR/pages/1772879886/DebugNotifications

    _dev_to_debug_observers = []

    def _onRun(self):
        if SystemDebugNotifications.isEnable() is False:
            return True

        self.__addObservers()
        return True

    def _onInitialize(self):
        self.__addDevToDebug()

    def _onFinalize(self):
        self.__remDevToDebug()

    @staticmethod
    def isEnable():
        return Menge.hasOption("notifications")

    # Preparation ======================================================================================================

    def __addObservers(self):
        """ add observers from DebugNotifications.xlsx """
        records = DebugNotificationsManager.getAllData()

        for record in records:
            identity = record.get("identity")
            message = record.get("message")
            show_args = record.get("show_args")

            self.__createObserver(identity, message, show_args)

    def __createObserver(self, identity, message, show_args):
        def fn(*args, **kwargs):  # todo: handle kwargs
            def mapper(arg):
                try:
                    return "{}:'{}'".format(str(type(arg)).split(".")[-1][:-2], str(arg.getName()))
                except AttributeError:
                    return str(arg)

            args = tuple(map(mapper, args))  # fix for unicode values
            f_args = " {}".format(args) if show_args is True else ""
            f_msg = ""

            if message is not None:
                f_arg_count = message.count("%s")
                if f_arg_count != 0:
                    if len(args) == f_arg_count:
                        f_msg = message % args
                    else:
                        Trace.log("System", 0, "Invalid number of '%%s' ({}) for format {!r} message (got {} args: {})".format(f_arg_count, identity, len(args), list(args)))
                        if len(args) > message.count("%s"):
                            _msg = message + " | other args: " + "'%s', " * abs(len(args) - f_arg_count)
                            f_msg = _msg % args
                        else:
                            # todo: replace unnecessary "%s" from message
                            f_msg = message.replace("%s", "_")

            f_message = identity
            f_message += f_args if len(args) > 0 else ""
            f_message += (" | " + f_msg) if f_msg else ""

            if _QUALITYASSURANCE is False:
                Trace.msg("    * " + f_message)
            else:
                SystemQALogger.notify(f_message)
            return False

        notificator = Notificator.getIdentity(identity)
        if notificator is not None:
            self.addObserver(notificator, fn)

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    @staticmethod
    def __sendNotify(text):
        """ Command Line handler for send_notification widget """

        params = text.split(" ")
        if len(params) == 0:
            return

        identity = params[0]
        notificator = Notificator.getIdentity(identity)
        if notificator is None:
            return

        args = [int(arg) if arg.isdigit() else arg for arg in params[1:]]
        Notification.notify(notificator, *args)
        Trace.msg("<SystemDebugNotifications> sent notify '{} {}' via DevToDebug".format(identity, args))

    @staticmethod
    def __addObserver(text):
        """ Command Line handler for set_observer widget """

        identity = text

        notificator = Notificator.getIdentity(identity)
        if notificator is None:
            return

        def _observer(*args, **kwargs):
            Trace.msg("*   {}: args={} kwargs={}".format(identity, args, kwargs))
            return False

        observer = Notification.addObserver(notificator, _observer)
        SystemDebugNotifications._dev_to_debug_observers.append(observer)
        Trace.msg("<SystemDebugNotifications> successfully add observer to '{}' via DevToDebug".format(identity))

    @staticmethod
    def __addDevToDebug():
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return

        tab = Menge.getDevToDebugTab("Cheats") or Menge.addDevToDebugTab("Cheats")

        if tab.findWidget("set_observer") is None:
            w_observe = Menge.createDevToDebugWidgetCommandLine("set_observer")
            w_observe.setTitle("Set observer")
            w_observe.setPlaceholder("Syntax: <identity>")
            w_observe.setCommandEvent(SystemDebugNotifications.__addObserver)
            tab.addWidget(w_observe)

        if tab.findWidget("send_notification") is None:
            w_notify = Menge.createDevToDebugWidgetCommandLine("send_notification")
            w_notify.setTitle("Send notify")
            w_notify.setPlaceholder("Syntax: <identity> [*args]")
            w_notify.setCommandEvent(SystemDebugNotifications.__sendNotify)
            tab.addWidget(w_notify)

    @staticmethod
    def __remDevToDebug():
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return

        for observer in SystemDebugNotifications._dev_to_debug_observers:
            Notification.removeObserver(observer)