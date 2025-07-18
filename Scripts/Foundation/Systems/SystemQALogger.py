from Foundation.System import System


class SystemQALogger(System):
    """
        Confluence doc: https://wonderland-games.atlassian.net/wiki/spaces/TDH/pages/1772421145/QA
    """

    __Logger = None
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

    @staticmethod
    def shouldDuplicate():
        """ if -qa:duplicate - all logs will write to file and console """
        if _QUALITYASSURANCE is True:
            option = Mengine.getOptionValue("qa")
            return option == "duplicate"
        return False

    @staticmethod
    def onlyConsole():
        """ if -qa:console - all logs will write only to console """
        if _QUALITYASSURANCE is True:
            option = Mengine.getOptionValue("qa")
            return option == "console"
        return False

    # --- Observer utils -----------------------------------------------------------------------------------------------

    def __addObservers(self):
        self._addMessageObservers()
        self._addFilterObservers()

    def _addMessageObservers(self):
        identities_with_message = {  # use $id for paste identity in message
            "onParagraphRun": "      $id '%s'",
            "onParagraphComplete": "      $id '%s'",
            "onScenarioComplete": "    $id '%s'",
            "onEnableSceneLayerGroup": "<SceneManager> enable scene '%s' layer '%s'",
            "onDisableSceneLayerGroup": "<SceneManager> disable scene '%s' layer '%s'",
            "onGameSceneChange": "<SceneManager> changed game scene from '%s' to '%s'",
            "onEnigmaStart": "start enigma '%s'",
            "onEnigmaComplete": "complete enigma '%s'",
            "onInventoryItemDetach": "<Inventory> detach item '%s' (state=%s)",
            "onInventoryItemPick": "<Inventory> pick item '%s' (state=%s)",
            "onHOGFittingItemPicked": "<HOGInventoryFitting> pick item '%s'",
            "onHOGFittingItemUsed": "<HOGInventoryFitting> use item '%s'",
            "onHOGFittingItemDetached": "<HOGInventoryFitting> detach item '%s'",
            "onLocationComplete": "complete location '%s'",
            # Dungeon
            "onBankSetResource": "upd bank [%s] '%s' from %s to %s",
            "onGameBattleStart": "start battle",
            "onGameBattleEnd": "end battle (win=%s) (level_up=%s) with results: %s. Transition to '%s'",
            "onShowBattleCardInfo": "show battle card info: %s",
            "onBattleCardClick": "click on card at position %s",
        }
        for identity, message in identities_with_message.items():
            self.__createMessageObserver(identity, message)

    def _addFilterObservers(self):
        identities_with_filter = {
            # Foundation
            "onMovieSocketClickSuccess": self._cbMovieSocketClick,
            "onSocketClick": self._cbSocketClick,
            "onButtonClick": self._cbButtonClick,
            # HOPA
            "onInventoryAddItem": self._cbInventoryAddItem,
            "onItemClick": self._cbButtonClick,
            "onItemCollectComplete": self._cbItemCollectComplete,
            "onInventoryCombineInventoryItem": self._cbInventoryCombineInventoryItem,
            "onHintActionStart": self._cbHintActionStart,
        }
        for identity, Filter in identities_with_filter.items():
            if Notificator.hasIdentity(identity) is False:
                continue
            notificator = Notificator.getIdentity(identity)
            self.addObserver(notificator, Filter)

    def __createMessageObserver(self, identity, message=None):
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
                assert type(message) == str

                f_message = str(f_args) + " | " + message
                if message.count("%s") > 0:
                    f_message = message % f_args
                f_message = f_message.replace("$id", identity)
            else:
                f_message = str(f_args)
            SystemQALogger.notify(f_message)
            return False

        self.addObserver(notificator, Filter)

    # --- Custom observer filters --------------------------------------------------------------------------------------

    # Foundation

    @staticmethod
    def _cbButtonClick(obj):
        f_message = "click on {!r} [{!r}]".format(obj.getName(), obj.getGroupName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def _cbSocketClick(obj):
        f_message = "click on socket {!r} [{!r}]".format(obj.getName(), obj.getGroupName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def _cbMovieSocketClick(object, name, touchId, x, y, button, isDown, isPressed):
        f_message = "click on socket {!r} [{!r}]: isDown={}, isPressed={}".format(
            name, object.getGroupName(), isDown, isPressed)
        SystemQALogger.notify(f_message)
        return False

    # HOPA

    @staticmethod
    def _cbInventoryCombineInventoryItem(inv, arrowItem, invItem):
        inv_name = inv.getName().replace("Demon_", "")
        f_message = "<{}> try combine {!r} (arrow) with {!r} (inventory)".format(
            inv_name, arrowItem.getName(), invItem.getName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def _cbInventoryAddItem(inv, item):
        inv_name = inv.getName().replace("Demon_", "")
        f_message = "<{}> add item {!r}".format(inv_name, item.getName())
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def _cbItemCollectComplete(socket, item_list):
        f_message = "romashka {!r} complete".format(socket.getName().replace("Socket_", ""))
        SystemQALogger.notify(f_message)
        return False

    @staticmethod
    def _cbHintActionStart(HintAction):
        f_message = "<Hint> {} [{}]".format(HintAction.__class__.__name__, HintAction.Quest.questType)
        SystemQALogger.notify(f_message)
        return False

    # --- Logger utils -------------------------------------------------------------------------------------------------

    @staticmethod
    def __createLogger():
        """ Creates logger file and starts logger instance """
        if SystemQALogger.__Logger is not None:
            return
        if SystemQALogger.onlyConsole() is True:
            return
        t = Mengine.getDatePathTimestamp()
        file_name = "QA_{}.log".format(t)
        SystemQALogger.__Logger = Mengine.makeFileLogger(file_name)

    @staticmethod
    def log(msg, type_=None):
        if _QUALITYASSURANCE is False:
            return

        if SystemQALogger.onlyConsole() is True:
            Trace.msg(":QA: {}".format(msg))
            return

        if SystemQALogger.__Logger is None:
            if _DEVELOPMENT is True:
                Trace.msg_err("SystemQALogger: can't save log (file not created), your msg: {!r}".format(msg))
            return

        prefix = SystemQALogger.s_msg_prefixes.get(type_, "")

        SystemQALogger.__Logger(prefix + msg)
        if SystemQALogger.shouldDuplicate() is True:
            Trace.msg(":QA: {}".format(msg))

    @staticmethod
    def notify(msg):
        SystemQALogger.log(msg, "notify")
