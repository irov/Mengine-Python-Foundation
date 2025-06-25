class LayoutBox(object):
    class Component(object):
        def __init__(self, x, y, sizer, layout, parent):
            self.x = x
            self.y = y
            self.sizer = sizer
            self.layout = layout
            self.parent = parent

        def getOffsetX(self):
            if self.parent is not None:
                return self.x
            offsetX = self.x + self.parent.getOffsetX()
            return offsetX

        def getOffsetY(self):
            if self.parent is not None:
                return self.y
            offsetY = self.y + self.parent.getOffsetY()
            return offsetY

    def __init__(self, sizer):
        self.sizer = sizer
        self.components = []
        pass

    class BuilderBase(object):
        def __init__(self):
            self.elements = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            #Empty
            pass

    class BuilderElement(BuilderBase):
        def addFixed(self, name, _getter, _setter):
            element = (name, Mengine.LET_FIXED, _getter, _setter)
            self.elements.append(element)
            return self

        def addPad(self, name, _getter, _setter):
            element = (name, Mengine.LET_PAD, _getter, _setter)
            self.elements.append(element)
            return self

    class BuilderSubHorizontal(BuilderElement):
        def __init__(self, height):
            super(LayoutBox.BuilderSubHorizontal, self).__init__()
            self.height = height

        def addLayoutVertical(self, width):
            builder = LayoutBox.BuilderSubVertical(width)
            self.elements.append(builder)
            return builder

    class BuilderSubVertical(BuilderElement):
        def __init__(self, width):
            super(LayoutBox.BuilderSubVertical, self).__init__()
            self.width = width

        def addLayoutHorizontal(self, width):
            builder = LayoutBox.BuilderSubHorizontal(width)
            self.elements.append(builder)
            return builder

    class BuilderVertical(BuilderElement):
        def __init__(self, box):
            super(LayoutBox.BuilderVertical, self).__init__()
            self.box = box

        def addLayoutHorizontal(self, height):
            builder = LayoutBox.BuilderSubHorizontal(height)
            self.elements.append(builder)
            return builder

        def __buildSubHorizontalComponent(self, height, component, elements):
            for element in self.elements:
                if isinstance(element, LayoutBox.BuilderSubVertical):
                    width = element.width

                    def __vertical():
                        w, h = self.component.sizer()
                        return h

                    sub_vertical_layout = Mengine.createLayout(__vertical)

                    self.__buildSubVerticalComponent(width, component, element.elements)
                    pass
                elif isinstance(element, LayoutBox.BuilderElement):
                    name, let_type, getter, setter = element

                    def __getter():
                        w, h = getter()
                        return h

                    def __setter(offset, size):
                        offsetX = component.getOffsetX()
                        offsetY = component.getOffsetY()
                        setter((offsetX, offsetY + offset), (size, height))

                    component.layout.addElement(name, let_type, __getter, __setter)
                    pass

        def __buildSubVerticalComponent(self, width, component, elements):
            for element in self.elements:
                if isinstance(element, LayoutBox.BuilderSubHorizontal):
                    height = element.height

                    def __horizontal():
                        w, h = self.component.sizer()
                        return w

                    sub_horizontal_layout = Mengine.createLayout(__horizontal)

                    self.__buildSubHorizontalComponent(height, component, element.elements)
                    pass
                elif isinstance(element, LayoutBox.BuilderElement):
                    name, let_type, getter, setter = element

                    def __getter():
                        w, h = getter()
                        return w

                    def __setter(offset, size):
                        offsetX = component.getOffsetX()
                        offsetY = component.getOffsetY()
                        setter((offsetX + offset, offsetY), (width, size))

                    component.layout.addElement(name, let_type, __getter, __setter)
                    pass

        def __build(self):
            def __vertical():
                w, h = self.box.sizer()
                return h

            layout = Mengine.createLayout(__vertical)

            component = LayoutBox.Component(0, 0, layout, None)

            for element in self.elements:
                if isinstance(element, LayoutBox.BuilderSubHorizontal):
                    height = element.height

                    def __horizontal():
                        w, h = self.box.sizer()

                        return w

                    sub_horizontal_layout = Mengine.createLayout(__horizontal)

                    for sub_element in element.elements:
                        if isinstance(sub_element, LayoutBox.BuilderSubVertical):
                            pass
                        elif isinstance(sub_element, LayoutBox.BuilderElement):
                            name, let_type, getter, setter = sub_element

                            def __getter():
                                w, h = getter()
                                return w

                            def __setter(offset, size):
                                w, h = getter()
                                setter(offset, (size, h))

                            sub_horizontal_layout.addElement(name, let_type, __getter, __setter)
                        pass

                    def __getter():
                        return height

                    def __setter(offset, size):
                        #ToDo
                        pass

                    layout.addElement(None, Mengine.LET_FIXED, __getter, __setter)
                    pass
                elif isinstance(element, LayoutBox.BuilderElement):
                    name, let_type, getter, setter = element

                    def __getter():
                        w, h = getter()
                        return w

                    def __setter(offset, size):
                        w, h = getter()
                        setter(offset, (size, h))

                    layout.addElement(name, let_type, __getter, __setter)
                    pass
            pass

        def __exit__(self, exc_type, exc_val, exc_t):
            pass