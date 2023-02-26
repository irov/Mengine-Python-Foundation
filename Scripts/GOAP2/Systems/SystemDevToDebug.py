from GOAP2.System import System

class SystemDevToDebug(System):

    def __init__(self):
        super(SystemDevToDebug, self).__init__()
        self.coin = 0

    def _onRun(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return True

        # self.createTestTab()
        # self.createSpamTabs()
        # self.createGroupedButtons()
        # self.createTextInputTab()

        return True

    def createTextInputTab(self):
        """ Here we will test CommandLine Widget """

        tab = Menge.addDevToDebugTab("TextInputTab")

        # this dict storage data from CommandLine, that will be output in the text widget
        data = {"output": "no data", "version": 0}

        # 1. create widget with inputted from CommandLine text

        def get_output():
            return "Output [{}]: '{}'".format(data["version"], data["output"])

        widget1 = Menge.createDevToDebugWidgetText("command_line_output")
        widget1.setText(get_output)

        # 2. create CommandLine widget

        def get_input(text):
            print
            "receive new text from CommandLine: '{}'".format(text)
            data["output"] = text
            data["version"] += 1

        widget2 = Menge.createDevToDebugWidgetCommandLine("command_line_input")

        widget2.setTitle("Command Line Title")
        widget2.setPlaceholder("input something good")
        widget2.setCommandEvent(get_input)

        tab.addWidget(widget1)
        tab.addWidget(widget2)

    def createSpamTabs(self):
        """ Here we will create 20 tabs with 50 widgets inside and see what would happen """
        for i in range(20):
            tab = Menge.addDevToDebugTab("SpamTab_%s" % i)
            for j in range(50):
                widget_text = Menge.createDevToDebugWidgetText("test_%s" % j)
                widget_text.setText("test const text %s %s %s" % (i, j, i * j))
                tab.addWidget(widget_text)

    def createGroupedButtons(self):
        """ Here we will create text and button widgets """

        tab = Menge.addDevToDebugTab("TestTab2")

        def _cb(text):
            print(text)

        for i in range(50):
            name = "test_%s" % i

            if i % 10 == 0:
                widget = Menge.createDevToDebugWidgetText(name)
                widget.setText("title_" + name)
            else:
                widget = Menge.createDevToDebugWidgetButton(name)
                widget.setTitle("title_" + name)
                widget.setClickEvent(_cb, "cb " + name)

            tab.addWidget(widget)

    def createTestTab(self):
        """ Here we will create 1 tab and some widgets """

        tab = Menge.addDevToDebugTab("TestTab")  # create tab

        widget_text1 = Menge.createDevToDebugWidgetText("test_1")
        widget_text1.setText("test const text")
        widget_text1.setColor((0.76, 0.2, 0.2))
        tab.addWidget(widget_text1)

        widget_text2 = Menge.createDevToDebugWidgetText("test_2")

        def __get_coin():
            # print("__get_coin {}".format(self.coin))
            return "Coin: {}".format(self.coin)

        widget_text2.setText(__get_coin)

        tab.addWidget(widget_text2)

        widget_btn = Menge.createDevToDebugWidgetButton("test_3")
        widget_btn.setTitle("test button widget")

        def __add_coins():
            self.coin += 1
            print("cb __add_coins works")

        widget_btn.setClickEvent(__add_coins)

        tab.addWidget(widget_btn)

    def _onStop(self):
        return True  # clean