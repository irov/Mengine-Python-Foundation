class LayoutBox(object):
    def __init__(self, sizer):
        self.sizer = sizer
        self.component = None
        pass

    class ElementFixed(object):
        def __init__(self, let_type, getter, setter):
            self.let_type = let_type
            self.getter = getter
            self.setter = setter
            pass

    class ElementPadding(object):
        def __init__(self, weight):
            self.weight = weight

        def getWeight(self):
            return self.weight

    class Component(object):
        def __init__(self, x, y, sizer, layout, parent):
            self.x = x
            self.y = y
            self.sizer = sizer
            self.layout = layout
            self.parent = parent

        def getOffsetX(self):
            if self.parent is None:
                return self.x
            parentOffsetX = self.parent.getOffsetX()
            offsetX = parentOffsetX + self.x
            return offsetX

        def getOffsetY(self):
            if self.parent is None:
                return self.y
            parentOffsetY = self.parent.getOffsetY()
            offsetY = parentOffsetY + self.y
            return offsetY

    class BuilderElement(object):
        def __init__(self):
            self.elements = []
            pass

        def addFixed(self, _getter, _setter):
            element = LayoutBox.ElementFixed(Mengine.LET_FIXED, _getter, _setter)
            self.elements.append(element)
            return self

        def addPadding(self, weight):
            element = LayoutBox.ElementPadding(weight)
            self.elements.append(element)
            return self

        def addLayoutVertical(self, width):
            builder = LayoutBox.BuilderSubVertical(width)
            self.elements.append(builder)
            return builder

        def addLayoutHorizontal(self, height):
            builder = LayoutBox.BuilderSubHorizontal(height)
            self.elements.append(builder)
            return builder

        def buildSubHorizontalComponent(self, height, parent, elements):
            def __horizontal():
                w, h = parent.sizer()
                return w

            layout = Mengine.createLayout(__horizontal)

            def __sizer():
                w, h = parent.sizer()
                return w, height

            component = LayoutBox.Component(parent.x, parent.y, __sizer, layout, parent)

            for element in elements:
                def __process(element):
                    if isinstance(element, LayoutBox.BuilderSubVertical):
                        width = element.width

                        self.buildSubVerticalComponent(width, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.ElementFixed):
                        def __setter(offset, size):
                            offsetX = parent.getOffsetX()
                            offsetY = parent.getOffsetY()
                            element.setter((offsetX + offset, offsetY), (size, height))
                            pass

                        layout.addElement(element.let_type, element.getter, __setter)
                    elif isinstance(element, LayoutBox.ElementPadding):
                        layout.addElement(Mengine.LET_PAD, element.getWeight, None)
                        pass
                __process(element)

            def __getter():
                return height

            def __setter(offset, size):
                offsetX = parent.getOffsetX()
                offsetY = parent.getOffsetY()
                component.x = offsetX
                component.y = offsetY + offset
                pass

            parent.layout.addSubLayout(layout, Mengine.LET_FIXED, __getter, __setter)

            return component

        def buildSubVerticalComponent(self, width, parent, elements):
            def __vertical():
                w, h = parent.sizer()
                return h

            layout = Mengine.createLayout(__vertical)

            def __sizer():
                w, h = parent.sizer()
                return width, h

            component = LayoutBox.Component(parent.x, parent.y, __sizer, layout, parent)

            for element in elements:
                def __process(element):
                    if isinstance(element, LayoutBox.BuilderSubHorizontal):
                        height = element.height

                        self.buildSubHorizontalComponent(height, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.ElementFixed):
                        def __setter(offset, size):
                            offsetX = parent.getOffsetX()
                            offsetY = parent.getOffsetY()
                            element.setter((offsetX, offsetY + offset), (width, size))
                            pass

                        layout.addElement(element.let_type, element.getter, __setter)
                    elif isinstance(element, LayoutBox.ElementPadding):
                        layout.addElement(Mengine.LET_PAD, element.getWeight, None)
                        pass
                __process(element)

            def __getter():
                return width

            def __setter(offset, size):
                offsetX = parent.getOffsetX()
                offsetY = parent.getOffsetY()
                component.x = offsetX + offset
                component.y = offsetY
                pass

            parent.layout.addSubLayout(layout, Mengine.LET_FIXED, __getter, __setter)

            return component

    class BuilderSubVertical(BuilderElement):
        def __init__(self, width):
            super(LayoutBox.BuilderSubVertical, self).__init__()
            self.width = width
            pass

        def addFixedObject(self, ob):
            def __getter():
                w, h = ob.getLayoutSize()
                return h
            def __setter(offset, size):
                ob.setLayoutOffset(offset)
                ob.setLayoutSize(size)
            self.addFixed(__getter, __setter)
            return self

    class BuilderSubHorizontal(BuilderElement):
        def __init__(self, height):
            super(LayoutBox.BuilderSubHorizontal, self).__init__()
            self.height = height
            pass

        def addFixedObject(self, ob):
            def __getter():
                w, h = ob.getLayoutSize()
                return w
            def __setter(offset, size):
                ob.setLayoutOffset(offset)
                ob.setLayoutSize(size)
            self.addFixed(__getter, __setter)
            return self

    class BuilderVertical(BuilderSubVertical):
        def __init__(self, box):
            super(LayoutBox.BuilderVertical, self).__init__(None)
            self.box = box
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            def __vertical():
                w, h = self.box.sizer()
                return h

            layout = Mengine.createLayout(__vertical)

            component = LayoutBox.Component(0, 0, self.box.sizer, layout, None)

            self.box.component = component

            for element in self.elements:
                def __process(element):
                    if isinstance(element, LayoutBox.BuilderSubHorizontal):
                        height = element.height

                        self.buildSubHorizontalComponent(height, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.BuilderSubVertical):
                        width = element.width

                        self.buildSubVerticalComponent(width, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.ElementFixed):
                        def __setter(offset, size):
                            w, h = self.box.sizer()
                            offsetX = component.getOffsetX()
                            offsetY = component.getOffsetY()
                            element.setter((offsetX, offsetY + offset), (w, size))

                        layout.addElement(element.let_type, element.getter, __setter)
                    elif isinstance(element, LayoutBox.ElementPadding):
                        layout.addElement(Mengine.LET_PAD, element.getWeight, None)
                        pass

                __process(element)
            pass

    class BuilderHorizontal(BuilderSubHorizontal):
        def __init__(self, box):
            super(LayoutBox.BuilderHorizontal, self).__init__(None)
            self.box = box
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            def __horizontal():
                w, h = self.box.sizer()
                return w

            layout = Mengine.createLayout(__horizontal)

            component = LayoutBox.Component(0, 0, self.box.sizer, layout, None)

            self.box.component = component

            for element in self.elements:
                def __process(element):
                    if isinstance(element, LayoutBox.BuilderSubVertical):
                        width = element.width

                        self.buildSubVerticalComponent(width, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.BuilderSubHorizontal):
                        height = element.height

                        self.buildSubHorizontalComponent(height, component, element.elements)
                        pass
                    elif isinstance(element, LayoutBox.ElementFixed):
                        def __setter(offset, size):
                            w, h = self.box.sizer()
                            offsetX = component.getOffsetX()
                            offsetY = component.getOffsetY()
                            element.setter((offsetX + offset, offsetY), (size, h))

                        layout.addElement(element.let_type, element.getter, __setter)
                    elif isinstance(element, LayoutBox.ElementPadding):
                        layout.addElement(Mengine.LET_PAD, element.getWeight, None)
                        pass
                    pass

                __process(element)
            pass
        pass