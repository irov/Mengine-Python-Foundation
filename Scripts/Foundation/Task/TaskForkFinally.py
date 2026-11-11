from Foundation.Task.TaskForkSource import TaskForkSource
from Foundation.TaskManager import TaskManager

class TaskForkFinally(TaskForkSource):
    @staticmethod
    def onCancelIdle(base):
        if TaskManager.isInitialized() is False:
            return

        # Stop the generated tasks before releasing their resources.
        base._cancelPrev()

        group = base.taskGroup

        if group is None:
            group = base.chain.Group
            pass

        taskChain = TaskManager.createTaskChain(Caller=base.caller, Group=group)

        taskChain.setSource(base.taskParams.get("Source"))

        taskChain.run()
        pass
    pass
