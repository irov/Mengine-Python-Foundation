from Foundation.Manager import Manager
from Foundation.Group import Group
from Foundation.GroupManager import GroupManager
from Foundation.Object.BaseObject import BaseObject
from Foundation.Object.ChildObject import ChildObject
from Foundation.Params import DefaultParam

class SaveDict(object):
    __slots__ = ("value",)

    def __init__(self, value):
        super(SaveDict, self).__init__()

        self.value = value
        pass
    pass

class SaveConstString(object):
    __slots__ = ("value",)

    def __init__(self, value):
        super(SaveConstString, self).__init__()

        self.value = str(value)
        pass
    pass

class SaveObjectRef(object):
    __slots__ = ("value",)

    def __init__(self, value):
        super(SaveObjectRef, self).__init__()

        self.value = value
        pass
    pass

class SaveGroupRef(object):
    __slots__ = ("value",)

    def __init__(self, value):
        super(SaveGroupRef, self).__init__()

        self.value = value
        pass
    pass

class SaveManager(Manager):
    @staticmethod
    def getPickleTypes():
        return [SaveDict, SaveConstString, SaveObjectRef, SaveGroupRef]

    @staticmethod
    def saveObject(obj):
        name = obj.getName()

        if obj.isSavable() is True:
            save_obj = obj._onSave()
            try:
                save_value = SaveManager._saveValue(save_obj)
            except Exception as ex:
                raise Exception("SaveManager.saveObject '%s' name '%s' _saveValue error: %s" % (obj.getType(), name, ex))

            save_data = (name, save_value)

            return save_data

        params = obj.getParams()

        try:
            save_params = SaveManager._saveParams(params)
        except Exception as ex:
            raise Exception("SaveManager.saveObject '%s' name '%s' _saveParams error: %s" % (obj.getType(), name, ex))

        save_child_objs = []
        if isinstance(obj, ChildObject) is True:
            child_objs = obj.getObjects()

            for child_obj in child_objs:
                if child_obj.isSaving() is False:
                    continue

                save_child_obj = SaveManager.saveObject(child_obj)

                save_child_objs.append(save_child_obj)
                pass
            pass

        save_obj = (save_params, save_child_objs)

        save_data = (name, save_obj)

        return save_data

    @staticmethod
    def loadObject(group, load_data):
        name, load_obj = load_data

        obj = group.getObject(name)

        if obj is None:
            Trace.log("Manager", 0, "load object {} not found".format(name))

            return True

        if obj.isSavable() is True:
            load_value = SaveManager.getValue(load_obj)
            obj._onLoad(load_value)
        else:
            load_params, load_child_objs = load_obj
            params = SaveManager._loadParams(load_params)

            if isinstance(obj, ChildObject) is True:
                for load_child_obj in load_child_objs:
                    SaveManager.loadObject(obj, load_child_obj)
                    pass
                pass

            obj.loadParams(params)
            pass

        return True

    @staticmethod
    def saveGroup(group):
        objs = group.getObjects()

        save_objs = []

        for obj in objs:
            if obj.isSaving() is False:
                continue

            save_obj = SaveManager.saveObject(obj)

            save_objs.append(save_obj)
            pass

        groupName = group.getName()

        save_data = (groupName, save_objs)

        return save_data

    @staticmethod
    def loadGroup(load_group):
        groupName, load_objs = load_group

        group = GroupManager.getGroup(groupName)

        if group is None:
            return False

        for load_data in load_objs:
            if SaveManager.loadObject(group, load_data) is False:
                return False
            pass

        return True

    @staticmethod
    def _saveParams(params):
        save_params = []
        for key, value in params.iteritems():
            try:
                save_value = SaveManager._saveValue(value)
            except Exception as ex:
                raise Exception("_saveParams key '%s' value '%s' error: %s" % (key, value, ex))

            save_param = (key, save_value)
            save_params.append(save_param)
            pass

        return save_params

    @staticmethod
    def _loadParams(save_params):
        params = {}

        for key, pickle_value in save_params:
            value = SaveManager._loadValue(pickle_value)

            params[key] = value
            pass

        return params

    @staticmethod
    def _saveValue(value):
        if value is None:
            return None

        if isinstance(value, DefaultParam) is True:
            value = value.value
            pass

        if isinstance(value, (unicode, str, float, long, int, bool)) is True:
            return value

        save_value = None

        if isinstance(value, tuple) is True:
            temp_save_value = []

            for v in value:
                save_v = SaveManager._saveValue(v)
                temp_save_value.append(save_v)
                pass

            save_value = tuple(temp_save_value)
            pass
        elif isinstance(value, list) is True:
            save_value = []

            for v in value:
                save_v = SaveManager._saveValue(v)
                save_value.append(save_v)
                pass
            pass
        elif isinstance(value, dict) is True:
            dict_list = []

            for k, v in value.iteritems():
                save_k = SaveManager._saveValue(k)
                save_v = SaveManager._saveValue(v)

                dict_list.append((save_k, save_v))
                pass

            save_value = SaveDict(dict_list)
            pass
        elif isinstance(value, Group) is True:
            groupName = value.getName()
            save_value = SaveGroupRef(groupName)
            pass
        elif isinstance(value, BaseObject) is True:
            object_path = []

            def __getObjectPath(value, path):
                name = value.getName()
                path.append(name)

                group = value.getGroup()

                if isinstance(group, Group) is True:
                    groupName = group.getName()
                    return groupName
                elif isinstance(group, BaseObject) is True:
                    objectPath = __getObjectPath(group, path)
                    return objectPath
                else:
                    raise Exception("__getObjectPath '%s' invalid group type '%s' for object '%s' type '%s'" % (group, type(group), value.getName(), type(value)))

            groupName = __getObjectPath(value, object_path)

            save_value = SaveObjectRef((groupName, object_path))
            pass
        elif Mengine.is_class(value) is True:
            if isinstance(value, Mengine.vec2f) is True:
                save_value = (value.x, value.y)
                pass
            elif isinstance(value, Mengine.vec3f) is True:
                save_value = (value.x, value.y, value.z)
                pass
            elif isinstance(value, Mengine.ConstString) is True:
                save_value = SaveConstString(value)
                pass
            else:
                raise Exception("isinstance('%s', Mengine.pybind_base_type) is True" % (value))
        else:
            raise Exception("_saveValue '%s' invalid pickle type '%s'" % (value, type(value)))

        return save_value
    pass

    @staticmethod
    def getValue(load_value):
        value = SaveManager._loadValue(load_value)
        return value

    @staticmethod
    def _loadValue(load_value):
        if load_value is None:
            return None

        if isinstance(load_value, (unicode, str, float, long, int, bool)) is True:
            return load_value

        value = None

        if isinstance(load_value, tuple) is True:
            temp_value = []
            for v in load_value:
                load_v = SaveManager._loadValue(v)

                temp_value.append(load_v)
                pass

            value = tuple(temp_value)
            pass
        elif isinstance(load_value, list) is True:
            value = []
            for v in load_value:
                load_v = SaveManager._loadValue(v)

                value.append(load_v)
                pass
            pass
        elif isinstance(load_value, SaveDict) is True:
            value = {}

            for k, v in load_value.value:
                load_k = SaveManager._loadValue(k)
                load_v = SaveManager._loadValue(v)

                value[load_k] = load_v
                pass
            pass
        elif isinstance(load_value, SaveObjectRef) is True:
            groupName, path = load_value.value
            group = GroupManager.getGroup(groupName)

            object = group
            for obj_name in reversed(path):
                object = object.getObject(obj_name)
                pass

            value = object
            pass
        elif isinstance(load_value, SaveGroupRef) is True:
            value = GroupManager.getGroup(load_value.value)
            pass
        elif isinstance(load_value, SaveConstString) is True:
            value = load_value.value
            pass
        else:
            raise Exception("_loadValue '%s' invalid pickle type '%s'" % (load_value, type(load_value)))

        return value

    @staticmethod
    def saveGroups():
        save_groups = []
        for group in GroupManager.s_groups.itervalues():
            if isinstance(group, GroupManager.EmptyGroup):
                continue

            if group.getSave() is False:
                continue

            try:
                save_group = SaveManager.saveGroup(group)
            except Exception as ex:
                raise Exception("SaveManager.saveGroups group '%s' error: %s" % (group.getName(), ex))

            save_groups.append(save_group)
            pass

        return save_groups
    pass