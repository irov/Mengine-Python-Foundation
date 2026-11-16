class AdminPanelElementBuilder(object):
    def __init__(self, description):
        self._description = description

    def _set(self, name, value):
        self._description[name] = value
        return self

    @staticmethod
    def _number(value, positive=False, dimension=False):
        if type(value) not in (int, long, float):
            raise ValueError("OpButton value must be a number")

        try:
            value = float(value)
        except OverflowError:
            raise ValueError("OpButton value must be finite")

        if value != value or abs(value) == float("inf"):
            raise ValueError("OpButton value must be finite")

        if positive is True and value <= 0:
            raise ValueError("OpButton value must be positive")

        if dimension is True and (value < 0 or value > 4096):
            raise ValueError("OpButton dimension must be between 0 and 4096")

        return value

    @staticmethod
    def _string(value):
        if isinstance(value, basestring) is False:
            raise ValueError("OpButton value must be a string")
        return value

    @staticmethod
    def _boolean(value):
        if type(value) is not bool:
            raise ValueError("OpButton value must be a boolean")
        return value

    @staticmethod
    def _choice(value, choices):
        if value not in choices:
            raise ValueError("Invalid OpButton value: {}".format(value))
        return value

    def _place(self, name, value):
        self._description.setdefault("placement", {})[name] = value
        return self

    def width(self, value):
        return self._place("width", self._number(value, True, True))

    def contentWidth(self):
        return self._place("width", "content")

    def fill(self, weight=1):
        self._place("weight", self._number(weight, True, True))
        return self._place("width", "fill")

    def minWidth(self, value):
        return self._place("minWidth", self._number(value, False, True))

    def maxWidth(self, value):
        return self._place("maxWidth", self._number(value, True, True))

    def alignSelf(self, value):
        return self._place("alignSelf", self._choice(value, ("start", "center", "end", "stretch")))


class AdminPanelWidgetBuilder(AdminPanelElementBuilder):
    def __init__(self, context, widgetType, label):
        super(AdminPanelWidgetBuilder, self).__init__(dict(type=widgetType, label=self._string(label)))
        self._identifier = "widget-{}".format(len(context.widgets) + 1)
        self._handler = None
        context.widgets.append(self)

    def setId(self, identifier):
        self._string(identifier)
        if len(identifier) == 0:
            raise ValueError("OpButton id must not be empty")
        return self._set("id", identifier)

    def _callback(self, callback, args, passValue):
        if callable(callback) is False:
            raise ValueError("OpButton callback must be callable")

        self._description.setdefault("id", self._identifier)
        self._handler = (callback, args, passValue)
        return self


class AdminPanelButtonBuilder(AdminPanelWidgetBuilder):
    def variant(self, value):
        return self._set("variant", self._string(value))

    def color(self, value):
        return self._set("color", self._string(value))

    def disabled(self, value):
        return self._set("disabled", self._boolean(value))

    def onClick(self, callback, *args):
        return self._callback(callback, args, False)


class AdminPanelLabelBuilder(AdminPanelWidgetBuilder):
    def __init__(self, context, widgetType, label):
        super(AdminPanelLabelBuilder, self).__init__(context, widgetType, label)
        self._description["text"] = self._description.pop("label")

    def text(self, value):
        return self._set("text", self._string(value))

    def color(self, value):
        return self._set("color", self._string(value))


class AdminPanelStatBuilder(AdminPanelWidgetBuilder):
    def value(self, value):
        return self._set("value", self._string(value))

    def unit(self, value):
        return self._set("unit", self._string(value))


class AdminPanelSwitchBuilder(AdminPanelWidgetBuilder):
    def defaultValue(self, value):
        return self._set("defaultValue", self._boolean(value))

    def onChange(self, callback, *args):
        return self._callback(callback, args, True)


