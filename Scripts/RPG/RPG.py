import random

class RPGUnit(object):
    def __init__(self):
        self.attributes = {}
        self.buffs = []
        pass

    def addAttribute(self, name, value):
        self.attributes[name] = value
        pass

    def addBuff(self, buff):
        self.buffs.append(buff)
        pass

    def makeAttributes(self):
        total_attributes = self.attributes.copy()
        total_exceptions = {}

        for buff in self.buffs:
            buff.onBuffException(total_exceptions)
            pass

        for buff in self.buffs:
            buff.onBuffBase(total_attributes, total_exceptions)
            pass

        for buff in self.buffs:
            buff.onBuffOver(total_attributes, total_exceptions)
            pass

        return total_attributes
        pass
    pass

class RPGManager(object):
    def __init__(self):
        self.formules = {}
        pass

    @staticmethod
    def __Rand(Value):
        if Value == 0.0:
            return False
            pass
        elif Value == 1.0:
            return True
            pass

        return random.random() <= Value
        pass

    def __makeFormulaCode(self, name, code):
        c = compile(code, '<string>', 'exec')

        sandbox = dict(Rand=RPGManager.__Rand)
        sandbox.update(self.formules)

        try:
            exec(c, sandbox)
        except Exception as ex:
            print("ex: function %s error: %s" % (name, ex))

            raise ex
            pass

        f = sandbox[name]

        return f
        pass

    def addFormula(self, name, function):
        f = self.__makeFormulaCode(name, function)

        self.formules[name] = f
        pass

    def calcFormulaAttributeSelf(self, FormulaName, Self):
        SelfAttributes = Self.makeAttributes()

        SelfType = type("Self", (object,), SelfAttributes)

        Formula = self.formules[FormulaName]

        Result = Formula(SelfType)

        return Result
        pass

    def calcFormulaAttributeOther(self, FormulaName, Self, Other):
        SelfAttributes = Self.makeAttributes()
        OtherAttributes = Other.makeAttributes()

        SelfType = type("Self", (object,), SelfAttributes)
        OtherType = type("Other", (object,), OtherAttributes)

        Formula = self.formules[FormulaName]

        Result = Formula(SelfType, OtherType)

        return Result
        pass
    pass

class BaseBuff(object):
    def __init__(self, value):
        self.value = value
        pass

    def onBuffException(self, exceptions):
        pass

    def onBuffBase(self, attributes, exceptions):
        attributes["PhysicDamage"] += self.value
        pass

    def onBuffOver(self, attributes, exceptions):
        pass
    pass

rpg = RPGManager()

ResistFunction = """
def Resist(Value):
    if Value > 100.0:
        Result = 0.0
        pass
    elif Value < 0.0:
        Result = 1.0 + (-Value) / 100.0 + (-Value) * (-Value) / 500.0
        pass
    else:
        Result = (100.0 - Value) / 100.0
        pass

    return Result
    pass
"""

rpg.addFormula("Resist", ResistFunction)

CritFunction = """
def Crit(Value):
    Result = 1.0

    for chance, multiplier in Value:
        if Rand(chance) is True:
            Result = multiplier
            break
            pass
        pass

    return Result
    pass
"""

rpg.addFormula("Crit", CritFunction)

BlockFunction = """
def Block(Value, Second):
    Result = Value

    for chance, dmg in Second:
        if Rand(chance) is True:
            Result -= dmg

            if Result <= 0.0:
                Result = 0.0
                break
                pass
            pass
        pass

    return Result
    pass
"""

rpg.addFormula("Block", BlockFunction)

EvadeFunction = """
def Evade(Value):
    Result = 1.0
    for chance in Value:
        if Rand(chance) is True:
            Result = 0.0
            break
            pass
        pass

    return Result
    pass
"""

rpg.addFormula("Evade", EvadeFunction)

HelthFormula = """
def Helth(Self):
    return Self.BaseHealth + Self.Strength * 0.1
    pass
"""

rpg.addFormula("Helth", HelthFormula)

AttackSpeedFormula = """
def AttackSpeed(Self):
    return Self.BaseAttackSpeed + Self.Agility * 0.1 + Self.Advertency * 0.05
    pass
"""

