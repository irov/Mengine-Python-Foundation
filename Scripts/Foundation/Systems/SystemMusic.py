from Foundation.DefaultManager import DefaultManager
from Foundation.MusicManager import MusicManager
from Foundation.System import System


class SystemMusic(System):

    def __init__(self):
        super(SystemMusic, self).__init__()
        self.playList = None       # current list of tracks, or None
        self.playMusic = False
        self.pauseMusic = False
        self.easing = "easyLinear"
        self.fadeTime = 250.0
        self.random = False
        # Per-playlist saved track index (so we resume on the next track when returning)
        self.playListIndex = {}    # id(playlist) -> index
        self.currentIndex = 0
        # Last played track per playlist (used in random mode to avoid immediate repeats)
        self.lastTrack = {}        # id(playlist) -> track

    def _onRun(self):
        self.random = DefaultManager.getDefaultBool("MusicPlayListRandom", False)
        self.addObserver(Notificator.onSceneInit, self.__onSceneInit)
        return True

    def _onStop(self):
        self.stopMusic()

    def __onSceneInit(self, sceneName):
        if MusicManager.hasScenePlayList(sceneName) is True:
            playList = MusicManager.getScenePlayList(sceneName)
        else:
            playList = MusicManager.getDefaultPlayList()

        # No music for this scene -> pause without losing position
        if playList is None:
            if self.playMusic is True and self.pauseMusic is False:
                Mengine.musicPause()
                self.pauseMusic = True
            return False

        if self.playMusic is True:
            if playList is self.playList:
                if self.pauseMusic is True:
                    Mengine.musicResume()
                    self.pauseMusic = False
            else:
                self.__switchPlayList(playList)
            return False

        self.__switchPlayList(playList)
        self.playMusic = True
        return False

    def __switchPlayList(self, playList):
        # Save current playlist position before switching to a different one
        if self.playList is not None:
            self.playListIndex[id(self.playList)] = self.currentIndex

        self.pauseMusic = False
        self.playList = playList

        if self.random is True:
            self.currentIndex = self.__pickRandomIndex(playList)
        else:
            self.currentIndex = self.playListIndex.get(id(playList), 0)
        # Fade-in only on explicit playlist change (not on natural in-playlist transitions)
        self.__playCurrent(fade=True)

    def __pickRandomIndex(self, playList):
        if len(playList) <= 1:
            return 0

        last = self.lastTrack.get(id(playList))
        candidates = [i for i, t in enumerate(playList) if t != last]
        if len(candidates) == 0:
            candidates = list(range(len(playList)))
        return candidates[Mengine.rand(len(candidates))]

    def __playCurrent(self, fade=False):
        playList = self.playList
        if playList is None or len(playList) == 0:
            return

        if self.currentIndex >= len(playList):
            self.currentIndex = 0

        track = playList[self.currentIndex]
        self.lastTrack[id(playList)] = track

        def _onAmplifierMusicEnd(identity):
            if self.playList is not playList:
                return
            if self.playMusic is False or self.pauseMusic is True:
                return

            if self.random is True:
                self.currentIndex = self.__pickRandomIndex(playList)
            else:
                self.currentIndex = (self.currentIndex + 1) % len(playList)
            # Natural in-playlist transition — no fade
            self.__playCurrent(fade=False)

        callbacks = dict(
            onAmplifierMusicEnd=_onAmplifierMusicEnd,
        )

        # loop=False so onAmplifierMusicEnd fires when the track finishes and we can advance
        if fade is True:
            Mengine.musicFadeOut(track, 0.0, False, self.fadeTime, self.easing, callbacks)
        else:
            Mengine.musicPlay(track, 0.0, False, callbacks)

    def stopMusic(self):
        Mengine.musicStop()
        self.playMusic = False
