from Foundation.Entity.BaseEntity import BaseEntity

class Fade(BaseEntity):
    FADE_IDLE = 0
    FADE_IN = 1
    FADE_IN_COMPLETE = 2
    FADE_OUT = 3
    FADE_DISABLE = 4

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        # If Size is None, or (x < 0) or (y < 0) current resolution is used for that dimension.
        Type.addAction(Type, "Size")
        Type.addAction(Type, "State")

    def __init__(self):
        super(Fade, self).__init__()

        self.sprite = None

        self.affector = None
        self.state = Fade.FADE_IDLE

    def _onActivate(self):
        super(Fade, self)._onActivate()
        resolution = Mengine.getContentResolution()

        if not self.Size:
            width = resolution.getWidth()
            height = resolution.getHeight()
            pass
        else:
            width, height = self.Size
            if width < 0:
                width = resolution.getWidth()
                pass
            if height < 0:
                height = resolution.getHeight()
                pass
            pass

        surface = Mengine.createSurface("SurfaceSolidColor")
        surface.setName("FadeSurface_{}".format(id(self)))
        surface.setSolidColor((0.0, 0.0, 0.0, 1.0))
        surface.setSolidSize((width, height))

        sprite = self.createChild("ShapeQuadFixed")
        sprite.setName("FadeSprite_{}".format(id(self)))
        sprite.setSurface(surface)
        sprite.disable()

        self.sprite = sprite

        self.state = Fade.FADE_IDLE
        self.affector = None
        pass

    def _onDeactivate(self):
        super(Fade, self)._onDeactivate()
        self.stopFade()

        Mengine.destroyNode(self.sprite)
        self.sprite = None

        self.state = Fade.FADE_DISABLE
        self.affector = None
        pass

    def fadeIn(self, fadeTo, time, cb, easing):
        self.sprite.enable()

        if self.state == Fade.FADE_IDLE:
            render = self.sprite.getRender()
            render.setLocalAlpha(0.0)
            pass
        elif self.state == Fade.FADE_IN:
            self.sprite.colorStop()
            pass
        elif self.state == Fade.FADE_OUT:
            self.sprite.colorStop()
            pass
        elif self.state == Fade.FADE_IN_COMPLETE:
            cb(True)
            return

        if self.state == Fade.FADE_DISABLE:
            cb(True)
            return

        if self.sprite.isEnable() is False:
            self.sprite.enable()
            pass

        self.state = Fade.FADE_IN

        def __onFadeInComplete(node, isEnd, cb):
            self.state = Fade.FADE_IN_COMPLETE

            self.affector = None

            cb(isEnd is True)
            pass

        self.affector = self.sprite.alphaTo(time, fadeTo, easing, __onFadeInComplete, cb)

        if self.affector is None:
            self.state = Fade.FADE_IDLE
            cb(True)
            pass
        pass

    def fadeOut(self, fadeFrom, time, cb, easing):
        self.sprite.enable()

        if self.state == Fade.FADE_IDLE:
            render = self.sprite.getRender()
            render.setLocalAlpha(fadeFrom)
            pass
        elif self.state == Fade.FADE_IN_COMPLETE:
            render = self.sprite.getRender()
            render.setLocalAlpha(fadeFrom)
            pass
        elif self.state == Fade.FADE_IN:
            self.sprite.colorStop()
            pass
        elif self.state == Fade.FADE_OUT:
            self.sprite.colorStop()
            pass

        if self.state == Fade.FADE_DISABLE:
            cb(True)
            return

        if self.sprite.isEnable() is False:
            self.sprite.enable()
            pass

        self.state = Fade.FADE_OUT

        def __onFadeOutComplete(node, isEnd, cb):
            node.disable()

            self.state = Fade.FADE_IDLE

            self.affector = None

            cb(isEnd is True)
            pass

        self.affector = self.sprite.alphaTo(time, 0, easing, __onFadeOutComplete, cb)

        if self.affector is None:
            self.state = Fade.FADE_IDLE
            cb(True)
            pass
        pass

    def stopFade(self):
        self.sprite.colorStop()

        if self.state == Fade.FADE_DISABLE:
            return

        self.sprite.disable()

        self.state = Fade.FADE_IDLE
        self.affector = None
        pass
    pass