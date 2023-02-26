from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.MixinNode import MixinNode

class TaskManager(object):
    s_skiped = False
    s_finalize = False

    s_types = {}
    s_typesDomain = {}

    s_runningNamedChain = {}
    s_idleNamedChain = {}

    s_runningChain = []
    s_idleChain = []

    @staticmethod
    def onFinalize():
        for chain in TaskManager.s_runningChain[:]:
            chain.cancel()
            pass

        TaskManager.s_finalize = True

        TaskManager.s_runningNamedChain = {}
        TaskManager.s_idleNamedChain = {}

        TaskManager.s_runningChain = []
        TaskManager.s_idleChain = []

        TaskManager.s_types = {}
        pass

    @staticmethod
    def cancelTasks():
        for chain in TaskManager.s_runningChain[:]:
            chain.cancel()
            pass
        pass

    @staticmethod
    def importTasks(module, names):
        for name in names:
            TaskManager.importTask(module, name)
            pass
        pass

    @staticmethod
    def importTask(module, name):
        TaskManager.s_types[name] = module
        pass

    @staticmethod
    def __importTaskDomain(module, name):
        Name = "%s" % (name)
        FromName = module
        ModuleName = "%s.%s" % (FromName, Name)

        try:
            Module = __import__(ModuleName, fromlist=[FromName])
        except ImportError as ex:
            Trace.log("Manager", 0, "TaskManager.__importTaskDomain %s:%s import error %s" % (module, name, ex))

            return None
            pass

        Type = getattr(Module, Name)

        return Type
        pass

    @staticmethod
    def getTaskType(typeName):
        if typeName not in TaskManager.s_types:
            Trace.log("TaskManager", 0, "TaskManager.getTaskType: not found %s" % (typeName))

            return None
            pass

        type = TaskManager.s_typesDomain.get(typeName)

        if type is None:
            module = TaskManager.s_types[typeName]
            type = TaskManager.__importTaskDomain(module, typeName)

            if type is None:
                Trace.log("TaskManager", 0, "TaskManager.getTaskType: invalid import task %s from module %s" % (typeName, module))

                return None
                pass

            TaskManager.s_typesDomain[typeName] = type
            pass

        return type
        pass

    @staticmethod
    def createTask(taskType, base, chain, group, params):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "create Task %s after finalize" % (taskType))
            return None
            pass

        if taskType is None:
            Trace.log("TaskManager", 0, "TaskManager.createTask: taskType is None")

            return None
            pass

        task = taskType()

        task.setBase(base)

        try:
            task.onParams(params)
        except KeyError as ex:
            Trace.log("TaskManager", 0, "TaskManager.createTask: Task %s except %s" % (taskType, ex))

            return None
            pass

        if issubclass(taskType, MixinGroup) is True:
            def __updateMixinGroupParams(params, chain, group):
                if "GroupName" in params:
                    return None
                    pass

                params_group = params.get("Group")

                if params_group is not None:
                    return params_group
                    pass

                if group is not None:
                    return group
                    pass

                if chain.Group is not None:
                    return chain.Group
                    pass

                return None
                pass

            def __updateMixinGroupNameParams(params, chain, group):
                params_group_name = params.get("GroupName")

                if params_group_name is not None:
                    return params_group_name
                    pass

                if group is not None:
                    return group.name
                    pass

                if chain.GroupName is not None:
                    return chain.GroupName
                    pass

                return None
                pass

            def __updateMixinDemonNameParams(params, chain):
                params_demon_name = params.get("DemonName")

                if params_demon_name is not None:
                    return params_demon_name
                    pass

                if chain.DemonName is not None:
                    return chain.DemonName
                    pass

                return None
                pass

            Group = __updateMixinGroupParams(params, chain, group)
            task.setGroup(Group)

            GroupName = __updateMixinGroupNameParams(params, chain, group)
            task.setGroupName(GroupName)

            DemonName = __updateMixinDemonNameParams(params, chain)
            task.setDemonName(DemonName)
            pass

        if issubclass(taskType, MixinNode) is True:
            node = params.get("Node", chain.node)

            task.setNode(node)
            pass

        return task
        pass

    @staticmethod
    def createTaskChain(Caller=None, CallerDeep=0, **params):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "create TaskChain after finalize")
            return
            pass

        taskChainType = TaskManager.getTaskType("TaskChain")

        if taskChainType is None:
            Trace.log("TaskManager", 0, "TaskManager.createTaskChain: Task type 'TaskChain' not register")

            return None
            pass

        taskChain = taskChainType()

        try:
            taskChain.onParams(params)
        except KeyError as ex:
            Trace.log("TaskManager", 0, "TaskManager.createTaskChain: onParams except %s" % (ex))

            return None
            pass

        if _DEVELOPMENT is True:
            if Caller is None:
                Caller = Trace.caller(CallerDeep) + ("global",)
                pass

            taskChain.setCaller(Caller)
            pass

        return taskChain
        pass

    @staticmethod
    def runAlias(name, cb, **params):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "run Alias after finalize")
            return
            pass

        with TaskManager.createTaskChain(CallerDeep=1, Cb=cb) as tc:
            tc.addTask(name, **params)
            pass
        pass

    @staticmethod
    def runningTaskChain(chain, named):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "running TaskChain after finalize")
            return
            pass

        Trace.log("TaskManager", 1, "TaskManager.runTaskChain %s" % (chain.name))

        if named is True:
            TaskManager.s_runningNamedChain[chain.name] = chain
            pass

        TaskManager.s_runningChain.append(chain)
        pass

    @staticmethod
    def endTaskChain(chain, named):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "end TaskChain after finalize")
            return
            pass

        Trace.log("TaskManager", 1, "TaskManager.endTaskChain %s" % (chain.name))

        TaskManager.s_runningChain.remove(chain)

        if named is True:
            if chain.name not in TaskManager.s_runningNamedChain:
                Trace.log("TaskManager", 0, "TaskManager.endTaskChain %s not exist" % (chain.name))
                return
                pass

            TaskManager.s_runningNamedChain.pop(chain.name)
            pass
        pass

    @staticmethod
    def skipTasks(exceptOfTask=None, skipGlobal=True):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "skip Tasks after finalize")
            return
            pass

        TaskManager.s_skiped = True

        for task in TaskManager.s_runningChain[:]:
            if skipGlobal is False:
                if task.isGlobal() is True:
                    continue
                    pass
                pass

            if exceptOfTask is not task:
                task.skip()
                pass
            pass

        TaskManager.s_skiped = False
        pass

    @staticmethod
    def isTaskChainSkiping():
        return TaskManager.s_skiped
        pass

    @staticmethod
    def addTaskChain(chain, named):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "add TaskChain after finalize")
            return
            pass

        Trace.log("TaskManager", 1, "TaskManager.addTaskChain %s" % (chain.name))

        if named is True:
            if chain.name in TaskManager.s_idleNamedChain:
                Trace.log("TaskManager", 0, "TaskManager.addTaskChain %s already exist" % (chain.name))
                return
                pass

            TaskManager.s_idleNamedChain[chain.name] = chain
            pass

        TaskManager.s_idleChain.append(chain)
        pass

    @staticmethod
    def existTaskChain(name):
        return name in TaskManager.s_idleNamedChain
        pass

    @staticmethod
    def removeTaskChain(chain, named):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "remove TaskChain after finalize")
            return
            pass

        Trace.log("TaskManager", 1, "TaskManager.removeTaskChain %s" % (chain.name))

        if named is True:
            if chain.name not in TaskManager.s_idleNamedChain:
                Trace.log("TaskManager", 0, "TaskManager.removeTaskChain %s not exist" % (chain.name))

                return
                pass

            TaskManager.s_idleNamedChain.pop(chain.name)
            pass

        TaskManager.s_idleChain.remove(chain)
        pass

    @staticmethod
    def runTaskChain(name):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "run TaskChain after finalize")
            return False
            pass

        if name not in TaskManager.s_idleNamedChain:
            Trace.log("TaskManager", 0, "TaskManager.runChain %s not exist" % (name))
            return False
            pass

        chain = TaskManager.s_idleNamedChain.get(name)

        isValid = chain.run()

        return isValid
        pass

    @staticmethod
    def cancelTaskChain(name, exist=True):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "cancel TaskChain after finalize")
            return
            pass

        if name not in TaskManager.s_idleNamedChain:
            if exist is True:
                Trace.log("TaskManager", 0, "TaskManager.cancelChain %s not exist" % (name))
                pass

            return
            pass

        chain = TaskManager.s_idleNamedChain.get(name)

        chain.cancel()
        pass

    @staticmethod
    def skipTaskChain(name):
        if TaskManager.s_finalize is True:
            Trace.log("TaskManager", 0, "skip TaskChain after finalize")
            return
            pass

        if name not in TaskManager.s_idleNamedChain:
            Trace.log("TaskManager", 0, "TaskManager.skipChain %s not exist" % (name))
            return
            pass

        chain = TaskManager.s_idleNamedChain.get(name)

        chain.skip()
        pass
    pass