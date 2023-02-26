def baseslots(*slots):
    def meta(cls, name, bases, classdict):
        new_classdict = {}
        new_classdict.update(classdict)

        new_classdict.update(__slots__=())
        new_classdict.update(__multislots__=slots)

        return type(name, bases, new_classdict)
        pass

    return type("meta_baseslots", (type,), dict(__new__=meta))
    pass

def finalslots(*slots):
    def meta(cls, name, bases, classdict):
        mro = type(name, bases, {}).mro()

        final_slots = []

        for b in mro[1:]:
            if hasattr(b, "__multislots__") is False:
                continue
                pass

            final_slots.extend(b.__multislots__)
            pass

        final_slots.extend(slots)

        if len(slots) > len(set(slots)):
            raise TypeError("type %s finalslots have dublicate attributes" % (name))

            return None
            pass

        new_classdict = {}
        new_classdict.update(classdict)

        new_classdict.update(__slots__=final_slots)
        new_classdict.update(__multislots__=slots)

        return type(name, bases, new_classdict)
        pass

    return type("meta_finalslots", (type,), dict(__new__=meta))
    pass