from Foundation.DatabaseManager import DatabaseManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Manager import Manager


class MusicManager(Manager):
    """ Music registry.

    Each record in the bound database may declare:
        - SceneName        : optional. If set, the track is appended to this scene's playlist.
                             If omitted, the track is appended to the global (default) playlist.
        - MusicResourceName: ResourceMusic name.

    Multiple records sharing the same SceneName (or all without SceneName) form a
    sequential playlist played in declaration order.
    """

    s_default = []     # global playlist (list of ResourceMusic names)
    s_scenes = {}      # scene_name -> list of tracks
    s_tags = {}

    s_gameMusicResourceName = None
    s_menuMusicResourceName = None

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)
        for record in records:
            SceneName = record.get("SceneName")
            track = record.get("MusicResourceName", None)

            if track is None:
                continue

            if SceneName is None:
                MusicManager.s_default.append(track)
                continue

            playlist = MusicManager.s_scenes.get(SceneName)
            if playlist is None:
                playlist = []
                MusicManager.s_scenes[SceneName] = playlist
            playlist.append(track)

        return True

    @staticmethod
    def getScenePlayList(sceneName):
        return MusicManager.s_scenes.get(sceneName)

    @staticmethod
    def hasScenePlayList(sceneName):
        return sceneName in MusicManager.s_scenes

    @staticmethod
    def getDefaultPlayList():
        if len(MusicManager.s_default) == 0:
            return None
        return MusicManager.s_default

    @staticmethod
    def getMusic():
        return MusicManager.s_scenes

    @staticmethod
    def getTags():
        return MusicManager.s_tags

    @staticmethod
    def getGameMusicResourceName():
        if MusicManager.s_gameMusicResourceName is None:
            MusicGameScene = DefaultManager.getDefault("MusicGameScene", None)
            MusicManager.s_gameMusicResourceName = MusicGameScene

        return MusicManager.s_gameMusicResourceName

    @staticmethod
    def getMenuMusicResourceName():
        if MusicManager.s_menuMusicResourceName is None:
            MusicMenuScene = DefaultManager.getDefault("MusicMenuScene", None)
            MusicManager.s_menuMusicResourceName = MusicMenuScene

        return MusicManager.s_menuMusicResourceName
