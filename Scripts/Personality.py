import sys

from Notification import Notification

from Foundation.AccountManager import AccountManager
from Foundation.Bootstrapper import Bootstrapper
from Foundation.DefaultManager import DefaultManager
from Foundation.GameManager import GameManager
from Foundation.StateManager import StateManager
from Foundation.Notificator import Notificator

sys.setrecursionlimit(500)

exception_array = {Mengine.KC_TAB, Mengine.KC_OEM_4, Mengine.KC_OEM_6, Mengine.KC_F1, Mengine.KC_F2, Mengine.KC_F3, Mengine.KC_F4, Mengine.KC_F5, Mengine.KC_F6, Mengine.KC_F7, Mengine.KC_F, Mengine.KC_F9, Mengine.KC_F10, Mengine.KC_F11, Mengine.KC_F12}

def onPreparation(isDebug):
    from Foundation.Notificator import Notificator
    Mengine.addGlobalModule("Notificator", Notificator)

    notifiers = [
        "onFocus"
        , "onAppMouseEnter"
        , "onAppMouseLeave"
        , "onRun"
        , "onInterruption"
        , "onStop"
        , "onAccountFinalize"
        , "onFinalize"

        , "onKeyEvent"
        , "onKeyEventEnd"
        , "onTextEvent"
        , "onMouseMove"
        , "onMouseButtonEventBegin"
        , "onMouseButtonEvent"
        , "onMouseButtonEventEnd"
        , "onTimeFactorChange"
        , "onSettingChange"
        , "onFullscreen"
        , "onFixedContentResolution"
        , "onCursorMode"
        , "onSelectAccount"
        , "onRenderViewportChange"
        , "onGameViewportChange"
        , "onUnselectAccount"
        , "onDeleteAccount"
        , "onInitializeRenderResources"
        , "onFinalizeRenderResources"
        , "onCreateAccout"
        , "onCreateDefaultAccount"
        , "onCreateGlobalAccount"
        , "onLoadAccounts"
        , "onMute"
        , "onSoundVolume"
        , "onMusicVolume"
        , "onVoiceVolume"
        , "onUserEvent"

        , "onApplicationDidEnterBackground"
        , "onApplicationDidBecomeActive"
        , "onApplicationWillEnterForeground"
        , "onApplicationWillResignActive"
        , "onApplicationWillTerminate"

        , "onAnalyticsEvent"
    ]

    Notificator.addIdentities(notifiers)

    return True

def onFocus(value):
    Notification.notify(Notificator.onFocus, value)

def onAppMouseEnter(event):
    Notification.notify(Notificator.onAppMouseEnter, event)

def onAppMouseLeave(event):
    Notification.notify(Notificator.onAppMouseLeave, event)

def onInitialize():
    StateManager.addState("AliasMessageShow", False)
    StateManager.addState("StateHintReady", True)
    StateManager.addState("StateHintCharge", False)
    StateManager.addState("StateHintEmpty", False)
    StateManager.addState("StateInventory", "INVENTORY_DOWN")

    if Bootstrapper.loadManagers("Database", "Managers") is False:
        Trace.log("Manager", 0, "Personality.onInitialize: bootstrapper invalid load managers")
        return False
        pass

    from TraceManager import TraceManager

    TraceManager.setLevel("TaskInventoryAddCountItem", 3)
    TraceManager.setLevel("TaskInventoryReturnItem", 3)
    TraceManager.setLevel("AliasObjectAlphaTo", 3)
    TraceManager.setLevel("AliasMovie2AlphaTo", 3)
    TraceManager.setLevel("TaskChainCancel", 3)
    TraceManager.setLevel("TaskChain", 0)
    TraceManager.setLevel("Task", 0)
    TraceManager.setLevel("TaskListener", 0)
    TraceManager.setLevel("TaskNodeTranslateTo", 0)
    TraceManager.setLevel("InventoryItem", 0)
    TraceManager.setLevel("InventoryCountItem", 3)
    TraceManager.setLevel("BaseEntity", 0)
    TraceManager.setLevel("Object", 3)
    TraceManager.setLevel("ObjectInventory", 3)
    TraceManager.setLevel("Inventory", 0)
    TraceManager.setLevel("Movie", 3)
    TraceManager.setLevel("HOG", 3)
    TraceManager.setLevel("MixinObjectTemplate", 3)
    TraceManager.setLevel("Manager", 3)
    TraceManager.setLevel("Group", 0)
    TraceManager.setLevel("SceneManager", 0)
    TraceManager.setLevel("TaskManager", 0)
    TraceManager.setLevel("Notification", 0)
    TraceManager.setLevel("Main", 0)
    TraceManager.setLevel("Transition", 0)
    TraceManager.setLevel("Item", 0)
    TraceManager.setLevel("Scenario", 0)
    TraceManager.setLevel("MacroCommand", 0)

    if Bootstrapper.loadSystems("Database", "Systems") is False:
        return False
        pass

    if Mengine.hasTouchpad() is True:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultMobileArrowRadius", 15.0)
    else:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultArrowRadius", 10.0)

    arrow = Mengine.getArrow()
    arrow.setRadius(DefaultArrowRadius)

    # setup build version text for production user
    build_alias_id, build_text_id = "$AliasBuildVersion", "ID_TEXT_BUILD_VERSION"
    if Mengine.existText(build_text_id) is True:
        build_version = ""

        # show all info for debug
        if _DEBUG is True or _DEVELOPMENT is True:
            build_version += "{} ({}) [{}]".format(_BUILD_VERSION, _BUILD_NUMBER, _ENGINE_GITSHA1[:6])
        # else only if parameter is set
        elif Mengine.getGameParamBool("ShowBuildVersion", True) is True:
            build_version += "{}".format(_BUILD_VERSION)

            if Mengine.getGameParamBool("ShowBuildVersionExt", True) is True:
                build_version += " ({}) [{}]".format(_BUILD_NUMBER, _ENGINE_GITSHA1[:6])

        # add build type info
        if _DEBUG is True or _DEVELOPMENT is True:
            build_version += " dev"

        Mengine.setTextAlias("", build_alias_id, build_text_id)
        Mengine.setTextAliasArguments("", build_alias_id, build_version)

    return True

