# from Foundation.Task.Task import Task
#
# from Foundation.Task.MixinObserver import MixinObserver
#
# from Foundation.Macro.MacroGlobal import MacroGlobal
#
# class TaskMacroBlock(MixinObserver, Task):
#    def _onParams(self, params):
#        super(TaskMacroBlock, self)._onParams(params)
#        pass
#
#    def _onInitialize(self):
#        super(TaskMacroBlock, self)._onInitialize()
#        pass
#
#    def _onRun(self):
#
#        if MacroGlobal.isBlock() is False:
#            return True
#            pass
#
#        self.addObserver("onMacroBlock", self.__onMacroBlockFilter)
#
#        return False
#        pass
#
#    def __onMacroBlockFilter(self, value):
#        if value is True:
#            return False
#            pass
#
#        return True
#        pass
#    pass