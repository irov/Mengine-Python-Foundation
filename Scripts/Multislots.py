def baseslots(*slots):
    def __meta(cls, name, bases, classdict):
        new_classdict = {}
        new_classdict.update(classdict)

        new_classdict.update(__slots__=())
        new_classdict.update(__multislots__=slots)

        return type(name, bases, new_classdict)

    return type("meta_baseslots", (type,), dict(__new__=__meta))

def finalslots(*slots):
    def __meta(cls, name, bases, classdict):
        mro = type(name, bases, {}).mro()

        final_slots = []

        for b in mro[1:]:
            if hasattr(b, "__multislots__") is False:
                continue

            final_slots.extend(b.__multislots__)
            pass

        final_slots.extend(slots)

        if len(slots) > len(set(slots)):
            raise TypeError("type %s finalslots have dublicate attributes" % (name))

        new_classdict = {}
        new_classdict.update(classdict)

        new_classdict.update(__slots__=final_slots)
        new_classdict.update(__multislots__=slots)

        return type(name, bases, new_classdict)

    return type("meta_finalslots", (type,), dict(__new__=__meta))