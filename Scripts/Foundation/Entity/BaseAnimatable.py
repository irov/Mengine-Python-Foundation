from Foundation.Entity.BaseEntity import BaseEntity

class BaseAnimatable(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction("PlayOnActivate")
        Type.addAction("LastFrameOnPlay")
        Type.addAction("Play", Activate=True, Update=BaseAnimatable.__updatePlay)
        Type.addAction("Pause", Activate=True, Update=BaseAnimatable.__updatePause)
        Type.addAction("Loop", Update=BaseAnimatable.__updateLoop)
        Type.addAction("StartTiming")
        Type.addAction("LastFrame", Activate=True, Update=BaseAnimatable.__updateLastFrame)
        Type.addActionActivate("SpeedFactor", Update=BaseAnimatable.__updateSpeedFactor)
        pass

    def __init__(self):
        super(BaseAnimatable, self).__init__()

        self.playId = 0
        pass

    def getAnimatable(self):
        return None

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None

        animation = animatable.getAnimation()

        return animation

    def __updatePlay(self, value):
        if value is True:
            self.play()
        else:
            self.stop()
            pass
        pass

    def __updatePause(self, value):
        if value is True:
            self.pause()
        else:
            self.resume()
            pass
        pass

    def __updateSpeedFactor(self, value):
        animatable = self.getAnimation()

        animatable.setAnimationSpeedFactor(value)
        pass

    def __updateLastFrame(self, value):
        if self.StartTiming is None:
            animatable = self.getAnimation()

            if value is True:
                result = animatable.setLastFrame()
            elif value is False:
                result = animatable.setFirstFrame()
                pass
            pass
        pass

    def play(self):
        self._onPlay()

        animatable = self.getAnimation()

        self.playId = animatable.play()

        if self.playId == 0:
            Trace.log("Entity", 0, "BaseAnimatable.play: %s invalid start play" % (animatable))

            self.end()
            return
            pass
        pass

    def _onPlay(self):
        pass

    def getPlayId(self):
        return self.playId
        pass

    def validPlayId(self, id):
        return self.playId == id
        pass

    def stop(self):
        if self.playId == 0:
            return
            pass

        animatable = self.getAnimation()
        animatable.stop()

        self._onStop()
        self.playId = 0

        if self.object is not None:
            if self.LastFrameOnPlay is True:
                self.object.setLastFrame(True)
                pass

            self.object.onAnimatableEnd(self.object, True)
            pass
        pass

    def _onStop(self):
        pass

    def pause(self):
        if self.playId == 0:
            return
            pass

        animatable = self.getAnimation()
        animatable.pause()

        self._onPause()
        pass

    def _onPause(self):
        pass

    def resume(self):
        if self.playId == 0:
            return
            pass

        animatable = self.getAnimation()
        animatable.resume()

        self._onResume()
        pass

    def _onResume(self):
        pass

    def end(self):
        if self.playId == 0:
            return
            pass

        self.playId = 0
        self._onEnd()

        if self.object is not None:
            if self.LastFrameOnPlay is True:
                self.object.setLastFrame(True)
                pass

            self.object.onAnimatableEnd(self.object, False)
            pass
        pass

    def _onEnd(self):
        pass

    def interrupt(self):
        animatable = self.getAnimation()

        successful = animatable.interrupt()

        return successful
        pass

    def isInterrupt(self):
        animatable = self.getAnimation()

        interrupt = animatable.isInterrupt()

        return interrupt
        pass

    def __updateLoop(self, value):
        animatable = self.getAnimation()

        animatable.setLoop(value)
        pass

    def _onActivate(self):
        super(BaseAnimatable, self)._onActivate()

        if self.PlayOnActivate is True and not self.Loop:
            self.object.setPlay(True)
            pass
        pass

    def _onDeactivate(self):
        super(BaseAnimatable, self)._onDeactivate()

        self.stop()
        pass

    def setPlayCount(self, value):
        animatable = self.getAnimation()
        animatable.setPlayCount(value)
        pass

    def getPlayCount(self):
        animatable = self.getAnimation()
        value = animatable.getPlayCount()
        return value
        pass

    def getPlayIterator(self):
        animatable = self.getAnimation()
        value = animatable.getPlayIterator()
        return value
        pass

    def setFirstFrame(self):
        animatable = self.getAnimation()

        animatable.setFirstFrame()
        pass

    def setLastFrame(self):
        animatable = self.getAnimation()

        animatable.setLastFrame()
        pass

    def setTiming(self, timing):
        animatable = self.getAnimation()

        animatable.setTime(timing)
        pass

    def getTiming(self):
        animatable = self.getAnimation()

        return animatable.getTime()
        pass

    def setInterval(self, begin, end):
        animatable = self.getAnimation()

        animatable.setInterval(begin, end)
        pass
    pass