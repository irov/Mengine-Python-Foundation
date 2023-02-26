from Foundation.System import System

class SystemQALogger(System):
    # Confluence doc: https://wonderland-games.atlassian.net/wiki/spaces/TDH/pages/1772421145/QA

    __Logger = None
    s_functions = []
    s_msg_prefixes = {"notify": "    * "}

    def _onRun(self):
        if _QUALITYASSURANCE is False:
            return True

        self.__createLogger()
        self.log("SystemQA successfully started!")
        self.__addObservers()

        return True

    def _onStop(self):
        self.log("SystemQA stopped!")
        return True

    # Preparation ======================================================================================================

    @classmethod
    def __createLogger(cls):
        if cls.__Logger is not None:
            return
        if cls.onlyConsole() is True:
            return
        t = Mengine.getDatePathTimestamp()
        file_name = "QA_{}.log".format(t)
        cls.__Logger = Mengine.makeFileLogger(file_name)

    @staticmethod
    def shouldDuplicate():
        if _QUALITYASSURANCE is True:
            option = Mengine.getOptionValue("qa")
            return option == "duplicate"
        return False

    @staticmethod
    def onlyConsole():
        if _QUALITYASSURANCE is True:
            option = Mengine.getOptionValue("qa")
            return option == "console"
        return False

    def __addObservers(self):
        identities = {  # use $id for paste identity in message
            "onParagraphRun": "      $id '%s'", "onParagraphComplete": "      $id '%s'", "onScenarioComplete": "    $id '%s'", "onEnableSceneLayerGroup": "<SceneManager> enable scene '%s' layer '%s'", "onDisableSceneLayerGroup": "<SceneManager> disable scene '%s' layer '%s'", "onGameSceneChange": "<SceneManager> changed game scene from '%s' to '%s'", "onEnigmaStart": "start enigma '%s'", "onEnigmaComplete": "complete enigma '%s'", "onInventoryItemDetach": "<Inventory> detach item '%s' (state=%s)",
            "onInventoryItemPick": "<Inventory> pick item '%s' (state=%s)", "onHOGFittingItemPicked": "<HOGInventoryFitting> pick item '%s'", "onHOGFittingItemUsed": "<HOGInventoryFitting> use item '%s'", "onHOGFittingItemDetached": "<HOGInventoryFitting> detach item '%s'"}
        for identity, message in identities.items():
            self.__createObserver(identity, message)

        self.addObserver(Notificator.onInventoryAddItem, self.__onInventoryAddItem)
        self.addObserver(Notificator.onButtonClick, self.__onButtonClick)
        self.addObserver(Notificator.onItemClick, self.__onButtonClick)
        # self.addObserver(Notificator.onMovieSocketClickSuccessful, self.__onMovieSocketClick)
        self.addObserver(Notificator.onSocketClick, self.__onSocketClick)
        self.addObserver(Notificator.onItemCollectComplete, self.__onItemCollectComplete)
        self.addObserver(Notificator.onInventoryCombineInventoryItem, self.__onInventoryCombineInventoryItem)
        self.addObserver(Notificator.onHintActionStart, self.__onHintActionStart)

    # Observers ========================================================================================================

    def __createObserver(self, identity, message=None):
        if Notificator.hasIdentity(identity) is False:
            return False
        notificator = Notificator.getIdentity(identity)

        def mapper(arg):
            try:
                return "{}".format(arg.getName())
            except AttributeError:
                return str(arg)

        def Filter(*args):
            f_args = tuple(map(mapper, args))  # fix for unicode values
            if message is not None:
                f_message = str(f_args) + " | " + message
                if message.count("%s") > 0:
                    f_message = message % f_args
                f_message = f_message.replace("$id", identity)
            else:
                f_message = str(f_args)
            SystemQALogger.notify(f_message)
            return False

        self.addObserver(notificator, Filter)

    @staticmethod
    def __onInventoryCombineInventoryItem(inv, arrowItem, invItem):
        inv_name = inv.getName().replace("Demon_", "")
        f_message = "<{}> try combine {!r} (arrow) with {!r} (inventory)".format(inv_name, arrowItem.getName(), invItem.getName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onInventoryAddItem(inv, item):
        inv_name = inv.getName().replace("Demon_", "")
        f_message = "<{}> add item {!r}".format(inv_name, item.getName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onButtonClick(obj):
        f_message = "click on {!r} [{!r}]".format(obj.getName(), obj.getGroupName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onSocketClick(obj):
        f_message = "click on socket {!r} [{!r}]".format(obj.getName(), obj.getGroupName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onMovieSocketClick(object, name, touchId, x, y, button, isDown, isPressed):
        f_message = "click on socket {!r} [{!r}]: isDown={}, isPressed={}".format(name, object.getGroupName(), isDown, isPressed)
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onItemCollectComplete(socket, item_list):
        f_message = "romashka {!r} complete".format(socket.getName().replace("Socket_", ""))
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def __onHintActionStart(HintAction):
        f_message = "<Hint> {} [{}]".format(HintAction.__class__.__name__, HintAction.Quest.questType)
        SystemQALogger.notify(f_message)
        return False

    # ==================================================================================================================

    @classmethod
    def log(cls, msg, type_=None):
        if _QUALITYASSURANCE is False:
            return

        if cls.onlyConsole() is True:
            Trace.msg(":QA: {}".format(msg))
            return

        if cls.__Logger is None:
            if _DEVELOPMENT is True:
                Trace.msg_err("SystemQALogger: can't save log (file not created), your msg: {!r}".format(msg))
            return

        prefix = cls.s_msg_prefixes.get(type_, "")

        cls.__Logger(prefix + msg)
        if cls.shouldDuplicate() is True:
            Trace.msg(":QA: {}".format(msg))

    @classmethod
    def notify(cls, msg):
        cls.log(msg, "notify")