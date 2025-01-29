def onInitialize():
    from Multislots import baseslots
    from Multislots import finalslots
    Mengine.addGlobalModule("baseslots", baseslots)
    Mengine.addGlobalModule("finalslots", finalslots)

    import traceback
    Mengine.addGlobalModule("traceback", traceback)

    from Holder import Holder
    Mengine.addGlobalModule("Holder", Holder)

    from Event import Event
    Mengine.addGlobalModule("Event", Event)

    from Functor import Functor, FunctorStore
    Mengine.addGlobalModule("Functor", Functor)
    Mengine.addGlobalModule("FunctorStore", FunctorStore)

    import Utils
    Mengine.addGlobalModule("Utils", Utils)

    # import Enum
    # Mengine.addGlobalModule("Enum", Enum.make_enum)

    from Enum import Enum
    Mengine.addGlobalModule("Enum", Enum)

    import Trace
    Mengine.addGlobalModule("Trace", Trace)

    import Keys
    Mengine.addGlobalModule("Keys", Keys)

    from Notification import Notification
    Mengine.addGlobalModule("Notification", Notification)

    from LayerManager import LayerManager

    LayerManager.importLayerType("Foundation.Layer", "Layer2D")
    LayerManager.importLayerType("Foundation.Layer", "Layer2DParallax")
    LayerManager.importLayerType("Foundation.Layer", "Layer2DIsometric")

    from Foundation.Task.Iterator import Iterator
    Mengine.addGlobalModule("Iterator", Iterator)

    from Foundation.Task.Semaphore import Semaphore
    Mengine.addGlobalModule("Semaphore", Semaphore)

    from Foundation.Task.Refcount import Refcount
    Mengine.addGlobalModule("Refcount", Refcount)

    from GoogleAnalytics import GoogleAnalytics
    Mengine.addGlobalModule("GoogleAnalytics", GoogleAnalytics)

    from Foundation.ArrowManager import ArrowManager

    Arrows = ["Default"]

    from Foundation.SceneManager import SceneManager

    Scenes = ["Main"]

    SceneManager.importScenes("Foundation.Scenes", Scenes)

    tasks = [
        "TaskChain"
        , "TaskQuitApplication"
        , "TaskFork"
        , "TaskDummy"
        , "TaskNoSkip"
        , "TaskSkip"
        , "TaskDeadLock"
        , "TaskChainCancel"
        , "TaskChainRun"
        , "TaskAlias"
        , "TaskIf"
        , "TaskGuard"
        , "TaskScope"
        , "TaskScopeListener"
        , "TaskDebugBreak"

        , "TaskDelay"
        , "TaskPipe"
        , "TaskWait"
        , "TaskNotify"
        , "TaskListener"
        , "TaskEvent"
        , "TaskScopeEvent"
        , "TaskFilter"
        , "TaskFunction"
        , "TaskSkipFunction"
        , "TaskCallback"
        , "TaskIterator"

        , "TaskGameBlock"
        , "TaskGameUnblock"

        , "TaskPrint"
        , "TaskPrintTrace"
        , "TaskTrace"

        , "TaskStateMutex"
        , "TaskStateChange"

        , "TaskParallelNeck"
        , "TaskRaceNeck"
        , "TaskSwitch"
        , "TaskScopeSwitch"
        , "TaskRepeat"
        , "TaskFor"

        , "TaskScenePreparation"
        , "TaskSceneInit"
        , "TaskSceneEnter"
        , "TaskSceneLeave"
        , "TaskSceneLayerGroupEnable"
        , "TaskSceneLayerAddEntity"
        , "TaskSceneEntering"
        , "TaskSceneLeaving"
        , "TaskRemoveCurrentScene"
        , "TaskSceneActivate"
        , "TaskGameScenesBlock"
        , "TaskGameSceneEnter"

        , "TaskFadeIn"
        , "TaskFadeOut"
        , "TaskFadeSetStateFadeInComplete"

        , "TaskSetParam"
        , "TaskAppendParam"
        , "TaskDelParam"
        , "TaskChangeParam"

        , "TaskRunSystem"
        , "TaskStopSystem"

        , "TaskMouseButtonClick"
        , "TaskMouseButtonClickEnd"
        , "TaskMouseUse"
        , "TaskMouseMoveDistance"
        , "TaskMouseMove"

        , "TaskRemoveArrowAttach"
        , "TaskArrowAttach2"
        , "TaskArrowHide"
        , "TaskArrowModeChange"

        , "TaskEnable"
        , "TaskInteractive"
        , "TaskBlockInteractive"

        , "TaskMusicSetVolume"

        , "TaskNodeAlphaTo"
        , "TaskNodeColorTo"
        , "TaskNodeScaleTo"
        , "TaskNodeRotateTo"
        , "TaskNodeMoveTo"
        , "TaskNodeAccelerateTo"
        , "TaskNodeBezier2To"
        , "TaskNodeBezier2Follow"
        , "TaskNodeBezier3To"
        , "TaskNodeParabolaTo"
        , "TaskNodeVelocityTo"
        , "TaskNodeFollowTo"
        , "TaskNodeFollowToWorld"
        , "TaskNodeLocalHide"
        , "TaskNodeEnable"
        , "TaskNodeFlip"
        , "TaskNodeEnable"
        , "TaskNodeEnableGlobalMouseEvent"
        , "TaskNodeAddChild"
        , "TaskNodeSetPosition"
        , "TaskNodeSetOrigin"
        , "TaskNodePercentVisibilityTo"
        , "TaskNodeDestroy"
        , "TaskNodeRemoveFromParent"

        , "TaskNodeMovieEvent"

        , "TaskInterpolatorLinearFloat"

        , "TaskSurfaceAnimationPlay"

        , "TaskAnimatablePlay"
        , "TaskAnimatableStop"
        , "TaskAnimatablePause"
        , "TaskAnimatableEnd"
        , "TaskAnimatableInterrupt"
        , "TaskAnimatableRewind"

        , "TaskObjectAnimatablePlay"
        , "TaskObjectAnimatableStop"
        , "TaskObjectAnimatablePause"
        , "TaskObjectAnimatableResume"
        , "TaskObjectAnimatableEnd"
        , "TaskObjectAnimatableInterrupt"

        , "TaskObjectPlay"

        , "TaskMovieSlotAddChild"
        , "TaskMovieSlotAddObject"
        , "TaskMovieStop"
        , "TaskMoviePlay"
        , "TaskSubMoviePlay"
        , "TaskSubMovie2Play"
        , "TaskMoviePause"      # resume only for Movie2, because Movie is deprecated
        , "TaskMovieEnd"
        , "TaskMovieLastFrame"
        , "TaskMovieSocketClick"
        , "TaskMovieSocketEnter"
        , "TaskMovieSocketLeave"
        , "TaskMovieSocketMove"
        , "TaskMovieSocketEnable"
        , "TaskMovieRewind"
        , "TaskMovieInterrupt"

        , "TaskMovie2Stop"
        , "TaskMovie2Play"
        , "TaskMovie2Pause"
        , "TaskMovie2Resume"
        , "TaskMovie2End"
        , "TaskMovie2Rewind"
        , "TaskMovie2Interrupt"
        , "TaskMovie2SocketClick"
        , "TaskMovie2SocketEnter"
        , "TaskMovie2SocketLeave"
        , "TaskMovie2SocketMove"

        , "TaskNodeSocketClick"
        , "TaskNodeSocketEnter"
        , "TaskNodeSocketLeave"
        , "TaskNodeSocketMove"

        , "TaskAnimationPlay"
        , "TaskAnimationStop"
        , "TaskAnimationSetFrame"
        , "TaskAnimationSetSequence"
        , "TaskAnimationEnd"

        , "TaskVideoPlay"
        , "TaskVideoStop"
        , "TaskVideoEnd"

        , "TaskSoundEffect"
        , "TaskVoicePlay"

        , "TaskShift"
        , "TaskShiftNext"
        , "TaskPuffShowElement"
        , "TaskCheckBox"
        , "TaskCheckBoxBlockState"

        , "TaskMovieCheckBox"
        , "TaskMovie2CheckBox"

        , "TaskInteraction"

        , "TaskTransition"
        , "TaskTransitionClick"
        , "TaskTransitionEnter"
        , "TaskTransitionLeave"
        , "TaskTransitionBlock"
        , "TaskTransitionUnblock"

        , "TaskSocketClick"
        , "TaskSocketClickUp"
        , "TaskSocketClickEndUp"
        , "TaskSocketEnter"
        , "TaskSocketLeave"

        , "TaskSocketUse"# click socket with any object, don't remove attach

        , "TaskButtonClick"
        , "TaskButtonClickEndUp"
        , "TaskButtonEnter"
        , "TaskButtonLeave"
        , "TaskButtonBlockState"
        , "TaskButtonSetState"
        , "TaskButtonChangeState"
        , "TaskButtonUse"
        , "TaskButtonBlockKeys"
        , "TaskButtonSwitchMode"

        , "TaskObjectSetPosition"
        , "TaskObjectSetAlpha"
        , "TaskObjectSetScale"

        , "TaskObjectReturn"
        , "TaskObjectActivate"
        , "TaskObjectDeactivate"
        , "TaskObjectDestroy"

        , "TaskTextSetTextID"
        , "TaskObjectTextSetMaxVisibleChar"

        , "TaskTrigger"

        , "TaskStates"
        , "TaskKeyPress"

        , "TaskGameSceneInit"

        , "TaskCursorClickEmulate"
        , "TaskCursorSetPosition"

        , "TaskMovieButtonClick"
        , "TaskMovieButtonClickEnd"
        , "TaskMovieButtonPressed"
        , "TaskMovieButtonEnter"
        , "TaskMovieButtonLeave"
        , "TaskMovieButtonUse"

        , "TaskMovie2ButtonClick"
        , "TaskMovie2ButtonEnter"
        , "TaskMovie2ButtonLeave"

        , "TaskSemaphore"
        , 'TaskSemaphoreIncrement'
        , "TaskRefcount"

        , "TaskMovieSocketSwipe"

        , "TaskPrefetchGroup"
        , "TaskUnfetchGroup"
        , "TaskSendAnalytics"
        , "TaskSendAnalyticsScreenView"
        , 'TaskFacebookPostMessage'
        , 'TaskFacebookGetData'
        , 'TaskFacebookAuthentication'
        , 'TaskDownloadAsset'
        , 'TaskMountPak'
        , 'TaskSpinnerCheck'
        , 'TaskLoadVersionFiles'
        , 'TaskGetVersion'
        , 'TaskGetFtp'
        , 'TaskLoadPaks'
        , 'TaskNodeLoopedRotate'

        , "TaskHeaderData"
        , "TaskHeaderDataPlayfab"
        , "TaskVirtualAreaScroll"

        , "TaskMovie2LayerAlphaTo"
        ]

    from TaskManager import TaskManager
    TaskManager.importTasks("Foundation.Task", tasks)

    aliases = [
        "AliasTextPlay"
        , "AliasTextPlay2"

        , "AliasObjectMoveTo"
        , "AliasObjectScaleTo"
        , "AliasObjectAlphaTo"
        , "AliasMovie2AlphaTo"
        , "AliasObjectRotateTo"
        , "AliasObjectPercentVisibilityTo"
        , "AliasObjectBezier2To"
        , "AliasObjectBezier2Follow"

        , "AliasNodeTranslateTo"

        , "AliasMakeMovieAndPlayOnce"
        , "AliasMakeTriggerAndWait"
        ]

    from TaskManager import TaskManager
    TaskManager.importTasks("Foundation.Alias", aliases)

    policies = [
        "PolicyExternalAchieveProgressAppleGameCenter"
        , "PolicyExternalAchieveProgressGooglePlay"
    ]

    from TaskManager import TaskManager
    TaskManager.importTasks("Foundation.Policy", policies)

    traces = [
        "TaskInventoryAddCountItem"
        , "TaskInventoryRemoveItem"
        , "TaskNodeTranslateTo"
        , "AliasObjectAlphaTo"
        , "AliasMovie2AlphaTo"
        , "TaskChainCancel"
        , "TaskManager"
        , "TaskChain"
        , "TaskListener"
        , "AliasNodeTranslateTo"
        , "TaskInventoryFindItem"
        , "TaskInventoryFindCountItem"
        , "InventoryCountItem"
        , "ObjectInventory"
        , "InventoryItem"
        , "Inventory"
        , "Actor"
        , "BaseEntity"
        , "BaseObject"
        , "Object"
        , "Manager"
        , "Movie"
        , "Movie2"
        , "HOG"
        , "MixinObjectTemplate"
        , "Utils"
        , "Task"
        , "Policy"
        , "Group"
        , "SceneManager"
        , "Notification"
        , "Main"
        , "Item"
        , "HOGInventory"
        , "ArrowManager"
        , "ObjectManager"
        , "GroupManager"
        , "TaskSceneLayerGroupEnable"
        , "Button"
        , "HintAction"
        , "AliasTransition"
        , "System"
        , "Entity"
        , "Command"
        , "MovieButton"
        , "Movie2Button"
        , "Provider"
        ]

    from TraceManager import TraceManager
    TraceManager.addTraces(traces)

    from Foundation.Notificator import Notificator
    Mengine.addGlobalModule("Notificator", Notificator)

    notifiers = [
        #    Notificator.onSave
        "onResume"
        , "onCommandLayerEnable"
        , "onSetCurrentChapter"

        , "onLoadSession"

        , "onCustomCursor"

        , "onTaskRun"
        , "onTaskComplete"

        , "onScenePreparation"
        , "onSceneInit"
        , "onSceneRestartBegin"
        , "onSceneRestartEnd"
        , "onSceneEnter"
        , "onSceneLeave"
        , "onSceneRemoved"
        , "onSceneChange"

        , "onSceneActivate"
        , "onSceneDeactivate"

        , "onInteractionMouseLeave"
        , "onInteractionMouseEnter"
        , "onInteractionClickBegin"
        , "onInteractionClick"
        , "onInteractionClickUpBegin"
        , "onInteractionClickUp"
        , "onInteractionClickEnd"
        , "onInteractionClickEndUp"

        , "InventoryItemTaken"

        , "onItemClickBegin"
        , "onItemClick"
        , "onItemClickEnd"
        , "onItemMouseEnter"
        , "onItemMouseLeave"

        , "onSocketClickBegin"
        , "onSocketClick"
        , "onSocketSoundClick"
        , "onSocketClickUpBegin"
        , "onSocketClickUp"
        , "onSocketClickEnd"
        , "onSocketClickEndUp"
        , "onSocketMouseEnter"
        , "onSocketSoundEnter"
        , "onSocketMouseLeave"

        , "onTransition"
        , "onTransitionClickBegin"
        , "onTransitionClick"
        , "onTransitionChangeScene"
        , "onTransitionHOGMouseEnter"
        , "onTransitionHOGMouseLeave"
        , "onTransitionUpMouseEnter"
        , "onTransitionUpMouseLeave"
        , "onTransitionBackMouseEnter"
        , "onTransitionBackMouseLeave"
        , "onTransitionLeftMouseEnter"
        , "onTransitionUpLeftMouseEnter"
        , "onTransitionUpLeftMouseLeave"
        , "onTransitionLeftMouseLeave"
        , "onTransitionRightMouseEnter"
        , "onTransitionUpRightMouseEnter"
        , "onTransitionRightMouseLeave"
        , "onTransitionUpRightMouseLeave"
        , "onTransitionPuzzleMouseEnter"
        , "onTransitionPuzzleMouseLeave"
        , "onTransitionMouseEnter"
        , "onTransitionMouseLeave"
        , "onTransitionBegin"
        , "onTransitionEnd"
        , "onTransitionUseBegin"
        , "onTransitionUse"
        , "onTransitionBlock"
        , "onTransitionEnable"

        , "onGameBlock"
        , "onBlockKeyBoard"

        , "onZoomInit"
        , "onZoomEnter"
        , "onZoomLeave"
        , "onZoomEmpty"
        , "onZoomClose"
        , "onZoomForceClose"
        , "onZoomForceOpen"
        , "onZoomMouseEnter"
        , "onZoomMouseLeave"
        , "onZoomOpen"
        , "onZoomClickBegin"
        , "onZoomClick"
        , "onZoomClickEnd"
        , "onZoomUseBegin"
        , "onZoomUse"
        , "onZoomUseEnd"
        , "onZoomBlockClose"
        , "onZoomEnable"

        , "onButtonMouseLeave"
        , "onButtonMouseEnter"
        , "onButtonClickBegin"
        , "onButtonClick"
        , "onButtonClickUp"
        , "onButtonClickEnd"
        , "onButtonClickEndUp"
        , "onButtonSoundClick"
        , "onButtonSoundEnter"
        , "onButtonSwitchOn"
        , "onButtonSwitchOff"

        , "onMovieButtonPush"
        , "onMovieButtonRelease"
        , "onMovieButtonClick"
        , "onMovieButtonClickEnd"
        , "onMovieButtonPressed"
        , "onMovieButtonMouseEnter"
        , "onMovieButtonMouseLeave"

        , "onMovie2ButtonMouseEnter"
        , "onMovie2ButtonMouseLeave"
        , "onMovie2ButtonPush"
        , "onMovie2ButtonPressed"
        , "onMovie2ButtonRelease"
        , "onMovie2ButtonClick"
        , "onMovie2ButtonClickEnd"

        , "onArrowPreparation"
        , "onArrowActivate"
        , "onArrowDeactivate"
        , "onArrowAttach"
        , "onArrowDeattach"

        , "onLayerGroupPreparation"
        , "onLayerGroupEnableBegin"
        , "onLayerGroupEnable"
        , "onLayerGroupRelease"
        , "onLayerGroupDisable"

        , "TaskAliasRun"
        , "TaskAliasEnd"

        , "onStageInit"
        , "onStageLoad"
        , "onStageSave"
        , "onStageRun"
        , "onStageResume"
        , "onStageInvalidLoad"

        , "onCompleteStage"

        , "onStateChange"
        , "onSlider"
        , "onCheckBox"
        , "onMovieCheckBox"
        , "onMovie2CheckBox"

        , "onAnimatableEnd"
        , "onAnimationEnd"
        , "onVideoEnd"

        , "onParagraphRun"
        , "onParagraphComplete"

        , "onObjectEnable"
        , "onObjectDisable"

        , "onKeyEvent2"
        , "onKeyEvent2End"

        , "onZoomBlockOpen"
        , "onTransitionBlockOpen"

        , "onSliderUp"
        , "onSliderDown"

        , "onButtonEnter"

        , "onSwitchChainsClick"

        , "EditBoxEmpty"
        , "EditBoxChange"
        , "EditBoxFocus"
        , "EditBoxUnhold"
        , "EditBoxKeyEvent"

        , "onMouseButtonEvent2"

        , "onChargerRun"
        , "onChargerRelease"
        , "onChargerCharge"
        , "onChargerSkip"
        , "onChargerReload"

        , "onNodeSocketClickSuccessful"

        , "onMovieSocketEnter"
        , "onMovieSocketLeave"
        , "onMovieSocketClick"
        , "onMovieSocketClickSuccessful"
        , "onMovieSocketMove"
        , "onMovieLoop"

        , "onSessionNew"
        , "onSessionSave"
        , "onSessionLoad"
        , "onSessionLoadComplete"
        , "onSessionLoadInvalid"
        , "onSessionRemove"
        , "onSessionRemoveComplete"

        , "onProgressBarUpdate"

        , "onMovieEditBoxFocus"
        , "MovieEditBoxKeyEvent"

        , "MovieEditBoxEmpty"
        , "MovieEditBoxChange"

        , "onMovie2EditBoxFocus"
        , "onMovie2EditBoxFocusLost"
        , "onMovie2EditBoxKeyEvent"

        , "onMovie2EditBoxEmpty"
        , "onMovie2EditBoxChange"

        , 'PlanetEnter'
        , 'PlanetLeave'
        , 'PlanetDefeat'
        , 'MonsterFight'
        , 'MonsterDead'
        , 'TestConsoleOpen'
        , 'DungeonPlotTwistTextId'
        , 'WarpGateTextId'
        , 'onTabGroupSelect'

        , 'onCombatSpinnerChange'
        , 'onCombatSpinnerDamageTarget'
        , 'onCombatSpinnerAddAbility'
        , 'onCombatSpinnerEndState'

        , 'onCombatSpinnerEventDamageTarget'
        , 'onFacebookAuthEscape'
        , 'onLoadedVersionFiles'
        , 'onSpinnerStop'
        , 'onLoadingVersionMessage'

        , 'onStageTimePassed'

        , 'onPrefetchGroupsTaggedBegin'
        , 'onPrefetchGroupsTaggedComplete'
        , 'onPrefetchGroupsTaggedFinished'
        , 'onHintActionItemCollectEnd'
        , 'onInventoryRise'

        , 'onTaskGuardUpdate'

        , 'onMobileKeyboardShow'
        , 'onEditboxSetActive'

        , 'onAttachedArrow'

        , 'onEnableSceneLayerGroup'
        , 'onDisableSceneLayerGroup'
        , 'onGameSceneChange'

        , 'onAdPointStart'
        , 'onDisableInterstitialAds'

        , "onAdShowCompleted"
        , "onAdRevenuePaid"
        , "onAdUserRewarded"

        , "onRequestPromoCodeResult"

        , "onAvailableAdsEnded"
        , "onAvailableAdsNew"

        , "onUpdateGoldBalance"
        , "onUpdateEnergyBalance"
        , "onGameStoreNotEnoughGold"
        , "onGameStorePayGoldSuccess"
        , "onGameStorePayGoldFailed"
        , "onGameStorePayGold"
        , "onGameStoreSentRewards"

        , "onProductAlreadyOwned"
        , "onRestorePurchasesDone"
        , "onPaySuccess"
        , "onPayFailed"
        , "onPayComplete"
        , "onProductsUpdate"
        , "onProductsUpdateDone"
        , "onDelayPurchased"
        , "onReleasePurchased"

        , "onAppRated"
        , "onGetRemoteConfig"

        , "onUserLoggedIn"
        , "onUserLoggedOut"

    ]

    Notificator.addIdentities(notifiers)

    from Foundation.AccountManager import AccountManager

    def accountSetuper(accountID, isGlobal):
        if isGlobal is True:
            return

        Mengine.addCurrentAccountSetting("InvalidLoad", u"False", None)

    AccountManager.addCreateAccountExtra(accountSetuper)

    from ObjectManager import ObjectManager
    from EntityManager import EntityManager

    Types = [
        "Animation"
        , "Interaction"
        , "Button"
        , "CheckBox"
        , "EditBox"
        , "Fade"
        , "Group"
        , "Movie"
        , "Movie2"
        , "Point"
        , "Puff"
        , "Shift"
        , "Slider"
        , "Socket"
        , "Sprite"
        , "Switch"
        , "States"
        , "Text"
        , "Video"
        , "Window"
        , "Viewport"
        ]

    if Mengine.getGameParamBool("NotUseDefaultEntitiesList", False) is True:
        Types = []
        from Foundation.DatabaseManager import DatabaseManager
        records = DatabaseManager.getDatabaseRecordsFilterBy("Database", "Entities", Module="Foundation")

        for record in records:
            Types.append(record.get("Type"))

    ObjectManager.importObjects("Foundation.Object", Types)
    EntityManager.importEntities("Foundation.Entities", Types)

    EntityManager.importEntity("Foundation.Entities", "Landscape2D")
    ObjectManager.importObject("Foundation.Entities.Landscape2D", "Landscape2D")

    EntityManager.importEntity("Foundation.Entities", "MovieButton")
    ObjectManager.importObject("Foundation.Entities.MovieButton", "MovieButton")

    EntityManager.importEntity("Foundation.Entities", "Movie2Button")
    ObjectManager.importObject("Foundation.Entities.Movie2Button", "Movie2Button")

    EntityManager.importEntity("Foundation.Entities", "ProgressBar")
    ObjectManager.importObject("Foundation.Entities.ProgressBar", "ProgressBar")

    EntityManager.importEntity("Foundation.Entities", "MovieCheckBox")
    ObjectManager.importObject("Foundation.Entities.MovieCheckBox", "MovieCheckBox")

    EntityManager.importEntity("Foundation.Entities", "Movie2CheckBox")
    ObjectManager.importObject("Foundation.Entities.Movie2CheckBox", "Movie2CheckBox")

    ObjectManager.importObject("Foundation.Entities.Charger", "Charger")
    EntityManager.importEntity("Foundation.Entities", "Charger")

    EntityManager.importEntity("Foundation.Entities", "MovieVirtualArea")
    ObjectManager.importObject("Foundation.Entities.MovieVirtualArea", "MovieVirtualArea")

    EntityManager.importEntity("Foundation.Entities", "MovieScrollbar")
    ObjectManager.importObject("Foundation.Entities.MovieScrollbar", "MovieScrollbar")

    EntityManager.importEntity("Foundation.Entities", "Movie2Scrollbar")
    ObjectManager.importObject("Foundation.Entities.Movie2Scrollbar", "Movie2Scrollbar")

    EntityManager.importEntity("Foundation.Entities", "MovieProgressBar")
    ObjectManager.importObject("Foundation.Entities.MovieProgressBar", "MovieProgressBar")

    EntityManager.importEntity("Foundation.Entities", "Movie2ProgressBar")
    ObjectManager.importObject("Foundation.Entities.Movie2ProgressBar", "Movie2ProgressBar")

    EntityManager.importEntity("Foundation.Entities", "MovieEditBox")
    ObjectManager.importObject("Foundation.Entities.MovieEditBox", "MovieEditBox")

    EntityManager.importEntity("Foundation.Entities", "Movie2EditBox")
    ObjectManager.importObject("Foundation.Entities.Movie2EditBox", "Movie2EditBox")

    EntityManager.importEntity("Foundation.Entities", "MovieTabsGroup")
    ObjectManager.importObject("Foundation.Entities.MovieTabsGroup", "MovieTabsGroup")

    providers = [
        "AdvertisementProvider"
        , "RatingAppProvider"
        , "PaymentProvider"
        , "ProductsProvider"
        , "FacebookProvider"
        , "AchievementsProvider"
        , "AuthProvider"   # main account
        , "RemoteConfigProvider"
        , "AdPointProvider"
        , "AnalyticsProvider"
    ]
    from Foundation.ProviderManager import ProviderManager
    ProviderManager.importProviders("Foundation.Providers", providers)

    Trace.msg("Foundation.onInitialize")

    from Foundation.DatabaseManager import DatabaseManager
    DatabaseManager.onInitialize()

    from Foundation.ArrowManager import ArrowManager
    ArrowManager.onInitialize()

    from Foundation.SceneManager import SceneManager
    SceneManager.onInitialize()

    from Foundation.GroupManager import GroupManager
    GroupManager.onInitialize()

    from Foundation.Business.ContractManager import ContractManager
    ContractManager.onInitialize()

    from Foundation.Business.BankManager import BankManager
    BankManager.onInitialize()

    from Foundation.PrefetchResourceManager import PrefetchResourceManager
    PrefetchResourceManager.onInitialize()

    from Foundation.PrefetchGroupManager import PrefetchGroupManager
    PrefetchGroupManager.onInitialize()

    from Foundation.PrefetchGroupNotifyManager import PrefetchGroupNotifyManager
    PrefetchGroupNotifyManager.onInitialize()

    from Foundation.SessionManager import SessionManager
    SessionManager.onInitialize()

    return True


