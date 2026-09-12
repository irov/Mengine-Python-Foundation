class FixedLayoutCell(object):
    """
    Fixed-height cell of a vertical LayoutBox whose height is polled every frame.

    attachTo() registers the cell with box.addFixed() and owns the polling
    affector. Reattaching to another layout transfers ownership, so finalizing
    the previous screen cannot collapse the cell of the new one. Subclasses
    implement _measure() and return the wanted height in layout units.
    """

    def __init__(self, engine=None):
        self.engine = engine if engine is not None else Mengine
        self.height = 0.0
        self.layout = None
        self.viewport = None
        self.onResize = None
        self.affector = None

    def attachTo(self, layout, box, viewport, onResize=None):
        """ viewport() returns ((originX, originY), (width, height)) in layout units """
        self.layout = layout
        self.viewport = viewport
        self.onResize = onResize

        self._onAttach()

        box.addFixed(lambda: self.height if self.layout is layout else 0.0, None)

        if self.affector is None:
            self.affector = self.engine.addAffector(self._update)
            pass

        self._update(0.0)
        pass

    def detachFrom(self, layout):
        if self.layout is not layout:
            return

        self._onDetach()

        if self.affector is not None:
            self.engine.removeAffector(self.affector)
            self.affector = None
            pass

        self.layout = None
        self.viewport = None
        self.onResize = None
        self.height = 0.0
        pass

    def finalize(self):
        if self.layout is not None:
            self.detachFrom(self.layout)
            pass
        pass

    def getLayoutSize(self):
        origin, size = self.viewport()
        return size

    def getScreenHeight(self):
        resolution = self.engine.getCurrentResolution()
        return float(resolution.getHeight())

    def getSafeTopPixels(self):
        safeArea = self.engine.getSafeAreaViewport()
        return max(0.0, float(safeArea.begin.y))

    def getSafeBottomPixels(self):
        safeArea = self.engine.getSafeAreaViewport()
        end = float(safeArea.end.y)

        if end <= 0.0:
            return 0.0

        return max(0.0, self.getScreenHeight() - end)

    def pixelsToLayout(self, pixels):
        """ Convert screen pixels to layout units, never taking the whole viewport """
        screenHeight = self.getScreenHeight()
        size = self.getLayoutSize()

        if pixels <= 0.0 or screenHeight <= 0.0 or size[1] <= 0.0:
            return 0.0

        return min(pixels * size[1] / screenHeight, max(0.0, size[1] - 1.0))

    def _onAttach(self):
        pass

    def _onDetach(self):
        pass

    def _measure(self):
        return 0.0

    def _update(self, delta):
        if self.layout is None:
            return False

        height = self._measure()

        if height != self.height:
            self.height = height
            self.layout.flush()

            if self.onResize is not None:
                self.onResize()
                pass
            pass

        return False
    pass
