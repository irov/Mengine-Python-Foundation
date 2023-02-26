def onInitialize():
    from Multislots import baseslots
    from Multislots import finalslots
    Menge.addGlobalModule("baseslots", baseslots)
    Menge.addGlobalModule("finalslots", finalslots)

    import traceback
    Menge.addGlobalModule("traceback", traceback)

    from Holder import Holder
    Menge.addGlobalModule("Holder", Holder)

    from Event import Event
    Menge.addGlobalModule("Event", Event)

    from Functor import Functor, FunctorStore
    Menge.addGlobalModule("Functor", Functor)
    Menge.addGlobalModule("FunctorStore", FunctorStore)

    import Utils
    Menge.addGlobalModule("Utils", Utils)

    # import Enum
    # Menge.addGlobalModule("Enum", Enum.make_enum)

    from Enum import Enum
    Menge.addGlobalModule("Enum", Enum)

    import Trace
    Menge.addGlobalModule("Trace", Trace)

    import Keys
    Menge.addGlobalModule("Keys", Keys)

    from Notification import Notification
    Menge.addGlobalModule("Notification", Notification)

    from LayerManager import LayerManager

    LayerManager.importLayerType("GOAP2.Layer", "Layer2D")
    LayerManager.importLayerType("GOAP2.Layer", "Layer2DParallax")
    LayerManager.importLayerType("GOAP2.Layer", "Layer2DIsometric")

    from GOAP2.Task.Iterator import Iterator
    Menge.addGlobalModule("Iterator", Iterator)

    from GOAP2.Task.Semaphore import Semaphore
    Menge.addGlobalModule("Semaphore", Semaphore)

    from GOAP2.Task.Refcount import Refcount
    Menge.addGlobalModule("Refcount", Refcount)

    from GoogleAnalytics import GoogleAnalytics
    Menge.addGlobalModule("GoogleAnalytics", GoogleAnalytics)

    from Facebook import Facebook
    Menge.addGlobalModule("Facebook", Facebook)

    from GOAP2.ArrowManager import ArrowManager

    Arrows = ["Default"]

    ArrowManager.importArrows("GOAP2.Arrows", Arrows)

    from GOAP2.SceneManager import SceneManager

    Scenes = ["Main"]

    SceneManager.importScenes("GOAP2.Scenes", Scenes)

    tasks = ["TaskChain", "TaskQuitApplication", "TaskFork", "TaskDummy", "TaskNoSkip", "TaskSkip", "TaskDeadLock", "TaskChainCancel", "TaskChainRun", "TaskAlias", "TaskIf", "TaskGuard", "TaskScope", "TaskScopeListener", "TaskDebugBreak"

        , "TaskDelay", "TaskPipe", "TaskWait", "TaskNotify", "TaskListener", "TaskEvent", "TaskScopeEvent", "TaskFilter", "TaskFunction", "TaskSkipFunction", "TaskCallback", "TaskIterator"

        , "TaskGameBlock", "TaskGameUnblock"

        , "TaskPrint", "TaskPrintTrace", "TaskTrace"

        , "TaskStateMutex", "TaskStateChange"

        , "TaskParallelNeck", "TaskRaceNeck", "TaskSwitch", "TaskScopeSwitch", "TaskRepeat", "TaskFor"

        , "TaskScenePreparation", "TaskSceneInit", "TaskSceneEnter", "TaskSceneLeave", "TaskSceneLayerGroupEnable", "TaskSceneLayerAddEntity", "TaskSceneEntering", "TaskSceneLeaving", "TaskRemoveCurrentScene", "TaskSceneActivate", "TaskGameScenesBlock", "TaskGameSceneEnter"

        , "TaskStageInit", "TaskStageSave", "TaskStageResume"

        , "TaskFadeIn", "TaskFadeOut", "TaskFadeSetStateFadeInComplete"

        , "TaskSetParam", "TaskAppendParam", "TaskDelParam", "TaskChangeParam"

        , "TaskRunSystem", "TaskStopSystem", "TaskStageRun"

        , "TaskMouseButtonClick", "TaskMouseButtonClickEnd", "TaskMouseUse", "TaskMouseMoveDistance", "TaskMouseMove"

        , "TaskRemoveArrowAttach", "TaskArrowAttach2", "TaskArrowHide", "TaskArrowModeChange"

        , "TaskEnable", "TaskInteractive", "TaskBlockInteractive"

        , "TaskMusicSetVolume"

        , "TaskNodeAlphaTo", "TaskNodeColorTo", "TaskNodeScaleTo", "TaskNodeRotateTo", "TaskNodeMoveTo", "TaskNodeAccelerateTo", "TaskNodeBezier2To", "TaskNodeBezier2Follow", "TaskNodeBezier3To", "TaskNodeParabolaTo", "TaskNodeVelocityTo", "TaskNodeFollowTo", "TaskNodeFollowToWorld", "TaskNodeLocalHide", "TaskNodeEnable", "TaskNodeFlip", "TaskNodeEnable", "TaskNodeEnableGlobalMouseEvent", "TaskNodeAddChild", "TaskNodeSetPosition", "TaskNodeSetOrigin", "TaskNodePercentVisibilityTo", "TaskNodeDestroy",
        "TaskNodeRemoveFromParent"

        , "TaskNodeMovieEvent"

        , "TaskInterpolatorLinearFloat"

        , "TaskSurfaceAnimationPlay"

        , "TaskAnimatablePlay", "TaskAnimatableStop", "TaskAnimatablePause", "TaskAnimatableEnd", "TaskAnimatableInterrupt", "TaskAnimatableRewind"

        , "TaskObjectAnimatablePlay", "TaskObjectAnimatableStop", "TaskObjectAnimatablePause", "TaskObjectAnimatableEnd", "TaskObjectAnimatableInterrupt"

        , "TaskObjectPlay"

        , "TaskMovieSlotAddChild", "TaskMovieSlotAddObject", "TaskMovieStop", "TaskMoviePlay", "TaskSubMoviePlay", "TaskSubMovie2Play", "TaskMoviePause", "TaskMovieEnd", "TaskMovieLastFrame", "TaskMovieSocketClick", "TaskMovieSocketEnter", "TaskMovieSocketLeave", "TaskMovieSocketMove", "TaskMovieSocketEnable", "TaskMovieRewind", "TaskMovieInterrupt"

        , "TaskMovie2Stop", "TaskMovie2Play", "TaskMovie2Pause", "TaskMovie2End", "TaskMovie2Rewind", "TaskMovie2Interrupt", "TaskMovie2SocketClick", "TaskMovie2SocketEnter", "TaskMovie2SocketLeave", "TaskMovie2SocketMove"

        , "TaskNodeSocketClick", "TaskNodeSocketEnter", "TaskNodeSocketLeave", "TaskNodeSocketMove"

        , "TaskAnimationPlay", "TaskAnimationStop", "TaskAnimationSetFrame", "TaskAnimationSetSequence", "TaskAnimationEnd"

        , "TaskVideoPlay", "TaskVideoStop", "TaskVideoEnd"

        , "TaskSoundEffect", "TaskVoicePlay"

        , "TaskShift", "TaskShiftNext", "TaskPuffShowElement", "TaskCheckBox", "TaskCheckBoxBlockState"

        , "TaskMovieCheckBox", "TaskMovie2CheckBox"

        , "TaskInteraction"

        , "TaskTransition", "TaskTransitionClick", "TaskTransitionEnter", "TaskTransitionLeave", "TaskTransitionBlock", "TaskTransitionUnblock"

        , "TaskSocketClick", "TaskSocketClickUp", "TaskSocketClickEndUp", "TaskSocketEnter", "TaskSocketLeave"

        , "TaskSocketUse"  # click socket with any object, don't remove attach

        , "TaskButtonClick", "TaskButtonClickEndUp", "TaskButtonEnter", "TaskButtonLeave", "TaskButtonBlockState", "TaskButtonSetState", "TaskButtonChangeState", "TaskButtonUse", "TaskButtonBlockKeys", "TaskButtonSwitchMode"

        , "TaskObjectSetPosition", "TaskObjectSetAlpha", "TaskObjectSetScale"

        , "TaskObjectReturn", "TaskObjectActivate", "TaskObjectDeactivate", "TaskObjectDestroy"

        , "TaskZoomOpen", "TaskZoomInit", "TaskZoomEnter", "TaskZoomLeave", "TaskZoomEmpty", "TaskZoomLeave", "TaskZoomClose", "TaskZoomClick", "TaskZoomInterrupt"

        , "TaskTextSetTextID", "TaskObjectTextSetMaxVisibleChar"

        , "TaskTrigger"

        , "TaskStates", "TaskKeyPress"

        , "TaskGameSceneInit"

        , "TaskCursorClickEmulate", "TaskCursorSetPosition"

        , "TaskScenePlusInit", "TaskScenePlusEnter"

        , "TaskMovieButtonClick", "TaskMovieButtonClickEnd", "TaskMovieButtonPressed", "TaskMovieButtonEnter", "TaskMovieButtonLeave", "TaskMovieButtonUse"

        , "TaskMovie2ButtonClick", "TaskMovie2ButtonEnter", "TaskMovie2ButtonLeave"

        , "TaskSemaphore", 'TaskSemaphoreIncrement', "TaskRefcount"

        , "TaskMovieSocketSwipe"

        , "TaskPrefetchGroup", "TaskUnfetchGroup", "TaskSendAnalytics", "TaskSendAnalyticsScreenView", 'TaskFacebookPostMessage', 'TaskFacebookGetData', 'TaskFacebookAuthentication', 'TaskDownloadAsset', 'TaskMountPak', 'TaskSpinnerCheck', 'TaskLoadVersionFiles', 'TaskGetVersion', 'TaskGetFtp', 'TaskLoadPaks', 'TaskNodeLoopedRotate'

        , "TaskHeaderData", "TaskHeaderDataPlayfab", "TaskVirtualAreaScroll"

        , "TaskMovie2LayerAlphaTo"]

    from TaskManager import TaskManager
    TaskManager.importTasks("GOAP2.Task", tasks)

    aliases = ["AliasTextPlay", "AliasTextPlay2"

        , "AliasObjectMoveTo", "AliasObjectScaleTo", "AliasObjectAlphaTo", "AliasMovie2AlphaTo", "AliasObjectRotateTo", "AliasObjectPercentVisibilityTo", "AliasObjectBezier2To", "AliasObjectBezier2Follow"

        , "AliasNodeTranslateTo"

        , "AliasMakeMovieAndPlayOnce", "AliasMakeTriggerAndWait"

        , "AliasShowAdvert"]

    from TaskManager import TaskManager
    TaskManager.importTasks("GOAP2.Alias", aliases)

    policies = ["PolicyPurchaseDummy", "PolicyPurchaseGoogleBilling", "PolicyPurchaseAppleInApp", "PolicyExternalAchieveProgressAppleGameCenter", "PolicyExternalAchieveProgressGooglePlay"]

    from TaskManager import TaskManager
    TaskManager.importTasks("GOAP2.Policy", policies)

    traces = ["TaskInventoryAddCountItem", "TaskInventoryRemoveItem", "TaskNodeTranslateTo", "AliasObjectAlphaTo", "AliasMovie2AlphaTo", "TaskChainCancel", "TaskManager", "TaskChain", "TaskListener", "AliasNodeTranslateTo", "TaskInventoryFindItem", "TaskInventoryFindCountItem", "InventoryCountItem", "ObjectInventory", "InventoryItem", "Inventory", "Actor", "BaseEntity", "BaseObject", "Object", "Manager", "Movie", "Movie2", "HOG", "MixinObjectTemplate", "Utils", "Task", "Policy", "Group", "SceneManager",
        "Notification", "Main", "Transition", "Item", "HOGInventory", "ArrowManager", "ObjectManager", "GroupManager", "TaskSceneLayerGroupEnable", "Button", "HintAction", "AliasTransition", "System", "Entity", "Command", "MovieButton", "Movie2Button", "Provider"]

    from TraceManager import TraceManager
    TraceManager.addTraces(traces)

    from GOAP2.Notificator import Notificator
    import Trace

    Menge.addGlobalModule("Notificator", Notificator)

    notifiers = [#    Notificator.onSave
        "onResume", "onCommandLayerEnable", "onSetCurrentChapter"

        , "onSelectAccount", "onUnselectAccount", "onCreateDefaultAccount", "onLoadAccounts", "onLoadSession", "onDeleteAccount"

        , "onCustomCursor"

        , "onTaskRun", "onTaskComplete"

        , "onScenePreparation", "onSceneInit", "onSceneRestartBegin", "onSceneRestartEnd", "onSceneEnter", "onSceneLeave", "onSceneRemoved", "onSceneChange"

        , "onSceneActivate", "onSceneDeactivate"

        , "onInteractionMouseLeave", "onInteractionMouseEnter", "onInteractionClickBegin", "onInteractionClick", "onInteractionClickUpBegin", "onInteractionClickUp", "onInteractionClickEnd", "onInteractionClickEndUp"

        , "InventoryItemTaken"

        , "onItemClickBegin", "onItemClick", "onItemClickEnd", "onItemMouseEnter", "onItemMouseLeave"

        , "onSocketClickBegin", "onSocketClick", "onSocketSoundClick", "onSocketClickUpBegin", "onSocketClickUp", "onSocketClickEnd", "onSocketClickEndUp", "onSocketMouseEnter", "onSocketSoundEnter", "onSocketMouseLeave"

        , "onTransition", "onTransitionClickBegin", "onTransitionClick", "onTransitionChangeScene", "onTransitionHOGMouseEnter", "onTransitionHOGMouseLeave", "onTransitionUpMouseEnter", "onTransitionUpMouseLeave", "onTransitionBackMouseEnter", "onTransitionBackMouseLeave", "onTransitionLeftMouseEnter", "onTransitionUpLeftMouseEnter", "onTransitionUpLeftMouseLeave", "onTransitionLeftMouseLeave", "onTransitionRightMouseEnter", "onTransitionUpRightMouseEnter", "onTransitionRightMouseLeave",
        "onTransitionUpRightMouseLeave", "onTransitionPuzzleMouseEnter", "onTransitionPuzzleMouseLeave", "onTransitionMouseEnter", "onTransitionMouseLeave", "onTransitionBegin", "onTransitionEnd", "onTransitionUseBegin", "onTransitionUse", "onTransitionBlock", "onTransitionEnable"

        , "onGameBlock", "onBlockKeyBoard"

        , "onZoomInit", "onZoomEnter", "onZoomLeave", "onZoomEmpty", "onZoomClose", "onZoomForceClose", "onZoomForceOpen", "onZoomMouseEnter", "onZoomMouseLeave", "onZoomOpen", "onZoomClickBegin", "onZoomClick", "onZoomClickEnd", "onZoomUseBegin", "onZoomUse", "onZoomUseEnd", "onZoomBlockClose", "onZoomEnable"

        , "onButtonMouseLeave", "onButtonMouseEnter", "onButtonClickBegin", "onButtonClick", "onButtonClickUp", "onButtonClickEnd", "onButtonClickEndUp", "onButtonSoundClick", "onButtonSoundEnter", "onButtonSwitchOn", "onButtonSwitchOff"

        , "onMovieButtonPush", "onMovieButtonRelease", "onMovieButtonClick", "onMovieButtonClickEnd", "onMovieButtonPressed", "onMovieButtonMouseEnter", "onMovieButtonMouseLeave"

        , "onMovie2ButtonMouseEnter", "onMovie2ButtonMouseLeave", "onMovie2ButtonPush", "onMovie2ButtonPressed", "onMovie2ButtonRelease", "onMovie2ButtonClick", "onMovie2ButtonClickEnd"

        , "onArrowPreparation", "onArrowActivate", "onArrowDeactivate", "onArrowAttach", "onArrowDeattach"

        , "onLayerGroupPreparation", "onLayerGroupEnableBegin", "onLayerGroupEnable", "onLayerGroupRelease", "onLayerGroupDisable"

        , "TaskAliasRun", "TaskAliasEnd"

        , "onStageInit", "onStageLoad", "onStageSave", "onStageRun", "onStageResume", "onStageInvalidLoad"

        , "onCompleteStage"

        , "onStateChange", "onSlider", "onCheckBox", "onMovieCheckBox", "onMovie2CheckBox"

        , "onAnimatableEnd", "onAnimationEnd", "onVideoEnd"

        , "onParagraphRun", "onParagraphComplete"

        , "onObjectEnable", "onObjectDisable"

        , "onTimingFactor"

        , "onKeyEvent", "onKeyEventEnd", "onKeyEvent2", "onKeyEvent2End", "onTextEvent"

        , "onRun", "onInterruption", "onStop", "onAccountFinalize", "onFinalize", "onFocus", "onAppMouseEnter", "onAppMouseLeave", "onInitializeRenderResources", "onFinalizeRenderResources", "onRenderViewportChange", "onGameViewportChange"

        , "onZoomBlockOpen", "onTransitionBlockOpen"

        , "onSliderUp", "onSliderDown"

        , "onButtonEnter"

        , "onSwitchChainsClick", "onCursorMode"

        , "onFullscreen", "onMute", "onMusicVolume", "onSoundVolume", "onVoiceVolume"

        , "EditBoxEmpty", "EditBoxChange", "EditBoxFocus", "EditBoxUnhold", "EditBoxKeyEvent", "onFixedContentResolution", "onFixedDisplayResolution"

        , "onMouseMove", "onMouseButtonEventBegin", "onMouseButtonEvent", "onMouseButtonEvent2", "onMouseButtonEventEnd"

        , "onChargerRun", "onChargerRelease", "onChargerCharge", "onChargerSkip", "onChargerReload"

        , "onNodeSocketClickSuccessful"

        , "onMovieSocketEnter", "onMovieSocketLeave", "onMovieSocketClick", "onMovieSocketClickSuccessful", "onMovieSocketMove", "onMovieLoop"

        , "onSessionNew", "onSessionSave", "onSessionLoad", "onSessionLoadComplete", "onSessionLoadInvalid", "onSessionRemove", "onSessionRemoveComplete"

        , "onProgressBarUpdate"

        , "onMovieEditBoxFocus", "MovieEditBoxKeyEvent"

        , "MovieEditBoxEmpty", "MovieEditBoxChange"

        , "onMovie2EditBoxFocus", "onMovie2EditBoxFocusLost", "onMovie2EditBoxKeyEvent"

        , "onMovie2EditBoxEmpty", "onMovie2EditBoxChange"

        , 'PlanetEnter', 'PlanetLeave', 'PlanetDefeat', 'MonsterFight', 'MonsterDead', 'TestConsoleOpen', 'DungeonPlotTwistTextId', 'WarpGateTextId', 'onTabGroupSelect'

        , 'onCombatSpinnerChange', 'onCombatSpinnerDamageTarget', 'onCombatSpinnerAddAbility', 'onCombatSpinnerEndState'

        , 'onCombatSpinnerEventDamageTarget', 'onFacebookAuthEscape', 'onLoadedVersionFiles', 'onSpinnerStop', 'onCreateGlobalAccount', 'onLoadingVersionMessage'

        , 'onStageTimePassed'

        , 'onPrefetchGroupsTaggedBegin', 'onPrefetchGroupsTaggedComplete', 'onPrefetchGroupsTaggedFinished', 'onHintActionItemCollectEnd', 'onInventoryRise'

        , 'onTaskGuardUpdate'

        , 'onMobileKeyboardShow', 'onEditboxSetActive'

        , 'onAttachedArrow'

        , 'onEnableSceneLayerGroup', 'onDisableSceneLayerGroup', 'onGameSceneChange'

        , 'onAdvertLoadSuccess', 'onAdvertLoadFail', 'onAdvertDisplayed', 'onAdvertDisplayFailed', 'onAdvertCompleted', 'onAdvertClicked', 'onAdvertRewarded', 'onAdvertHidden'

        , "oniOSApplicationDidEnterBackground", "oniOSApplicationDidBecomeActive", "oniOSApplicationWillEnterForeground", "oniOSApplicationWillResignActive", "oniOSApplicationWillTerminate"

        , "onAndroidActivityResumed", "onAndroidActivityPaused", "onAndroidActivityStarted", "onAndroidActivityStopped", "onAndroidActivityDestroyed", "onAndroidActivityCreated", "onAndroidActivitySaveInstanceState"

        , "onAvailableAdsEnded", "onAvailableAdsNew"

        , "onUpdateGoldBalance", "onUpdateEnergyBalance", "onGameStoreNotEnoughGold", "onGameStorePayGoldSuccess", "onGameStorePayGoldFailed", "onGameStoreSentRewards"

        , "onPaySuccess", "onPayFailed", "onProductsUpdate", "onProductsUpdateDone"

    ]

    Notificator.addIdentities(notifiers)

    from ObjectManager import ObjectManager
    from EntityManager import EntityManager

    Types = ["Animation", "Interaction", "Button", "CheckBox", "EditBox", "Fade", "Group", "Movie", "Movie2", "Point", "Puff", "Shift", "Slider", "Socket", "Sprite", "Switch", "States", "Text", "Transition", "TransitionBack", "Video", "Window", "Zoom", "Viewport"]

    if Menge.getGameParamBool("NotUseDefaultEntitiesList", False) is True:
        Types = []
        from GOAP2.DatabaseManager import DatabaseManager
        records = DatabaseManager.getDatabaseRecordsFilterBy("Database", "Entities", Module="GOAP2")

        for record in records:
            Types.append(record.get("Type"))

    ObjectManager.importObjects("GOAP2.Object", Types)
    EntityManager.importEntities("GOAP2.Entities", Types)

    EntityManager.importEntity("GOAP2.Entities", "Landscape2D")
    ObjectManager.importObject("GOAP2.Entities.Landscape2D", "Landscape2D")

    EntityManager.importEntity("GOAP2.Entities", "MovieButton")
    ObjectManager.importObject("GOAP2.Entities.MovieButton", "MovieButton")

    EntityManager.importEntity("GOAP2.Entities", "Movie2Button")
    ObjectManager.importObject("GOAP2.Entities.Movie2Button", "Movie2Button")

    EntityManager.importEntity("GOAP2.Entities", "ProgressBar")
    ObjectManager.importObject("GOAP2.Entities.ProgressBar", "ProgressBar")

    EntityManager.importEntity("GOAP2.Entities", "MovieCheckBox")
    ObjectManager.importObject("GOAP2.Entities.MovieCheckBox", "MovieCheckBox")

    EntityManager.importEntity("GOAP2.Entities", "Movie2CheckBox")
    ObjectManager.importObject("GOAP2.Entities.Movie2CheckBox", "Movie2CheckBox")

    ObjectManager.importObject("GOAP2.Entities.Charger", "Charger")
    EntityManager.importEntity("GOAP2.Entities", "Charger")

    EntityManager.importEntity("GOAP2.Entities", "MovieVirtualArea")
    ObjectManager.importObject("GOAP2.Entities.MovieVirtualArea", "MovieVirtualArea")

    EntityManager.importEntity("GOAP2.Entities", "MovieScrollbar")
    ObjectManager.importObject("GOAP2.Entities.MovieScrollbar", "MovieScrollbar")

    EntityManager.importEntity("GOAP2.Entities", "Movie2Scrollbar")
    ObjectManager.importObject("GOAP2.Entities.Movie2Scrollbar", "Movie2Scrollbar")

    EntityManager.importEntity("GOAP2.Entities", "MovieProgressBar")
    ObjectManager.importObject("GOAP2.Entities.MovieProgressBar", "MovieProgressBar")

    EntityManager.importEntity("GOAP2.Entities", "Movie2ProgressBar")
    ObjectManager.importObject("GOAP2.Entities.Movie2ProgressBar", "Movie2ProgressBar")

    EntityManager.importEntity("GOAP2.Entities", "MovieEditBox")
    ObjectManager.importObject("GOAP2.Entities.MovieEditBox", "MovieEditBox")

    EntityManager.importEntity("GOAP2.Entities", "Movie2EditBox")
    ObjectManager.importObject("GOAP2.Entities.Movie2EditBox", "Movie2EditBox")

    EntityManager.importEntity("GOAP2.Entities", "MovieTabsGroup")
    ObjectManager.importObject("GOAP2.Entities.MovieTabsGroup", "MovieTabsGroup")

    if _DEVELOPMENT is True:
        from GOAP2.Providers.AdvertisementProvider import AdvertisementProvider
        AdvertisementProvider.setDevProvider()

    Trace.msg("GOAP2.onInitialize")

    from GOAP2.DatabaseManager import DatabaseManager
    DatabaseManager.onInitialize()

    from GOAP2.ArrowManager import ArrowManager
    ArrowManager.onInitialize()

    from GOAP2.SceneManager import SceneManager
    SceneManager.onInitialize()

    from GOAP2.GroupManager import GroupManager
    GroupManager.onInitialize()

    from GOAP2.Business.ContractManager import ContractManager
    ContractManager.onInitialize()

    from GOAP2.Business.BankManager import BankManager
    BankManager.onInitialize()

    from GOAP2.PrefetchResourceManager import PrefetchResourceManager
    PrefetchResourceManager.onInitialize()

    from GOAP2.PrefetchGroupManager import PrefetchGroupManager
    PrefetchGroupManager.onInitialize()

    from GOAP2.PrefetchGroupNotifyManager import PrefetchGroupNotifyManager
    PrefetchGroupNotifyManager.onInitialize()

    from GOAP2.SessionManager import SessionManager
    SessionManager.onInitialize()

    return True
    pass