def onFinalize():
    Trace.msg("Foundation.onFinalize")

    from Foundation.SessionManager import SessionManager
    SessionManager.onFinalize()

    from Foundation.Business.ContractManager import ContractManager
    ContractManager.onFinalize()

    from Foundation.Business.BankManager import BankManager
    BankManager.onFinalize()

    from Foundation.TaskManager import TaskManager
    TaskManager.onFinalize()

    from Foundation.ArrowManager import ArrowManager
    ArrowManager.onFinalize()

    from Foundation.SystemManager import SystemManager
    SystemManager.onFinalize()

    from Foundation.EntityManager import EntityManager
    EntityManager.onFinalize()

    from Foundation.SceneManager import SceneManager
    SceneManager.onFinalize()

    from Foundation.GroupManager import GroupManager
    GroupManager.onFinalize()

    from Foundation.DemonManager import DemonManager
    DemonManager.onFinalize()

    from Foundation.StateManager import StateManager
    StateManager.onFinalize()

    from Foundation.DefaultManager import DefaultManager
    DefaultManager.onFinalize()

    from Foundation.PrefetchGroupManager import PrefetchGroupManager
    PrefetchGroupManager.onFinalize()

    from Foundation.PrefetchResourceManager import PrefetchResourceManager
    PrefetchResourceManager.onFinalize()

    from Foundation.DatabaseManager import DatabaseManager
    DatabaseManager.onFinalize()

    from Notification import Notification
    Notification.onFinalize()

    from Foundation.ProviderManager import ProviderManager
    ProviderManager.onFinalize()
