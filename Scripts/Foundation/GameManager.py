from Foundation.Manager import Manager

class GameManager(Manager):
    s_block_game = 0
    s_block_keyboard = 0

    # DEFAULT KEYBOARD INPUT BLOCKER (see Personality onHandleKeyEvent)

    @staticmethod
    def blockKeyboard(state):
        if state is True:
            GameManager.s_block_keyboard += 1
        else:
            GameManager.s_block_keyboard -= 1
        if GameManager.s_block_keyboard < 0:
            Trace.log("Manager", 0, "GameManager.s_block_keyboard is negative")

        block = GameManager.s_block_keyboard != 0

        Notification.notify(Notificator.onBlockKeyBoard, block)

    @staticmethod
    def unblockKeyboard():
        """ alias for blockKeyboard(False) """
        return GameManager.blockKeyboard(False)

    @staticmethod
    def isBlockKeyboard():
        if GameManager.s_block_keyboard == 0:
            return False
        return True

    # GAME BLOCK (just as flag, not really block the game)

    @staticmethod
    def blockGame(value):
        if value is True:
            GameManager.s_block_game += 1
        else:
            GameManager.s_block_game -= 1
        if GameManager.s_block_game < 0:
            Trace.log("Manager", 0, "GameManager.s_block is negative")

        block = GameManager.s_block_game != 0

        Notification.notify(Notificator.onGameBlock, block)

    @staticmethod
    def unblockGame():
        """ alias for blockGame(False) """
        return GameManager.blockGame(False)

    @staticmethod
    def isBlockGame():
        if GameManager.s_block_game == 0:
            return False
        return True
