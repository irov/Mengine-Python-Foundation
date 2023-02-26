from Foundation.DatabaseManager import DatabaseManager

class Notary(object):
    def __init__(self, name):
        super(Notary, self).__init__()

        self.name = name

        self.storage = {}
        pass

    def addTerms(self, name, terms):
        if name in self.storage:
            Trace.log("Manager", 0, "Notary.addTerms %s terms %s already exist" % (self.name, name))
            return False
            pass

        self.storage[name] = terms

        return True
        pass

    def mergeTerms(self, name, terms):
        if name in self.storage:
            return
            pass

        self.storage[name] = terms
        pass

    def hasTerms(self, name):
        if name not in self.storage:
            return False
            pass

        return True
        pass

    def getTerm(self, name):
        if name not in self.storage:
            Trace.log("Manager", 0, "Notary.getTerms %s term %s not exist" % (self.name, name))
            return None
            pass

        term = self.storage[name]

        return term
        pass

    def merge(self, ORMs):
        for ORM in ORMs:
            if ORM.Name is None:
                Trace.log("Manager", 0, "Notary.merge %s all record need Name" % (self.name))
                return False
                pass

            if hasattr(ORM, "Alias") is True and ORM.Alias is not None:
                if ORM.Alias not in self.storage:
                    Trace.log("Manager", 0, "Notary.merge %s term %s alias %s not found" % (self.name, ORM.Name, ORM.Alias))
                    return False
                    pass

                term_alias = self.storage[ORM.Alias]

                self.mergeTerms(ORM.Name, term_alias)

                continue
                pass

            self.mergeTerms(ORM.Name, ORM)
            pass

        return True
        pass

    def loadParams(self, module, param):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)

        if ORMs is None:
            Trace.log("Manager", 0, "Notary.loadParams %s invalid load database %s.%s" % (self.name, module, param))
            return False
            pass

        for ORM in ORMs:
            if ORM.Name is None:
                Trace.log("Manager", 0, "Notary.loadParams %s param %s all record need Name [ORM - %s]" % (self.name, param, [(k, getattr(ORM, k)) for k in dir(ORM)]))
                return False
                pass

            if self.addTerms(ORM.Name, ORM) is False:
                return False
                pass
            pass

        return True
        pass
    pass