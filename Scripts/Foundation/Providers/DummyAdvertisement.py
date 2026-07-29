from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.SceneManager import SceneManager
from Foundation.TaskManager import TaskManager


class _DummyInterstitialOverlay(object):
    TEXT_ID = "__ID_TIMING"

    def __init__(self, close_semaphore):
        self.close_semaphore = close_semaphore
        self.root = None
        self.hotspot = None
        self.countdown_text = None
        self.button_node = None
        self.button_pressed = False
        self.button_close_pending = False
        self.ok_rect = None

    def _createSolid(self, name, size, color, position, parent=None):
        surface = Mengine.createSurface("SurfaceSolidColor")
        surface.setName("{}Surface_{}".format(name, id(self)))
        surface.setSolidColor(color)
        surface.setSolidSize(size)

        if parent is None:
            parent = self.root

        shape = parent.createChild("ShapeQuadFixed")
        shape.setName("{}Shape_{}".format(name, id(self)))
        shape.setSurface(surface)
        shape.setLocalPosition(position)
        shape.enable()

        return shape

    def _createText(self, name, text, position, scale=1.0, parent=None):
        if parent is None:
            parent = self.root

        text_field = parent.createChild("TextField")
        text_field.setName("{}Text_{}".format(name, id(self)))
        text_field.setTextId(self.TEXT_ID)
        text_field.setTextFormatArgs(text)
        text_field.setFontColor((1.0, 1.0, 1.0, 1.0))
        text_field.setHorizontalCenterAlign()
        text_field.setVerticalCenterAlign()
        text_field.setLocalPosition(position)
        text_field.setLocalScale((scale, scale, 1.0))
        text_field.enable()

        return text_field

    def _animateButton(self, scale, time, callback):
        self.button_node.scaleStop()
        return self.button_node.scaleTo(
            time,
            (scale, scale, 1.0),
            "easyLinear",
            callback
        )

    def _onButtonScaleCompleted(self, node, is_end):
        pass

    def _onButtonReleaseAnimationCompleted(self, node, is_end):
        if self.root is None:
            return

        self.close_semaphore.setValue(True)

    def _onMouseButtonEvent(self, context, event):
        if event.button != 0:
            return True

        if event.isPressed is False or self.button_close_pending is True:
            return True

        x = event.position.world.x
        y = event.position.world.y
        left, top, right, bottom = self.ok_rect
        inside_button = left <= x <= right and top <= y <= bottom

        if event.isDown is True:
            if inside_button is True:
                self.button_pressed = True
                self._animateButton(0.94, 70.0, self._onButtonScaleCompleted)

            return True

        if self.button_pressed is False:
            return True

        self.button_pressed = False

        if inside_button is True:
            self.button_close_pending = True
            affector = self._animateButton(1.0, 90.0, self._onButtonReleaseAnimationCompleted)

            if affector is None:
                self.close_semaphore.setValue(True)
        else:
            self._animateButton(1.0, 90.0, self._onButtonScaleCompleted)

        return True

    def show(self):
        scene = SceneManager.getCurrentScene()
        if scene is None:
            Trace.msg_err("<DummyAdvertisement> can't show interstitial overlay: current scene is None")
            return False

        scene_node = scene.node
        if scene_node is None:
            Trace.msg_err("<DummyAdvertisement> can't show interstitial overlay: scene node is None")
            return False

        resolution = Mengine.getContentResolution()
        width = float(resolution.getWidth())
        height = float(resolution.getHeight())

        panel_width = min(width * 0.82, 520.0)
        panel_height = min(height * 0.44, 360.0)
        panel_x = (width - panel_width) * 0.5
        panel_y = (height - panel_height) * 0.5

        button_width = min(panel_width - 80.0, 220.0)
        button_height = 68.0
        button_x = (width - button_width) * 0.5
        button_y = panel_y + panel_height - button_height - 35.0

        self.root = Mengine.createNode("Interender")
        self.root.setName("DummyInterstitialOverlay_{}".format(id(self)))
        scene_node.addChild(self.root)
        self.root.enable()

        self._createSolid("Backdrop", (width, height), (0.0, 0.0, 0.0, 0.78), (0.0, 0.0))
        self._createSolid("Panel", (panel_width, panel_height), (0.08, 0.10, 0.16, 1.0), (panel_x, panel_y))
        self.button_node = self.root.createChild("Interender")
        self.button_node.setName("DummyInterstitialButton_{}".format(id(self)))
        self.button_node.setLocalPosition((
            button_x + button_width * 0.5,
            button_y + button_height * 0.5
        ))
        self.button_node.enable()

        self._createSolid("OkButton", (button_width, button_height), (0.12, 0.48, 0.80, 1.0), (-button_width * 0.5, -button_height * 0.5), parent=self.button_node)

        center_x = width * 0.5
        self._createText(
            "Title",
            "INTERSTITIAL",
            (center_x, panel_y + 70.0),
            1.25
        )
        self._createText(
            "Advertisement",
            "Dummy advertisement",
            (center_x, panel_y + 130.0)
        )
        self.countdown_text = self._createText(
            "Countdown",
            "",
            (center_x, panel_y + 190.0),
            0.8
        )
        self._createText(
            "Ok",
            "OK",
            (0.0, 0.0),
            parent=self.button_node
        )

        self.ok_rect = (
            button_x,
            button_y,
            button_x + button_width,
            button_y + button_height
        )

        self.hotspot = self.root.createChild("HotSpotPolygon")
        self.hotspot.setName("DummyInterstitialHotSpot_{}".format(id(self)))
        self.hotspot.setPolygon([
            (0.0, 0.0),
            (width, 0.0),
            (width, height),
            (0.0, height)
        ])
        self.hotspot.setExclusive(True)
        self.hotspot.setEventListener(onHandleMouseButtonEvent=self._onMouseButtonEvent)
        self.hotspot.enable()

        Trace.msg("<DummyAdvertisement> interstitial overlay shown")

        return True

    def setCountdown(self, seconds):
        if self.countdown_text is None:
            return

        self.countdown_text.setTextFormatArgs("Closes automatically in {}s".format(seconds))

    def destroy(self):
        if self.root is None:
            return

        if self.hotspot is not None:
            self.hotspot.setEventListener(onHandleMouseButtonEvent=None)

        if self.button_node is not None:
            self.button_node.scaleStop()

        self.root.removeFromParent()
        Mengine.destroyNode(self.root)

        self.root = None
        self.hotspot = None
        self.countdown_text = None
        self.button_node = None
        self.button_pressed = False
        self.button_close_pending = False
        self.ok_rect = None

        Trace.msg("<DummyAdvertisement> interstitial overlay closed")


