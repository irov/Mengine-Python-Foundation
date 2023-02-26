class TaskQueue(object):
    __slots__ = "append", "AntiStackCycle"

    class Element(object):
        __slots__ = "task", "skip", "next"

        def __init__(self, task, skip):
            self.task = task
            self.skip = skip
            self.next = None
            pass

        def link(self, element):
            element.next = self.next
            self.next = element
            pass
        pass

    def __init__(self):
        self.append = None
        self.AntiStackCycle = 0
        pass

    def isProcess(self):
        return self.append is not None
        pass

    def checkAntiStackCycle(self):
        self.AntiStackCycle += 1

        return self.AntiStackCycle
        pass

    def push(self, task, skip):
        element = TaskQueue.Element(task, skip)

        if self.append is not None:
            self.append.link(element)
            self.append = element

            return True
            pass

        return self.process(element)
        pass

    def process(self, current):
        while current is not None:
            self.append = current

            if self.process_task(current) is False:
                return False
                pass

            current = current.next
            pass

        self.AntiStackCycle = 0

        self.append = None

        return True
        pass

    def process_task(self, current):
        task = current.task

        # if task.chain is not None and task.chain.getName() is not None:
        #    print task.chain.getName(), task.taskType, task.taskParams, current.skip, task.isSkiped()
        #    pass

        if current.skip is False and task.isSkiped() is False:
            if task.run() is False:
                return False
                pass
            pass
        else:
            if task.skip() is False:
                return False
                pass
            pass

        return True
        pass

    pass