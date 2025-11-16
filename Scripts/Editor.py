from Foundation.SceneManager import SceneManager

def GetLayoutEditorSceneName():
    Scene = SceneManager.getCurrentScene()

    return Scene.getName()

def GetLayoutEditorSceneGroups():
    Scene = SceneManager.getCurrentScene()

    groups = []
    def __foreachGroups(group):
        if group is None:
            return
        groups.append(group)

    Scene.foreachGroups(__foreachGroups)

    return groups

def GetLayoutEditorObjectAttributes(obj):
    from Foundation.Params import DefaultParam

    PARAMS_WIDGETS = getattr(obj.__class__, "PARAMS_WIDGETS", {})

    params = obj.getParams()

    attributes = {}

    for key, param in params.iteritems():
        def __getAttributeValue(param):
            if isinstance(param, DefaultParam) is True:
                return param.value
            return param
        value = __getAttributeValue(param)
        Widget = PARAMS_WIDGETS.get(key)
        attributes[key] = (value, Widget)
        pass

    return attributes

def SetLayoutEditorObjectAttributeValue(obj, name, value):
    obj.setParam(name, value)
    pass

def GetLayoutEditorObjectChildren(obj):
    children = []

    def __visit(child):
        children.append(child)

    obj.visitChildren(__visit)

    return children

def GetLayoutEditorObjectEntityNode(obj):
    return obj.getEntityNode()