class AdminPanelInputBuilder(AdminPanelWidgetBuilder):
    def defaultValue(self, value):
        return self._set("defaultValue", self._string(value))

    def placeholder(self, value):
        return self._set("placeholder", self._string(value))

    def inputType(self, value):
        return self._set("inputType", self._string(value))

    def onSubmit(self, callback, *args):
        return self._callback(callback, args, True)


class AdminPanelSelectBuilder(AdminPanelWidgetBuilder):
    def options(self, values):
        options = []
        identifiers = set()

        for value, label in values:
            self._string(value)
            self._string(label)
            if value in identifiers:
                raise ValueError("Duplicate OpButton option: {}".format(value))
            identifiers.add(value)
            options.append(dict(value=value, label=label))

        if len(options) == 0:
            raise ValueError("OpButton options must not be empty")

        return self._set("options", options)

    def defaultValue(self, value):
        return self._set("defaultValue", self._string(value))

    def onChange(self, callback, *args):
        return self._callback(callback, args, True)


class AdminPanelRadioGroupBuilder(AdminPanelSelectBuilder):
    def optionDirection(self, value):
        return self._set("optionDirection", self._choice(value, ("horizontal", "vertical")))

    def disabled(self, value):
        return self._set("disabled", self._boolean(value))


class AdminPanelSliderBuilder(AdminPanelWidgetBuilder):
    def range(self, minimum, maximum, step):
        minimum = self._number(minimum)
        maximum = self._number(maximum)
        step = self._number(step, True)
        interval = self._number(maximum - minimum, True)
        if step > interval:
            raise ValueError("OpButton slider step exceeds its range")

        self._set("min", minimum)
        self._set("max", maximum)
        return self._set("step", step)

    def defaultValue(self, value):
        return self._set("defaultValue", self._number(value))

    def unit(self, value):
        return self._set("unit", self._string(value))

    def disabled(self, value):
        return self._set("disabled", self._boolean(value))

    def onChange(self, callback, *args):
        return self._callback(callback, args, True)


class AdminPanelTextareaBuilder(AdminPanelWidgetBuilder):
    def rows(self, value):
        if type(value) not in (int, long) or value < 1 or value > 2147483647:
            raise ValueError("OpButton rows must be a positive native integer")
        return self._set("rows", value)

    def defaultValue(self, value):
        return self._set("defaultValue", self._string(value))

    def onSubmit(self, callback, *args):
        return self._callback(callback, args, True)


class AdminPanelTableBuilder(AdminPanelWidgetBuilder):
    def columns(self, values):
        return self._set("columns", [dict(key=self._string(key), label=self._string(label)) for key, label in values])

    def rows(self, values):
        return self._set("rows", list(values))


class AdminPanelLogsBuilder(AdminPanelWidgetBuilder):
    def maxLines(self, value):
        if type(value) not in (int, long) or value < 1 or value > 2147483647:
            raise ValueError("OpButton maxLines must be a positive native integer")
        return self._set("maxLines", value)


