class Contract(object):
    INIT = 0
    READY = 1
    WAIT = 2
    AWARD = 3
    COMPLETE = 4
    CANCEL = 5

    def __init__(self):
        self.Name = None
        self.time = 0

        self.bank_from = None
        self.bank_to = None

        self.term_check = None
        self.term_pay = None
        self.term_award = None
        self.term_cancel = None

        self.scheduler = None
        self.scheduleId = 0

        self.state = Contract.INIT
        pass

    def initialize(self, Name, scheduler, time, terms, bank_from, bank_to):
        if self.state != Contract.INIT:
            return False
            pass

        self.Name = Name

        self.scheduler = scheduler
        self.time = time

        self.bank_from = bank_from
        self.bank_to = bank_to

        self.term_check = terms.get("Check")
        self.term_pay = terms.get("Pay")
        self.term_award = terms.get("Award")
        self.term_cancel = terms.get("Cancel")

        if self.__checkResources(self.term_check) is False:
            return False
            pass

        if self.__checkResources(self.term_pay) is False:
            return False
            pass

        if self.__checkResources(self.term_award) is False:
            return False
            pass

        if self.__checkResources(self.term_cancel) is False:
            return False
            pass

        self.state = Contract.READY

        return True
        pass

    def __checkResources(self, term):
        if term is None:
            return True
            pass

        if self.bank_from.checkResources(term) is False:
            return False
            pass

        if self.bank_to.checkResources(term) is False:
            return False
            pass

        return True
        pass

    def getBankFrom(self):
        return self.bank_from
        pass

    def getBankTo(self):
        return self.bank_to
        pass

    def restart(self, cb):
        if self.state != Contract.COMPLETE:
            return False
            pass

        self.state = Contract.READY

        successful = self.run(cb)

        return successful
        pass

    def run(self, cb):
        if self.state != Contract.READY:
            return False
            pass

        if self.__check() is False:
            return False
            pass

        self.__pay()

        if self.time == 0:
            self.__award()

            self.state = Contract.COMPLETE

            self.__notify(cb, True)
            pass
        else:
            def __wait(id, skip):
                if self.scheduleId != id:
                    return
                    pass

                if skip is False:
                    self.state = Contract.AWARD
                    self.__award()
                    self.state = Contract.COMPLETE
                    pass
                else:
                    self.state = Contract.CANCEL
                    self.__cancel()
                    pass

                self.__notify(cb, skip is False)
                pass

            self.state = Contract.WAIT

            self.scheduleId = self.scheduler.schedule(self.time, __wait)
            pass

        return True
        pass

    def cancel(self):
        if self.state != Contract.WAIT:
            return False
            pass

        if self.scheduler.remove(self.scheduleId) is False:
            return False
            pass

        return True
        pass

    def check(self):
        if self.term_check is not None:
            for key, value in self.term_check.iteritems():
                if self.bank_from.validResource(key, value) is False:
                    return False
                    pass
                pass
            pass

        if self.term_pay is not None:
            for key, value in self.term_pay.iteritems():
                if self.bank_from.validResource(key, value) is False:
                    return False
                    pass
                pass
            pass

        if self.term_award is not None:
            for key, value in self.term_award.iteritems():
                if self.bank_from.validResource(key, value) is False:
                    return False
                    pass
                pass
            pass

        return True
        pass

    def CheckHaveWhatPay(self):
        resHave = self.bank_from.viewAllResources()
        for key, value in self.term_award.iteritems():
            valIn = resHave[key]
            test = self.bank_to.testResource(key, valIn)
            if valIn > 0 and test > 0:
                return True
                pass
            pass
        return False
        pass

    def __notify(self, cb, complete):
        # bank_to_full = self.bank_to.isFull()
        # bank_from_empty = self.bank_from.isEmpty()
        #
        # cb(self, bank_to_full, bank_from_empty)

        cb(self, self.bank_from, self.bank_to, complete)
        pass

    def __check(self):
        if self.term_check is None:
            return True
            pass

        for key, value in self.term_check.iteritems():
            if self.bank_from.validResource(key, value) is False:
                return False
                pass
            pass

        return True
        pass

    def __pay(self):
        if self.term_pay is None:
            return
            pass

        self.__process(self.term_pay, self.bank_from, self.bank_to)
        pass

    def __award(self):
        if self.term_award is None:
            return
            pass

        self.__process(self.term_award, self.bank_from, self.bank_to)
        pass

    def __cancel(self):
        if self.term_cancel is None:
            return
            pass

        self.__process(self.term_cancel, self.bank_to, self.bank_from)
        pass

    def __process(self, resources, bank_from, bank_to):
        for key, value in resources.iteritems():
            test_value = bank_to.testResource(key, value)
            get_value = bank_from.getResource(key, test_value)
            bank_to.addResource(key, get_value)
            pass
        pass
    pass