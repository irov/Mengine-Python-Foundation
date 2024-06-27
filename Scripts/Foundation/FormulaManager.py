from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager
from RPG.RPGFormules import RPGFormules


class FormulaManager(Manager):
    s_db_module = "Database"
    s_db_name = "Formulas"

    s_formulas = None

    @staticmethod
    def loadFormulas():
        orms = DatabaseManager.getDatabaseORMs(FormulaManager.s_db_module, FormulaManager.s_db_name)

        formulas = FormulaManager.getFormulas()
        if formulas is None:
            formulas = RPGFormules()

        for ORM in orms:
            name = ORM.Name
            code = ORM.Formula

            formulas.addFormula(name, code)

        FormulaManager.setFormulas(formulas)

    @staticmethod
    def setFormulas(rpg_formulas):
        if _DEVELOPMENT is True and isinstance(rpg_formulas, RPGFormules) is False:
            Trace.log("Manager", 0, "Given formulas is wrong type {}, not RPGFormules!!!!!".format(type(rpg_formulas)))
        FormulaManager.s_formulas = rpg_formulas

    @staticmethod
    def getFormulas():
        return FormulaManager.s_formulas

    @staticmethod
    def calculate(formula_name, Value=None, **Variables):
        formulas = FormulaManager.getFormulas()

        if formulas.hasFormula(formula_name) is False:
            Trace.log("Manager", 0, "FormulaManager.calculate formula {!r} not exist in {}"
                      .format(formula_name, formulas.formules.keys()))
            return None

        result = formulas.calcFormula(formula_name, Value, **Variables)

        if result is None and _DEVELOPMENT is True:
            Trace.log("Entity", 0, "FormulaManager.calculate formula %s result is None" % formula_name)

        return result
