class AndroidAppLovinCallbacks(object):
    ANDROID_PLUGIN_NAME = "MengineAppLovin"

    def __init__(self):
        super(AndroidAppLovinCallbacks, self).__init__()
        self._cbs = {}

    def _addAndroidCallback(self, name, cb):
        if name in self._cbs:
            Trace.log("System", 0, "{}: callback {!r} is already exists !!!".format(self.__class__.__name__, name))
            Mengine.removeAndroidCallback(self.ANDROID_PLUGIN_NAME, name, self._cbs[name])
        identity = Mengine.addAndroidCallback(self.ANDROID_PLUGIN_NAME, name, cb)
        self._cbs[name] = identity
        return identity

    def _setCallbacks(self):
        raise NotImplementedError

    def _removeAndroidCallbacks(self):
        for name, cb_id in self._cbs.items():
            Mengine.removeAndroidCallback(self.ANDROID_PLUGIN_NAME, name, cb_id)
        self._cbs = {}
