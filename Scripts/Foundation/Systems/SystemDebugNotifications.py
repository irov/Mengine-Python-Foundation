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
        return Mengine.hasOption("notifications")

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
            kwargs = dict(map(lambda pair: (pair[0], mapper(pair[1])), kwargs.items()))

            f_args = " {}".format(args) if show_args is True else ""
            f_msg = self._prepareMessageArgs(identity, message, args)

            f_message = identity
            f_message += f_args if len(args) > 0 else ""
            f_message += (" | " + f_msg) if f_msg else ""
            f_message += " | kwargs: {}".format(kwargs) if len(kwargs) > 0 else ""

            if _QUALITYASSURANCE is False:
                Trace.msg("    * " + f_message)
            else:
                SystemQALogger.notify(f_message)
            return False

        notificator = Notificator.getIdentity(identity)
        if notificator is not None:
            self.addObserver(notificator, fn)

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
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        tab = Mengine.getDevToDebugTab("Cheats") or Mengine.addDevToDebugTab("Cheats")

        if tab.findWidget("set_observer") is None:
            w_observe = Mengine.createDevToDebugWidgetCommandLine("set_observer")
            w_observe.setTitle("Set observer")
            w_observe.setPlaceholder("Syntax: <identity>")
            w_observe.setCommandEvent(SystemDebugNotifications.__addObserver)
            tab.addWidget(w_observe)

        if tab.findWidget("send_notification") is None:
            w_notify = Mengine.createDevToDebugWidgetCommandLine("send_notification")
            w_notify.setTitle("Send notify")
            w_notify.setPlaceholder("Syntax: <identity> [*args]")
            w_notify.setCommandEvent(SystemDebugNotifications.__sendNotify)
            tab.addWidget(w_notify)

    @staticmethod
    def __remDevToDebug():
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        for observer in SystemDebugNotifications._dev_to_debug_observers:
            Notification.removeObserver(observer)

    # utils

    def _prepareMessageArgs(self, identity, message, args):
        if message is None:
            return ""

        s_counts = message.count("%s")
        if s_counts == 0:
            return message

        args_count = len(args)
        if args_count == s_counts:
            # CASE 1: all ok, message '%s' count and args count are same
            f_msg = message % args
        else:
            Trace.log("System", 3, "Invalid number of '%%s' ({}) for format {!r} message (got {} args: {})"
                      .format(s_counts, identity, args_count, list(args)))

            # CASE 2: add missing '%s' to the message text
            if args_count > s_counts:
                _msg = message + " | other args: " + ", ".join(["'%s'"] * (args_count - s_counts))

            # CASE 2: remove extra '%s' from text
            else:   # args_count < s_counts
                to_remove = s_counts - args_count
                _msg = Utils.replace_last(message, "s%", "_", to_remove, already_reverted_substrings=True)
                print _msg

            f_msg = _msg % args

        return f_msg

