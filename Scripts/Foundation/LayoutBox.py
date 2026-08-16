class LayoutBox(object):
    def __init__(self, sizer):
        self.sizer = sizer
        self.component = None
        pass

    def getSize(self):
        w, h = self.sizer()
        return w, h

    def finalize(self):
        if self.component is not None:
            Mengine.destroyLayoutBox(self.component)
            self.component = None
            pass

        self.sizer = None
        pass

    class ElementFixed(object):
        def __init__(self, getter, setter):
            self.getter = getter
            self.setter = setter
            pass

    class ElementPadding(object):
        def __init__(self, weight):
            self.weight = weight

        def getWeight(self):
            return self.weight
        pass

    class BuilderElement(object):
        def __init__(self):
            self.elements = []
            pass

        def addFixed(self, _getter, _setter=None):
            element = LayoutBox.ElementFixed(_getter, _setter)
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

        def buildElements(self, container, elements, box):
            for element in elements:
                if isinstance(element, LayoutBox.BuilderSubVertical):
                    sub = container.addBox(Mengine.ELBD_VERTICAL, element.width)

                    self.buildElements(sub, element.elements, box)
                    pass
                elif isinstance(element, LayoutBox.BuilderSubHorizontal):
                    sub = container.addBox(Mengine.ELBD_HORIZONTAL, element.height)

                    self.buildElements(sub, element.elements, box)
                    pass
                elif isinstance(element, LayoutBox.ElementFixed):
                    setter = None

                    if element.setter is not None:
                        def __setter(offset, size, element=element):
                            element.setter(box, (offset.x, offset.y), (size.x, size.y))
                            pass

                        setter = __setter
                        pass

                    container.addFixed(element.getter, setter)
                    pass
                elif isinstance(element, LayoutBox.ElementPadding):
                    container.addPadding(element.getWeight())
                    pass
                pass
            pass

        def build(self, box, direction):
            if box.component is not None:
                Mengine.destroyLayoutBox(box.component)
                box.component = None
                pass

            layout = Mengine.createLayoutBox(box.sizer)
            root = layout.createRoot(direction)

            self.buildElements(root, self.elements, box)

            box.component = layout

            layout.flush()
            pass

    class BuilderSubVertical(BuilderElement):
        def __init__(self, width):
            super(LayoutBox.BuilderSubVertical, self).__init__()
            self.width = width
            pass

        def addFixedObject(self, ob):
            def __getter():
                w, h = ob.getLayoutSize()
                return h

            def __setter(box, offset, size):
                ob.setLayoutOffset(box, offset, size)

            self.addFixed(__getter, __setter)
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            pass

    class BuilderSubHorizontal(BuilderElement):
        def __init__(self, height):
            super(LayoutBox.BuilderSubHorizontal, self).__init__()
            self.height = height
            pass

        def addFixedObject(self, ob):
            def __getter():
                w, h = ob.getLayoutSize()
                return w

            def __setter(box, offset, size):
                ob.setLayoutOffset(box, offset, size)

            self.addFixed(__getter, __setter)
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            pass

    class BuilderVertical(BuilderSubVertical):
        def __init__(self, box):
            super(LayoutBox.BuilderVertical, self).__init__(None)
            self.box = box
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            self.build(self.box, Mengine.ELBD_VERTICAL)
            pass

    class BuilderHorizontal(BuilderSubHorizontal):
        def __init__(self, box):
            super(LayoutBox.BuilderHorizontal, self).__init__(None)
            self.box = box
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_t):
            self.build(self.box, Mengine.ELBD_HORIZONTAL)
            pass
