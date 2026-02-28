ANDROID_PLUGIN_NAME = "AndroidAdServicePlugin"

class AndroidAdCallbacks(object):
    def __init__(self):
        super(AndroidAdCallbacks, self).__init__()
        self._cbs = {}

    def _addAndroidCallback(self, name, cb):
        if _DEVELOPMENT is True and name in self._cbs:
            Trace.log("System", 0, "{}: callback {!r} is already exists !!!".format(self.__class__.__name__, name))

        identity = Mengine.addAndroidCallback(ANDROID_PLUGIN_NAME, name, cb)
        self._cbs[name] = identity
        return identity

    def _setCallbacks(self):
        raise NotImplementedError

    def _removeAndroidCallbacks(self):
        for name, identity in self._cbs.items():
            Mengine.removeAndroidCallback(ANDROID_PLUGIN_NAME, name, identity)
        self._cbs = {}
