from Foundation.Initializer import Initializer
from Foundation.Params import Params
from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.TaskBase import TaskBase
from Foundation.Task.TaskBaseRace import TaskBaseRace
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource
from Foundation.Task.TaskQueue import TaskQueue
from Foundation.TaskManager import TaskManager

class TaskChain(MixinGroup, Params, Initializer):
    DEFAULT_CALLER = (None, None, None)

    if _DEVELOPMENT is True:
        IDLE = "IDLE"
        RUN = "RUN"
        SKIP = "SKIP"
        COMPLETE = "COMPLETE"
        STOP_IDLE = "STOP_IDLE"
        STOP_RUN = "STOP_RUN"
        CANCEL = "CANCEL"
        FINALIZE = "FINALIZE"
    else:
        IDLE = 0
        RUN = 1
        SKIP = 2
        COMPLETE = 3
        STOP_IDLE = 4
        STOP_RUN = 5
        CANCEL = 6
        FINALIZE = 7
        pass

    def __init__(self):
        super(TaskChain, self).__init__()

        self.name = None
        self.named = False

        self.cb = None
        self.cbArgs = None

        self.node = None
        self.__global = False
        self.repeat = False
        self.until = None

        self.AutoRun = True
        self.AutoReg = True

        self.runningTasks = []

        self.state = TaskChain.IDLE

        if _DEVELOPMENT is True:
            self.processing = None
            pass

        self.source = None
        self.caller = TaskChain.DEFAULT_CALLER

        self.skipInProgress = False

        self.queue = TaskQueue()
        self.tasks = []

        self.NoCheckAntiStackCycle = False
        pass

    def __repr__(self):
        return "TaskChain '{}' [{}] caller '{}:{}' doc '{}'".format(self.name, id(self), self.caller[0], self.caller[1], self.caller[2])

    def _onParams(self, params):
        super(TaskChain, self)._onParams(params)

        self.name = params.get("Name", None)

        self.cb = params.get("Cb", None)
        self.cbArgs = params.get("CbArgs", ())

        self.node = params.get("Node", None)

        self.__global = params.get("Global", False)

        self.repeat = params.get("Repeat", False)
        self.until = params.get("Until", None)

        self.AutoRun = params.get("AutoRun", True)
        self.AutoReg = params.get("AutoReg", True)
        self.source = params.get("Source", [])
        self.NoCheckAntiStackCycle = params.get("NoCheckAntiStackCycle", False)
        self.DebugPrintTask = params.get("DebugPrintTask", False)

        self.named = self.AutoReg is True and self.name is not None
        pass

    def getName(self):
        return self.name

    def setSource(self, source):
        self.source = source
        pass

    def getSource(self):
        return self.source

    def setCaller(self, caller):
        self.caller = caller
        pass

    def getCaller(self):
        return self.caller

    def createTaskSource(self):
        return TaskSource(self.source)

    def __enter__(self):
        return self.createTaskSource()

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False

        if len(self.source) == 0:
            Trace.log("TaskChain", 0, "%s empty source task, maybe you forget [with + as]" % (self))
            return True

        if self.AutoRun is True:
            self.run()
        else:
            self.onInitialize()
            pass

        return True

    def _onInitialize(self):
        super(TaskChain, self)._onInitialize()

        TaskManager.addTaskChain(self, self.named)
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("TaskChain", 0, "TaskChain '%s' is not initialize - '%s'" % (self, msg))
        pass

    def _onFinalizeFailed(self, msg):
        Trace.log("TaskChain", 0, "TaskChain '%s' is not finalized - '%s'" % (self, msg))
        pass

    def _onFinalize(self):
        super(TaskChain, self)._onFinalize()

        TaskManager.removeTaskChain(self, self.named)

        self.__finializeSourceTask()

        self.source = []

        for task in self.tasks:
            if task.isInitialized() is True:
                task.cancel()
                pass
            pass

        self.tasks = None

        self.queue = None

        self.node = None
        self.cb = None
        self.cbArgs = None

        self.state = TaskChain.FINALIZE
        pass

    def __initializeSourceTask(self):
        Caller = TaskBase.DEFAULT_CALLER
        if _DEVELOPMENT is True:
            Caller = Trace.caller(1) + ("taskchain",)
            pass

        beginTask = self.createTaskBase("TaskDummy", self.Group, Caller=Caller)

        tg = TaskGenerator(self, self.Group, self.source, beginTask)
        lastTask = tg.parse()

        if lastTask is None:
            Trace.log("TaskChain", 0, "__initializeSourceTask %s invalid initialize SourceTask" % (self))

            return None

        taskCb = self.createTaskBase("TaskCallback", self.Group, Caller=Caller, Cb=self.__complete)
        lastTask.addNext(taskCb)

        if self.repeat is False:
            self.source = None
            pass

        return beginTask

    def __finializeSourceTask(self):
        for task in self.runningTasks:
            task.onFinalize()
            pass

        self.runningTasks = []
        pass

    def isGlobal(self):
        return self.__global

    def setRepeat(self, value):
        self.repeat = value
        pass

    def __checkRepeat(self):
        if self.repeat is False:
            return False

        if self.until is not None:
            result = self.until()

            if isinstance(result, bool) is False:
                Trace.log("TaskChain", 0, "%s result invalid return %s value not [True|False] but %s" % (self, self.until, result))

                return False

            if result is True:
                return False
            pass

        return True

    def __complete(self, isSkip, onComplete):
        # if self.name is not None:
        #    Trace.log("Manager", 0, "_complete %s %s"%(self.name, isSkip))
        #    pass

        onComplete(isSkip)

        self.state = TaskChain.COMPLETE

        TaskManager.endTaskChain(self, self.named)

        repeat = self.__checkRepeat()

        if repeat is True and isSkip is False:
            self.state = TaskChain.IDLE

            self.__finializeSourceTask()

            if self.NoCheckAntiStackCycle is False and self.queue.checkAntiStackCycle() >= 2:
                Trace.log("TaskChain", 0, "%s Anti Stack Cycle %s:%s doc('%s')" % (self, self.caller[0], self.caller[1], self.caller[2]))

                return False

            self.__runTask()

            #ToDo: check if we need to skip the task
            #if isSkip is True:
            #    self.skip()
            #    pass

            return

        cb = self.cb
        cbArgs = self.cbArgs

        self.onFinalize()

        if cb is not None:
            cb(isSkip, *cbArgs)
            pass
        pass

    def createTaskBaseRace(self, group, NoSkip, PrevSkip, caller):
        taskBaseRace = TaskBaseRace()

        taskBaseRace.setRaceNoSkip(NoSkip)
        taskBaseRace.setRacePrevSkip(PrevSkip)

        taskType = TaskManager.getTaskType("TaskRaceNeck")

        if self.setupTaskBase(taskBaseRace, taskType, group, caller, {}) is False:
            return None

        self.tasks.append(taskBaseRace)

        return taskBaseRace

    def createTaskBase(self, typeName, group, **params):
        caller = None
        if _DEVELOPMENT is True:
            caller = params.get("Caller")
            pass

        taskBase = self.createTaskBaseParams(typeName, group, caller, params)

        return taskBase

    def createTaskBaseTypeParams(self, taskType, group, caller, params):
        taskBase = TaskBase()

        if self.setupTaskBase(taskBase, taskType, group, caller, params) is False:
            return None

        self.tasks.append(taskBase)

        return taskBase

    def createTaskBaseParams(self, typeName, group, caller, params):
        taskBase = TaskBase()

        taskType = TaskManager.getTaskType(typeName)

        if taskType is None:
            return None

        if self.setupTaskBase(taskBase, taskType, group, caller, params) is False:
            return None

        self.tasks.append(taskBase)

        return taskBase

    def setupTaskBase(self, taskBase, taskType, group, caller, params):
        taskBase.setTaskType(taskType)
        taskBase.setTaskGroup(group)
        taskBase.setTaskParams(params)

        taskBase.setChain(self)

        if _DEVELOPMENT is True:
            if caller is None:
                Trace.trace()
                pass

            taskBase.setCaller(caller)
            pass

        if taskBase.onInitialize() is False:
            Trace.log("TaskChain", 0, "createTaskBaseParams %s invalid initialize TaskBase %s" % (self, taskType.__name__))

            return False

        if taskBase.isIdle() is False:
            Trace.log("TaskChain", 0, "createTaskBaseParams %s invalid state TaskBase %s state %d" % (self, taskType.__name__, taskBase.state))

            return False

        Skiped = params.get("Skiped", None)

        if Skiped is not None:
            taskBase.setTaskSkiped(Skiped)
            pass

        return True
        pass

    def run(self):
        if self.onInitialize() is False:
            return False

        # print("%s run %s [%s]" % (self, self.state, id(self)))

        if self.__runTask() is False:
            Trace.log("TaskChain", 0, "%s invalid run Task" % (self))

            return False

        if TaskManager.isTaskChainSkiping() is True:
            self.skip()
            pass

        return True

    def __runTask(self):
        self.state = TaskChain.RUN

        TaskManager.runningTaskChain(self, self.named)

        beginTask = self.__initializeSourceTask()

        if beginTask is None:
            Trace.log("TaskChain", 0, "__runTask %s invalid initialize SourceTask" % (self))

            return False

        # if beginTask.run() is False:
        #     return False
        #     pass

        skiping = TaskManager.isTaskChainSkiping()
        self.processTask(beginTask, skiping)

        # if self.queue.push(beginTask, False) is False:
        #     Trace.log("TaskChain", 0, "__runTask %s task invalid run"%(self.name))
        #     pass

        return True

    def processTask(self, task, skip):
        self.queue.push(task, skip)
        pass

    def __skipRunningTasks(self):
        if self.skipInProgress is True:
            return

        self.skipInProgress = True

        # if self.queue is not None:
        #     self.queue.skip()
        #     pass

        for task in self.runningTasks[:]:
            task.skip()
            pass

        self.skipInProgress = False
        pass

    def skip(self):
        #        #print "TaskChain %s %s skip %s"%(self, self.state, [task for task in self.runningTasks])

        if self.state is TaskChain.IDLE:
            return

        if _DEVELOPMENT is True:
            if self.processing is not None:
                Trace.log("TaskChain", 0, "%s skip already processing [%s]" % (self, self.processing))

                return

            self.processing = Trace.caller(0)
            pass

        if self.state is TaskChain.RUN:
            self.__skipRunningTasks()
            pass

        if _DEVELOPMENT is True:
            self.processing = None
            pass
        pass

    def getRunningTasks(self):
        return self.runningTasks

    def cancel(self):
        if _DEVELOPMENT is True:
            if self.processing is not None:
                Trace.log("TaskChain", 0, "%s cancel already processing [%s]" % (self, self.processing))

                return

            self.processing = Trace.caller(0)
            pass

        self.repeat = False

        if self.state not in [TaskChain.IDLE, TaskChain.CANCEL, TaskChain.FINALIZE]:
            if self.state is TaskChain.RUN:
                self.__skipRunningTasks()

                for task in self.runningTasks[:]:
                    task.cancel()
                    pass
                pass

            # if self.queue is not None:
            #     self.queue.skip()
            #     pass

            if self.state not in [TaskChain.COMPLETE, TaskChain.CANCEL, TaskChain.FINALIZE]:
                TaskManager.endTaskChain(self, self.named)
                pass
            pass

        if self.state not in [TaskChain.CANCEL, TaskChain.FINALIZE]:
            self.state = TaskChain.CANCEL
            self.onFinalize()
            pass

        if _DEVELOPMENT is True:
            self.processing = None
            pass
        pass

    def runTask(self, task):
        if self.DebugPrintTask is True:
            Trace.msg("+ chain [%s] task [%s]" % (self.name, task))
            pass

        self.runningTasks.append(task)
        pass

    def completeTask(self, task):
        if task not in self.runningTasks:
            Trace.log("TaskChain", 0, "%s completeTask %s" % (self.name, task))

            return

        if self.DebugPrintTask is True:
            Trace.msg("- chain [%s] task [%s]" % (self.name, task))
            pass

        self.runningTasks.remove(task)
        pass
    pass