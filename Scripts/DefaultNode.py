# coding="utf-8"
from MessageSender import MessageSender

# ------------------------------------------------------------------------------
# Class:
# Description:
# - 
# ------------------------------------------------------------------------------
class DefaultNode(MessageSender):
    # ----------------------------------------------------------------------------
    # Method:
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def __init__(self):
        super(DefaultNode, self).__init__()

        self._callback = {}
        pass

    # ----------------------------------------------------------------------------
    # Method: onScaleEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def addCallback(self, key, fn):
        if fn in self._callback[key]:
            print
            "Error! this callback is already in list", self, key, fn
            return

        self._callback[key].append(fn)
        pass

    # ----------------------------------------------------------------------------
    # Method: onScaleEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def removeCallback(self, key, fn):
        self._callback[key].remove(fn)
        pass