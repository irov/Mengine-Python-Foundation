from Foundation.FixedLayoutCell import FixedLayoutCell


class SafeAreaTopLayoutCell(FixedLayoutCell):
    """
    Reserve the top safe-area inset (notch, Dynamic Island) as a fixed strip.

    The strip is the first cell of a screen's vertical LayoutBox, so content
    starts below the system cutout without knowing about it. getZones() splits
    the strip into left, center and right rectangles: the center covers the
    cutout and stays empty, the sides are free for small controls.

    The center comes from Mengine.getDisplayCutoutViewport() where the platform
    reports the cutout rectangle (Android). iOS publishes only the inset height,
    so there centerRatio approximates the island's share of the width.
    """

    def __init__(self, engine=None, centerRatio=0.5, minimumPixels=0.0):
        super(SafeAreaTopLayoutCell, self).__init__(engine)

        self.centerRatio = min(1.0, max(0.0, float(centerRatio)))
        self.minimumPixels = max(0.0, float(minimumPixels))

    def getRect(self):
        """ (x, y, width, height) of the strip in layout units, or None when detached """
        if self.layout is None:
            return None

        origin, size = self.viewport()

        return origin[0], origin[1], size[0], self.height

    def getCutoutSpan(self, width):
        """ (left, right) of the reported cutout in layout units, or None """
        getter = getattr(self.engine, "getDisplayCutoutViewport", None)

        if getter is None:
            return None

        cutout = getter()

        if cutout is None:
            return None

        resolution = self.engine.getCurrentResolution()
        screenWidth = float(resolution.getWidth())

        if screenWidth <= 0.0:
            return None

        left = max(0.0, float(cutout.begin.x)) * width / screenWidth
        right = min(screenWidth, float(cutout.end.x)) * width / screenWidth

        if right <= left:
            return None

        return left, right

    def getZones(self):
        """ {'left': rect, 'center': rect, 'right': rect}; the center is the cutout """
        strip = self.getRect()

        if strip is None:
            return None

        x, y, width, height = strip

        span = self.getCutoutSpan(width) if height > 0.0 else None

        if span is not None:
            leftWidth, rightEdge = span
        elif height > 0.0:
            center = width * self.centerRatio
            leftWidth = (width - center) / 2.0
            rightEdge = leftWidth + center
        else:
            leftWidth = width / 2.0
            rightEdge = leftWidth
            pass

        return {
            "left": (x, y, leftWidth, height),
            "center": (x + leftWidth, y, rightEdge - leftWidth, height),
            "right": (x + rightEdge, y, width - rightEdge, height),
        }

    def _measure(self):
        pixels = self.getSafeTopPixels()

        if pixels <= 0.0:
            return 0.0

        return self.pixelsToLayout(max(pixels, self.minimumPixels))
    pass
