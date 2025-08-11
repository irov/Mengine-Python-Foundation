from Foundation.System import System


class SystemDevToDebug(System):

    """ https://wonderland-games.atlassian.net/wiki/spaces/FRW2/pages/1853849603/DevToDebug """

    def __init__(self):
        super(SystemDevToDebug, self).__init__()
        self.coin = 0

    def _onRun(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return True

        # self.createTestTab()
        # self.createSpamTabs()
        # self.createGroupedButtons()
        # self.createTextInputTab()
        # self.createDebugExamples()
        # self.createCheckbox()
        # self.createRadioButtons()
        # self.createSelector()

        return True

    def createTextInputTab(self):
        """ Here we will test CommandLine Widget """

        tab = Mengine.addDevToDebugTab("TextInputTab")

        # this dict storage data from CommandLine, that will be output in the text widget
        data = {"output": "no data", "version": 0}

        # 1. create widget with inputted from CommandLine text

        def get_output():
            return "Output [{}]: '{}'".format(data["version"], data["output"])

        widget1 = Mengine.createDevToDebugWidgetText("command_line_output")
        widget1.setText(get_output)

        # 2. create CommandLine widget

        def get_input(text):
            print("receive new text from CommandLine: '{}'".format(text))
            data["output"] = text
            data["version"] += 1

        widget2 = Mengine.createDevToDebugWidgetCommandLine("command_line_input")

        widget2.setTitle("Command Line Title")
        widget2.setPlaceholder("input something good")
        widget2.setCommandEvent(get_input)

        tab.addWidget(widget1)
        tab.addWidget(widget2)

    def createSpamTabs(self):
        """ Here we will create 20 tabs with 50 widgets inside and see what would happen """
        for i in range(20):
            tab = Mengine.addDevToDebugTab("SpamTab_%s" % i)
            for j in range(50):
                widget_text = Mengine.createDevToDebugWidgetText("test_%s" % j)
                widget_text.setText("test const text %s %s %s" % (i, j, i * j))
                tab.addWidget(widget_text)

    def createGroupedButtons(self):
        """ Here we will create text and button widgets """

        tab = Mengine.addDevToDebugTab("TestTab2")

        def _cb(text):
            print(text)

        for i in range(50):
            name = "test_%s" % i

            if i % 10 == 0:
                widget = Mengine.createDevToDebugWidgetText(name)
                widget.setText("title_" + name)
            else:
                widget = Mengine.createDevToDebugWidgetButton(name)
                widget.setTitle("title_" + name)
                widget.setClickEvent(_cb, "cb " + name)

            tab.addWidget(widget)

    def createTestTab(self):
        """ Here we will create 1 tab and some widgets """

        tab = Mengine.addDevToDebugTab("TestTab")  # create tab

        widget_text1 = Mengine.createDevToDebugWidgetText("test_1")
        widget_text1.setText("test const text")
        widget_text1.setColor((0.76, 0.2, 0.2))
        tab.addWidget(widget_text1)

        widget_text2 = Mengine.createDevToDebugWidgetText("test_2")

        def __get_coin():
            return "Coins: {}".format(self.coin)

        widget_text2.setText(__get_coin)

        tab.addWidget(widget_text2)

        widget_btn = Mengine.createDevToDebugWidgetButton("test_3")
        widget_btn.setTitle("test button widget")

        def __add_coins():
            self.coin += 1

        widget_btn.setClickEvent(__add_coins)

        tab.addWidget(widget_btn)

        widget_line = Mengine.createDevToDebugWidgetButton("test_4")
        widget_line.setTitle("Set coins")

        def __set_coins(text):
            try:
                value = int(text)
                if value < 0:
                    raise ValueError("value must be positive")
            except ValueError as e:
                Trace.msg_dev("wrong input {}: {}".format(text, e))
                return
            self.coins = value

        widget_line.setClickEvent(__set_coins)

        tab.addWidget(widget_line)

    def createDebugExamples(self):
        tab = Mengine.getDevToDebugTab("Debug") or Mengine.addDevToDebugTab("Debug")
        widgets = []

        def _follower(text):
            x, y, z = [float(X) for X in text.split(" ")]

            def _upd(val):
                Trace.msg("[DevToDebug] follow [{}] {}".format(Mengine.getTimeMs(), val))
                if val >= z:
                    Trace.msg("[DevToDebug] destroyValueFollower")
                    return True

            follower = Mengine.createValueFollowerLinear(x, y, _upd)
            Trace.msg("[DevToDebug] createValueFollowerLinear (start={}, speed={}, stop={})".format(x, y, z))
            follower.setFollow(z)

        w_follower = Mengine.createDevToDebugWidgetCommandLine("follower")
        w_follower.setTitle("Try linear value follower")
        w_follower.setPlaceholder("Syntax: <start> <speed> <stop>")
        w_follower.setCommandEvent(_follower)
        widgets.append(w_follower)

        def _affector(text):
            z = float(text)
            d = {"total": 0}

            def _upd(dt, d):
                d["total"] += dt
                Trace.msg("[DevToDebug] ({}) affect [{}] dt={}, total={}".format(
                    affector_id, Mengine.getTimeMs(), dt, d["total"]))
                if d["total"] >= z:
                    Trace.msg("[DevToDebug] removeAffector {}".format(affector_id))
                    return True
                return False

            affector = Mengine.addAffector(_upd, d)
            if affector is None:
                Trace.msg_err("[DevToDebu] addAffector initialize failed")
            else:
                Trace.msg("[DevToDebug] addAffector (stop={}) {}".format(z, affector))

        w_affector = Mengine.createDevToDebugWidgetCommandLine("affector")
        w_affector.setTitle("Try affector")
        w_affector.setPlaceholder("Syntax: <stop>")
        w_affector.setCommandEvent(_affector)
        widgets.append(w_affector)

        for widget in widgets:
            if tab.findWidget(widget.getWidgetId()) is not None:
                continue
            tab.addWidget(widget)

    def createCheckbox(self):
        semaphore = Semaphore(False, "CheckboxState")
        tab = Mengine.getDevToDebugTab("Debug") or Mengine.addDevToDebugTab("Debug")

        def _cb(state):
            Trace.msg("checkbox update from {} to {}".format(semaphore.getValue(), state))
            semaphore.setValue(state)

        w_checkbox = Mengine.createDevToDebugWidgetCheckbox("test_checkbox")
        w_checkbox.setTitle("Test checkbox")
        w_checkbox.setValue(semaphore.getValue())
        w_checkbox.setChangeEvent(_cb)

        tab.addWidget(w_checkbox)

    def createRadioButtons(self):
        states = [
            "yes",
            "not sure",
            "no",
        ]
        holder = Holder(states[0])

        tab = Mengine.getDevToDebugTab("Debug") or Mengine.addDevToDebugTab("Debug")

        def _cb(value):
            Trace.msg("radiobutton update from {} to {}".format(holder.get(), value))
            holder.set(value)

        w_radio = Mengine.createDevToDebugWidgetRadioButton("test_radiobutton")
        w_radio.setTitle("[Radiobutton] Do you like cats?")
        for i, state in enumerate(states):
            w_radio.addState(str(i), state)
        w_radio.setChangeEvent(_cb)

        tab.addWidget(w_radio)

    def createSelector(self):
        states = [
            "yes",
            "not sure",
            "no",
        ]
        holder = Holder(states[0])

        tab = Mengine.getDevToDebugTab("Debug") or Mengine.addDevToDebugTab("Debug")

        def _cb(value):
            Trace.msg("selector update from {} to {}".format(holder.get(), value))
            holder.set(value)

        w_selector = Mengine.createDevToDebugWidgetSelector("test_selector")
        w_selector.setTitle("[Selector] Do you like cats?")
        for i, state in enumerate(states):
            w_selector.addState(str(i), state)
        w_selector.setChangeEvent(_cb)

        tab.addWidget(w_selector)

    def _onStop(self):
        return True