class DummyAdvertisement(object):
    """ Dummy Provider """

# ----- Banner ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def showBanner():
        AdType = "Banner"
        display_failed = Mengine.rand(20) < 5
        Trace.msg("<DummyAdvertisement> show advert {} (fail: {})...".format(AdType, display_failed))
        return True

    @staticmethod
    def hideBanner():
        AdType = "Banner"
        return True

    @staticmethod
    def getBannerWidth():
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x

        return game_width

    @staticmethod
    def getBannerHeight():
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        game_height = viewport.end.y - viewport.begin.y

        if Utils.isTabletByAspectRatio(game_width, game_height) is True:
            banner_height = DummyAdvertisement.getTabletAdaptiveBannerHeight(game_width)
        else:
            banner_height = DummyAdvertisement.getPhoneAdaptiveBannerHeight(game_width)

        return banner_height

    @staticmethod
    def getPhoneAdaptiveBannerHeight(width):
        """ Banners are automatically sized to 320x50 on phones """
        return 50.0 * width / 320.0

    @staticmethod
    def getTabletAdaptiveBannerHeight(width):
        """ Banners are automatically sized to 728x90 on tablets """
        return 90.0 * width / 728.0

# ----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def hasInterstitialAdvert():
        status = True
        Trace.msg("<DummyAdvertisement> hasInterstitialAdvert result = {}".format(status))
        return status

    @staticmethod
    def canYouShowInterstitialAdvert(placement):
        status = Mengine.rand(100) < 20
        Trace.msg("<DummyAdvertisement> canYouShowInterstitialAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def showInterstitialAdvert(placement):
        FakeWatchDelay = 10000
        display_failed = Mengine.rand(20) < 5
        revenue = 0.02
        close_semaphore = Semaphore(False, "DummyInterstitialClose")
        overlay = _DummyInterstitialOverlay(close_semaphore)

        with TaskManager.createTaskChain(Name="DummyShowInterstitialAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showInterstitialAdvert {}, delay {}s (fail: {})...".format(
                placement, round(float(FakeWatchDelay) / 1000, 1), display_failed))
            with source.addIfTask(overlay.show) as (overlay_shown, overlay_failed):
                overlay_shown.addDummy()
                overlay_failed.addSemaphore(close_semaphore, To=True)

            with source.addRaceTask(2) as (close, countdown):
                close.addSemaphore(close_semaphore, From=True)

                for seconds in range(int(FakeWatchDelay / 1000), 0, -1):
                    countdown.addFunction(overlay.setCountdown, seconds)
                    countdown.addDelay(1000)

            source.addFunction(overlay.destroy)

            if display_failed:
                source.addFunction(AdvertisementProvider.cbInterstitialShowCompleted, False, {"placement": placement})
            else:
                source.addFunction(AdvertisementProvider.cbInterstitialShowCompleted, True, {"placement": placement})
                source.addFunction(AdvertisementProvider.cbInterstitialRevenuePaid, {"placement": placement, "revenue": revenue})

        return True

    @staticmethod
    def hasRewardedAdvert():
        status = True
        Trace.msg("<DummyAdvertisement> hasRewardedAdvert result = {}".format(status))
        return status

    @staticmethod
    def canOfferRewardedAdvert(placement):
        status = Mengine.rand(20) < 15
        Trace.msg("<DummyAdvertisement> canOfferRewardedAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def canYouShowRewardedAdvert(placement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> canYouShowRewardedAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def showRewardedAdvert(placement):
        FakeWatchDelay = 5000
        GoldReward = 1
        display_failed = Mengine.rand(20) < 5
        revenue = 0.05

        with TaskManager.createTaskChain(Name="DummyShowRewardedAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showRewardedAdvert {}, delay {}s (fail: {})...".format(
                placement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addFunction(AdvertisementProvider.cbRewardedShowCompleted, False, {"placement": placement})
            else:
                source.addDelay(FakeWatchDelay)

                source.addFunction(AdvertisementProvider.cbRewardedUserRewarded, {"placement": placement})

                source.addFunction(AdvertisementProvider.cbRewardedShowCompleted, True, {"placement": placement})
                source.addFunction(AdvertisementProvider.cbRewardedRevenuePaid, {"placement": placement, "revenue": revenue})

        return True

    @staticmethod
    def setProvider():
        def _HasRewardedAdvert():
            return DummyAdvertisement.hasRewardedAdvert()
        def _HasInterstitialAdvert():
            return DummyAdvertisement.hasInterstitialAdvert()
        def _ShowRewardedAdvert(placement):
            return DummyAdvertisement.showRewardedAdvert(placement)
        def _CanOfferRewardedAdvert(placement):
            return DummyAdvertisement.canOfferRewardedAdvert(placement)
        def _CanYouShowRewardedAdvert(placement):
            return DummyAdvertisement.canYouShowRewardedAdvert(placement)
        def _ShowInterstitialAdvert(placement):
            return DummyAdvertisement.showInterstitialAdvert(placement)
        def _IsShowingInterstitialAdvert():
            return AdvertisementProvider.s_fullscreen_ad_showing
        def _IsShowingRewardedAdvert():
            return False
        def _CanYouShowInterstitialAdvert(placement):
            return DummyAdvertisement.canYouShowInterstitialAdvert(placement)
        def _ShowBanner():
            return DummyAdvertisement.showBanner()
        def _HideBanner():
            return DummyAdvertisement.hideBanner()
        def _GetBannerHeight():
            return DummyAdvertisement.getBannerHeight()
        def _GetBannerWidth():
            return DummyAdvertisement.getBannerWidth()
        def _GetNoAds():
            return False

        methods = dict(
            # banner:
            ShowBanner=_ShowBanner,
            HideBanner=_HideBanner,
            GetBannerHeight=_GetBannerHeight,
            GetBannerWidth=_GetBannerWidth,
            # interstitial:
            HasInterstitialAdvert=_HasInterstitialAdvert,
            CanYouShowInterstitialAdvert=_CanYouShowInterstitialAdvert,
            ShowInterstitialAdvert=_ShowInterstitialAdvert,
            IsShowingInterstitialAdvert=_IsShowingInterstitialAdvert,
            # rewarded:
            HasRewardedAdvert=_HasRewardedAdvert,
            CanOfferRewardedAdvert=_CanOfferRewardedAdvert,
            CanYouShowRewardedAdvert=_CanYouShowRewardedAdvert,
            ShowRewardedAdvert=_ShowRewardedAdvert,
            IsShowingRewardedAdvert=_IsShowingRewardedAdvert,
            # no ads:
            GetNoAds=_GetNoAds,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