def onRun():
    Notification.notify(Notificator.onRun)

def onInterruption():
    Notification.notify(Notificator.onInterruption)

def onStop():
    Notification.notify(Notificator.onStop)

def onAccountFinalize():
    Notification.notify(Notificator.onAccountFinalize)

def onFinalize():
    Notification.notify(Notificator.onFinalize)
    Bootstrapper.shutdown()

def onDestroy():
    pass

def onHandleKeyEvent(event):
    if GameManager.isBlockKeyboard() is True:
        if event.code not in exception_array:
            return False

    Notification.notify(Notificator.onKeyEvent, event.code, event.position.world.x, event.position.world.y, event.isDown, event.isRepeat)
    Notification.notify(Notificator.onKeyEventEnd, event.code, event.position.world.x, event.position.world.y, event.isDown, event.isRepeat)
    return False

def onHandleTextEvent(event):
    Notification.notify(Notificator.onTextEvent, event)
    return False

def onHandleMouseButtonEventBegin(event):
    Notification.notify(Notificator.onMouseButtonEventBegin, event)
    return False

def onHandleMouseButtonEvent(event):
    Notification.notify(Notificator.onMouseButtonEvent, event)
    return False

def onHandleMouseButtonEventEnd(event):
    Notification.notify(Notificator.onMouseButtonEventEnd, event)
    return False

def onTimeFactorChange(factor):
    Notification.notify(Notificator.onTimeFactorChange, factor)

def onSettingChange(setting, key):
    Notification.notify(Notificator.onSettingChange, setting, key)

def onFullscreen(fullscreen):
    if Mengine.hasCurrentAccountSetting("Fullscreen") is True:
        Mengine.changeCurrentAccountSetting("Fullscreen", unicode(fullscreen))
    Notification.notify(Notificator.onFullscreen, fullscreen)

def onFixedContentResolution(widescreen):
    if Mengine.hasCurrentAccountSetting("Widescreen") is True:
        Mengine.changeCurrentAccountSetting("Widescreen", unicode(widescreen))
    Notification.notify(Notificator.onFixedContentResolution, widescreen)

def onCursorMode(mode):
    Notification.notify(Notificator.onCursorMode, mode)

def onSelectAccount(accountID):
    Notification.notify(Notificator.onSelectAccount, accountID)

def onRenderViewport(viewport, contentResolution):
    Notification.notify(Notificator.onRenderViewportChange, viewport, contentResolution)

def onGameViewport(viewport, aspect):
    Notification.notify(Notificator.onGameViewportChange, viewport, aspect)

def onUnselectAccount(accountID):
    Notification.notify(Notificator.onUnselectAccount, accountID)

def onDeleteAccount(accountID):
    Notification.notify(Notificator.onDeleteAccount, accountID)

def onInitializeRenderResources():
    Notification.notify(Notificator.onInitializeRenderResources)

def onFinalizeRenderResources():
    Notification.notify(Notificator.onFinalizeRenderResources)

def onCreateAccount(accountID, isGlobal):
    AccountManager.callCreateAccount(accountID, isGlobal)
    Notification.notify(Notificator.onCreateAccout, accountID, isGlobal)

def onCreateDefaultAccount():
    AccountManager.callCreateDefaultAccount()
    Notification.notify(Notificator.onCreateDefaultAccount)

def onCreateGlobalAccount():
    AccountManager.callCreateGlobalAccount()
    Notification.notify(Notificator.onCreateGlobalAccount)

def onLoadAccounts():
    AccountManager.callLoadAccounts()
    Notification.notify(Notificator.onLoadAccounts)

def onChangeSoundVolume(soundVolume, musicVolume, voiceVolume):
    Notification.notify(Notificator.onSoundVolume, soundVolume)
    Notification.notify(Notificator.onMusicVolume, musicVolume)
    Notification.notify(Notificator.onVoiceVolume, voiceVolume)

def onOverFillrate(fillrate, limit):
    pass

def onUserEvent(event, params):
    Notification.notify(Notificator.onUserEvent, event, params)

# app is now in the background
def onApplicationDidEnterBackground():
    Notification.notify(Notificator.onApplicationDidEnterBackground)

# app has become active
def onApplicationDidBecomeActive():
    Notification.notify(Notificator.onApplicationDidBecomeActive)

# app is about to enter the foreground
def onApplicationWillEnterForeground():
    Notification.notify(Notificator.onApplicationWillEnterForeground)

# app is about to become inactive
def onApplicationWillResignActive():
    Notification.notify(Notificator.onApplicationWillResignActive)

# app is about to terminate
def onApplicationWillTerminate():
    Notification.notify(Notificator.onApplicationWillTerminate)

def onAnalyticsEvent(name, timestamp, params):
    Notification.notify(Notificator.onAnalyticsEvent, name, timestamp, params)
    pass

def onAnalyticsScreenView(screen_type, screen_name):
    pass

def onAnalyticsFlush():
    pass

