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
            elif self.__adoptPlayListIfSameTrack(playList) is True:
                # Same currently-playing track is present in the new playlist:
                # keep playing without restart, just rebind to the new list.
                if self.pauseMusic is True:
                    Mengine.musicResume()
                    self.pauseMusic = False
            else:
                self.__switchPlayList(playList)
            return False

        if self.__adoptPlayListIfSameTrack(playList) is True:
            self.playMusic = True
            if self.pauseMusic is True:
                Mengine.musicResume()
                self.pauseMusic = False
            return False

        self.__switchPlayList(playList)
        self.playMusic = True
        return False

    def __adoptPlayListIfSameTrack(self, playList):
        if playList is None or len(playList) == 0:
            return False
        currentTrack = self.lastTrack.get(id(self.playList)) if self.playList is not None else None
        if currentTrack is None:
            return False
        try:
            newIndex = playList.index(currentTrack)
        except ValueError:
            return False

        # Save outgoing playlist position
        if self.playList is not None and self.playList is not playList:
            self.playListIndex[id(self.playList)] = self.currentIndex

        self.playList = playList
        self.currentIndex = newIndex
        self.lastTrack[id(playList)] = currentTrack
        return True

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
            # Advance only if state still matches: same track was active and we're not paused/stopped.
            currentPlayList = self.playList
            if currentPlayList is None or len(currentPlayList) == 0:
                return
            if self.playMusic is False or self.pauseMusic is True:
                return
            if self.lastTrack.get(id(currentPlayList)) != track:
                return

            if self.random is True:
                self.currentIndex = self.__pickRandomIndex(currentPlayList)
            else:
                self.currentIndex = (self.currentIndex + 1) % len(currentPlayList)
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