class AdminPanelLayoutBuilder(AdminPanelElementBuilder):
    def __init__(self, context, direction, depth=0):
        if depth > 32:
            raise ValueError("OpButton layout nesting exceeds 32")

        self._depth = depth
        super(AdminPanelLayoutBuilder, self).__init__(dict(type="layout", direction=direction, children=[]))
        self._context = context

    def gap(self, value):
        return self._set("gap", self._number(value, False, True))

    def padding(self, value):
        return self._set("padding", self._number(value, False, True))

    def align(self, value):
        return self._set("align", self._choice(value, ("start", "center", "end", "stretch")))

    def justify(self, value):
        return self._set("justify", self._choice(value, ("start", "center", "end", "space-between")))

    def wrap(self, value):
        return self._set("wrap", self._boolean(value))

    def density(self, value):
        return self._set("density", self._choice(value, ("compact", "comfortable")))

    def columns(self, value):
        if type(value) not in (int, long) or value < 1 or value > 12:
            raise ValueError("OpButton grid column count must be between 1 and 12")
        return self._set("gridColumns", value)

    def minCellWidth(self, value):
        return self._set("minCellWidth", self._number(value, True, True))

    def title(self, value):
        return self._set("title", self._string(value))

    def _add(self, element):
        self._description["children"].append(element._description)
        return element

    def addVertical(self):
        return self._add(AdminPanelLayoutBuilder(self._context, "vertical", self._depth + 1))

    def addHorizontal(self):
        return self._add(AdminPanelLayoutBuilder(self._context, "horizontal", self._depth + 1))

    def addGrid(self):
        return self._add(AdminPanelLayoutBuilder(self._context, "grid", self._depth + 1))

    def addGroup(self, title):
        return self.addVertical().title(title)

    def addCollapsible(self, title):
        content = AdminPanelLayoutBuilder(self._context, "vertical", self._depth + 2)
        self._description["children"].append(dict(type="collapsible", title=self._string(title), children=[content._description]))
        return content

    def addPadding(self, weight=1):
        self._description["children"].append(dict(type="padding", weight=self._number(weight, False, True)))
        return self

    def addButton(self, label):
        return self._add(AdminPanelButtonBuilder(self._context, "button", label))

    def addLabel(self, label):
        return self._add(AdminPanelLabelBuilder(self._context, "label", label))

    def addStat(self, label):
        return self._add(AdminPanelStatBuilder(self._context, "stat", label))

    def addSwitch(self, label):
        return self._add(AdminPanelSwitchBuilder(self._context, "switch", label))

    def addInput(self, label):
        return self._add(AdminPanelInputBuilder(self._context, "input", label))

    def addSelect(self, label):
        return self._add(AdminPanelSelectBuilder(self._context, "select", label))

    def addTextarea(self, label):
        return self._add(AdminPanelTextareaBuilder(self._context, "textarea", label))

    def addTable(self, label):
        return self._add(AdminPanelTableBuilder(self._context, "table", label))

    def addLogs(self, label):
        return self._add(AdminPanelLogsBuilder(self._context, "logs", label))

    def addRadioGroup(self, label):
        return self._add(AdminPanelRadioGroupBuilder(self._context, "radio", label))

    def addSlider(self, label):
        return self._add(AdminPanelSliderBuilder(self._context, "slider", label))

    def build(self):
        return self._context.build()


class AdminPanelTabBuilder(object):
    def __init__(self, name):
        self._name = AdminPanelElementBuilder._string(name)
        if len(name) == 0:
            raise ValueError("OpButton tab must not be empty")
        self._context = None

    def _layout(self, direction):
        self._context = AdminPanelBuilderContext(self._name)
        layout = AdminPanelLayoutBuilder(self._context, direction)
        self._context.root = layout._description
        return layout

    def vertical(self):
        return self._layout("vertical")

    def horizontal(self):
        return self._layout("horizontal")

    def grid(self):
        return self._layout("grid")

    def build(self):
        if self._context is None:
            raise ValueError("Choose an OpButton root layout before building")
        return self._context.build()


class AdminPanelBuilderContext(object):
    def __init__(self, tab):
        self.tab = tab
        self.root = None
        self.widgets = []

    def build(self):
        from Foundation.Providers.AdminPanelProvider import AdminPanelProvider

        handlers = {}
        identifiers = set()
        for widget in self.widgets:
            identifier = widget._description.get("id")
            if identifier is None:
                continue

            if identifier in identifiers:
                raise ValueError("Duplicate OpButton widget id: {}".format(identifier))
            identifiers.add(identifier)

            if widget._handler is not None:
                handlers[identifier] = widget._handler

        dispatcher = AdminPanelCallbackDispatcher(handlers)
        return AdminPanelProvider.setTab(self.tab, self.root, dispatcher.onAction)


class AdminPanelCallbackDispatcher(object):
    def __init__(self, handlers):
        self._handlers = handlers

    def onAction(self, identifier, value):
        handler = self._handlers.get(identifier)
        if handler is None:
            return

        callback, args, passValue = handler
        if passValue is True:
            callback(value, *args)
        else:
            callback(*args)
