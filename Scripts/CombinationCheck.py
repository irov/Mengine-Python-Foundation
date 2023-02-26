class CombinationCheck():
    def __init__(self, combination, callback, *cbparams):
        self.combination = combination
        self.callback = callback
        self.cbparams = cbparams

        self.combIndex = 0

        self.done = False
        pass

    def checkCombination(self, key):
        if self.done == True:
            return

        if key == self.combination[self.combIndex]:
            if self.combIndex == (len(self.combination) - 1):
                self.callback(*self.cbparams)
                self.done == True
                return
                pass
            self.combIndex += 1
            pass
        elif self.combIndex != 0:
            self.combIndex = 0
            self.checkCombination(key)
            pass
        pass
    pass