rpg.addFormula("AttackSpeed", AttackSpeedFormula)

DamageFormula = """
def Damage(Self, Other):
    physicd = Self.PhysicDamage * Resist(Other.PhysicResist) * Crit(Self.PhysicCrit)

    fpd = physicd
    fpd = Block(fpd, Other.PhysicBlock)
    fpd *= Evade(Other.PhysicEvade)

    magicd = Self.MagicDamage * Resist(Other.MagicResist) * Crit(Self.MagicCrit)

    fired = Self.FireDamage * Resist(Other.MagicResist * 0.5) * Resist(Other.FireResist)
    iced = Self.IceDamage * Resist(Other.MagicResist * 0.5) * Resist(Other.IceResist)
    lightd = Self.LightDamage * Resist(Other.MagicResist * 0.5) * Resist(Other.LightResist)

    fmd = magicd
    fmd = Block(fmd, Other.MagicBlock)
    fmd *= Evade(Other.MagicEvade)

    pured = Self.PureDamage

    fed = fired + iced + lightd

    totald = fpd + fmd + fed + pured
    totald *= Resist(Other.PureResist)

    return totald
    pass
"""

rpg.addFormula("Damage", DamageFormula)

unit1 = RPGUnit()

unit1.addAttribute("BaseHealth", 100)

unit1.addAttribute("Strength", 10)
unit1.addAttribute("Agility", 5)
unit1.addAttribute("Advertency", 5)
unit1.addAttribute("Intelligence", 2)

unit1.addAttribute("PhysicDamage", 20)
unit1.addAttribute("MagicDamage", 0.0)
unit1.addAttribute("FireDamage", 0.0)
unit1.addAttribute("IceDamage", 0.0)
unit1.addAttribute("LightDamage", 0.0)
unit1.addAttribute("PureDamage", 0.0)

unit1.addAttribute("PhysicResist", 0.0)
unit1.addAttribute("MagicResist", 0.0)
unit1.addAttribute("FireResist", 0.0)
unit1.addAttribute("IceResist", 0.0)
unit1.addAttribute("LightResist", 0.0)
unit1.addAttribute("PureResist", 0.0)

unit1.addAttribute("PhysicCrit", [(1.0, 1.0)])
unit1.addAttribute("MagicCrit", [(1.0, 1.0)])

unit1.addAttribute("PhysicEvade", [0.0])
unit1.addAttribute("MagicEvade", [0.0])

unit1.addAttribute("PhysicBlock", [(0.0, 0.0)])
unit1.addAttribute("MagicBlock", [(0.0, 0.0)])

unit2 = RPGUnit()

unit2.addAttribute("BaseHealth", 100)

unit2.addAttribute("Strength", 10)
unit2.addAttribute("Agility", 5)
unit2.addAttribute("Advertency", 5)
unit2.addAttribute("Intelligence", 2)

unit2.addAttribute("PhysicDamage", 20)
unit2.addAttribute("MagicDamage", 0.0)
unit2.addAttribute("FireDamage", 0.0)
unit2.addAttribute("IceDamage", 0.0)
unit2.addAttribute("LightDamage", 0.0)
unit2.addAttribute("PureDamage", 0.0)

unit2.addAttribute("PhysicResist", 10.0)
unit2.addAttribute("MagicResist", 0.0)
unit2.addAttribute("FireResist", 0.0)
unit2.addAttribute("IceResist", 0.0)
unit2.addAttribute("LightResist", 0.0)
unit2.addAttribute("PureResist", 0.0)

unit2.addAttribute("PhysicCrit", [(1.0, 1.0)])
unit2.addAttribute("MagicCrit", [(1.0, 1.0)])

unit2.addAttribute("PhysicEvade", [0.5])
unit2.addAttribute("MagicEvade", [0.0])

unit2.addAttribute("PhysicBlock", [(0.2, 10.0)])
unit2.addAttribute("MagicBlock", [(0.0, 0.0)])

a = rpg.calcFormulaAttributeOther("Damage", unit1, unit2)

print(a)
print("done")