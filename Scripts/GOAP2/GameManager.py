from Notification import Notification

class GameManager(object):
    s_block = 0
    s_block_keyboard = 0

    @staticmethod
    def blockKeyboard(value):
        if value is True:
            GameManager.s_block_keyboard += 1
        else:
            GameManager.s_block_keyboard -= 1
            pass
        if GameManager.s_block_keyboard < 0:
            print
            "Wtf" * 1000
            print
            "GameManager.s_block_keyboard is negative", GameManager.s_block_keyboard

        block = GameManager.s_block_keyboard != 0

        Notification.notify(Notificator.onBlockKeyBoard, block)
        pass

    @staticmethod
    def isBlockKeyboard():
        if GameManager.s_block_keyboard == 0:
            return False
            pass

        return True

    @staticmethod
    def blockGame(value):
        if value is True:
            GameManager.s_block += 1
        else:
            GameManager.s_block -= 1
            pass

        block = GameManager.s_block != 0

        Notification.notify(Notificator.onGameBlock, block)
        pass

    @staticmethod
    def isBlockGame():
        if GameManager.s_block == 0:
            return False
            pass

        return True
        pass
    pass