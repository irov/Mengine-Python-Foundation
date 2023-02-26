from GOAP2.Initializer import Initializer
from GOAP2.Params import Params
from GOAP2.TaskManager import TaskManager
from Notification import Notification

class System(Params, Initializer):

    def __init__(self):
        super(System, self).__init__()

        self.active = False
        self.name = None
        self.type = None

        self.__observers = []
        self.__events = []
        self.__task_chains = {}

    def _onParams(self, params):
        super(System, self)._onParams(params)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def isRun(self):
        return self.active

    def run(self):
        if self.active is True:
            Trace.log("System", 0, "System '%s' already active" % (self.name))
            return False

        try:
            successful = self._onRun()
        except Exception as ex:
            traceback.print_exc()

            Trace.log("System", 0, "System.run %s except '%s'" % (self.name, ex))
            return False

        if isinstance(successful, bool) is False:
            Trace.log("System", 0, "System.run %s _onRun must return boolean [True|False]" % self.name)
            return False

        if successful is False:
            Trace.log("System", 0, "System '%s' invalid run" % (self.name))
            return False

        self.active = True

        return True

    def _onRun(self):
        return True

    def _onInitialize(self):
        super(System, self)._onInitialize()

    def _onFinalize(self):
        super(System, self)._onFinalize()

        if self.active is True:
            self.stop()

    def existTaskChain(self, Name):
        return Name in self.__task_chains

    def removeTaskChain(self, Name):
        tc = self.__task_chains[Name]
        tc.cancel()
        self.__task_chains.pop(Name)

    def removeObserver(self, observer):
        if observer not in self.__observers:
            Trace.log("System", 0, "{}.removeObserver - observer not found in system".format(self.__class__.__name__))
            return False

        Notification.removeObserver(observer)
        self.__observers.remove(observer)
        return True

    def removeEventObserver(self, event, observer):
        if (event, observer) not in self.__events:
            Trace.log("System", 0, "{}.removeEventObserver - observer not found in system".format(self.__class__.__name__))
            return False

        event.removeObserver(observer)
        self.__events.remove((event, observer))
        return True

    def createTaskChain(self, Name, Cb=None, CbArgs=(), **Params):
        if Name in self.__task_chains:
            Trace.log("System", 0, "System.createTaskChain %s already have task chain %s" % (self.name, Name))

            return None

        TrueCb = None
        if Cb is not None:
            def __cb(isSkip, *args):
                del self.__task_chains[Name]

                Cb(isSkip, *args)

            TrueCb = __cb

        tc = TaskManager.createTaskChain(Name=Name, CallerDeep=1, Cb=TrueCb, CbArgs=CbArgs, **Params)

        self.__task_chains[Name] = tc

        return tc

    def addObserver(self, ID, Function, *Args, **Kwds):
        observer = Notification.addObserver(ID, Function, *Args, **Kwds)

        if observer is None:
            return

        self.__observers.append(observer)
        return observer

    def addEvent(self, Event, Function, *Args, **Kwds):
        observer = Event.addObserver(Function, *Args, **Kwds)

        details = (Event, observer)
        self.__events.append(details)
        return details

    def onSave(self, dict_systems):
        if self._onSave is System._onSave:
            return

        data_save = self._onSave()

        dict_systems[self.__class__.__name__] = data_save

    def _onSave(self):
        return None

    def onLoad(self, dict_systems):
        if self._onLoad is System._onLoad:
            return

        data_save = dict_systems.get(self.__class__.__name__, {})

        self._onLoad(data_save)

    def _onLoad(self, save_dict):
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("System", 0, "System '%s' invalid initialization '%s'" % (self.name, msg))

    def _onFinalizeFailed(self, msg):
        Trace.log("System", 0, "System '%s' invalid finalization '%s'" % (self.name, msg))

    def stop(self):
        if self.active is False:
            Trace.log("System", 0, "System '%s' already stop" % self.name)
            return

        self.active = False

        for observer in self.__observers:
            Notification.removeObserver(observer)

        self.__observers = []

        for event, observer in self.__events:
            event.removeObserver(observer)

        self.__events = []

        for chain in self.__task_chains.itervalues():
            chain.cancel()

        self.__task_chains = {}

        try:
            self._onStop()
        except TypeError as ex:
            Trace.log("System", 0, "System '%s' _onStop %s error: %s" % (self.name, self._onStop, ex))
            return

    def _onStop(self):
        pass