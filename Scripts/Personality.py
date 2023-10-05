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
        , "onTimingFactor"
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

        , "oniOSApplicationDidEnterBackground"
        , "oniOSApplicationDidBecomeActive"
        , "oniOSApplicationWillEnterForeground"
        , "oniOSApplicationWillResignActive"
        , "oniOSApplicationWillTerminate"

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

    arrow = Mengine.getArrow()

    if Mengine.hasTouchpad() is True:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultMobileArrowRadius", 15.0)
    else:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultArrowRadius", 10.0)

    arrow.node.setRadius(DefaultArrowRadius)

    # setup build version text for production user
    build_alias_id, build_text_id = "$AliasBuildVersion", "ID_TEXT_BUILD_VERSION"
    if Mengine.existText(build_text_id) is True:
        Mengine.setTextAlias("", build_alias_id, build_text_id)
        if Mengine.getGameParamBool("ShowBuildVersion", True) is True:
            Mengine.setTextAliasArguments("", build_alias_id, _BUILD_VERSION)
        else:
            Mengine.setTextAliasArguments("", build_alias_id, "")

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
    if not Mengine.hasOption('cheats'):
        return False

    if GameManager.isBlockKeyboard() is True:
        if event.code not in exception_array:
            return False

    Notification.notify(Notificator.onKeyEvent, event.code, event.x, event.y, event.isDown, event.isRepeat)
    Notification.notify(Notificator.onKeyEventEnd, event.code, event.x, event.y, event.isDown, event.isRepeat)

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

def onTimeFactor(factor):
    Notification.notify(Notificator.onTimingFactor, factor)

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

# ios app is now in the background
def oniOSApplicationDidEnterBackground():
    Notification.notify(Notificator.oniOSApplicationDidEnterBackground)

# ios app has become active
def oniOSApplicationDidBecomeActive():
    Notification.notify(Notificator.oniOSApplicationDidBecomeActive)

# ios app is about to enter the foreground
def oniOSApplicationWillEnterForeground():
    Notification.notify(Notificator.oniOSApplicationWillEnterForeground)

# ios app is about to become inactive
def oniOSApplicationWillResignActive():
    Notification.notify(Notificator.oniOSApplicationWillResignActive)

# ios app is about to terminate
def oniOSApplicationWillTerminate():
    Notification.notify(Notificator.oniOSApplicationWillTerminate)

def onAnalyticsEvent(name, timestamp, params):
    Notification.notify(Notificator.onAnalyticsEvent, name, timestamp, params)
    pass

