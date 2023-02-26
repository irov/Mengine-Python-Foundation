from Foundation.Entity.BaseEntity import BaseEntity

from Notification import Notification

class Video(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "VideoResourceName")
        Type.addAction(Type, "Play", Update=Video._updatePlay)
        pass

    def __init__(self):
        super(Video, self).__init__()
        self.video = None
        self.isPlay = False
        pass

    def _onInitialize(self, obj):
        super(Video, self)._onInitialize(obj)
        self.video = self.createChild("Video")

        name = self.getName()
        self.video.setName(name)

        self.video.setResourceVideo(self.VideoResourceName)
        self.video.setEventListener(onVideoEnd=self._onVideoEnd)
        self.video.enable()
        pass

    def _onFinalize(self):
        super(Video, self)._onFinalize()

        Menge.destroyNode(self.video)
        self.video = None
        pass

    def _updatePlay(self, value):
        if value is True:
            self.video.play()
            self.isPlay = True
            pass

        if value is False and self.isPlay == True:
            self.video.stop()
            pass
        pass

    def _onVideoEnd(self, video, id, isEnd):
        Notification.notify(Notificator.onVideoEnd, self.object)
        return
    pass