def onFinalize():
    Trace.msg("GOAP2.onFinalize")

    from GOAP2.SessionManager import SessionManager
    SessionManager.onFinalize()

    from GOAP2.Business.ContractManager import ContractManager
    ContractManager.onFinalize()

    from GOAP2.Business.BankManager import BankManager
    BankManager.onFinalize()

    from GOAP2.TaskManager import TaskManager
    TaskManager.onFinalize()

    from GOAP2.ArrowManager import ArrowManager
    ArrowManager.onFinalize()

    from GOAP2.SystemManager import SystemManager
    SystemManager.onFinalize()

    from GOAP2.EntityManager import EntityManager
    EntityManager.onFinalize()

    from GOAP2.SceneManager import SceneManager
    SceneManager.onFinalize()

    from GOAP2.GroupManager import GroupManager
    GroupManager.onFinalize()

    from GOAP2.DemonManager import DemonManager
    DemonManager.onFinalize()

    from GOAP2.StateManager import StateManager
    StateManager.onFinalize()

    from GOAP2.DefaultManager import DefaultManager
    DefaultManager.onFinalize()

    from GOAP2.PrefetchGroupManager import PrefetchGroupManager
    PrefetchGroupManager.onFinalize()

    from GOAP2.PrefetchResourceManager import PrefetchResourceManager
    PrefetchResourceManager.onFinalize()

    from GOAP2.DatabaseManager import DatabaseManager
    DatabaseManager.onFinalize()

    from Notification import Notification
    Notification.onFinalize()
    pass