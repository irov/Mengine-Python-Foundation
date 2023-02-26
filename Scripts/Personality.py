# coding=utf-8
import sys

from Foundation.AccountManager import AccountManager
from Foundation.Bootstrapper import Bootstrapper
from Foundation.DefaultManager import DefaultManager
from Foundation.GameManager import GameManager
from Foundation.StateManager import StateManager
from Notification import Notification

sys.setrecursionlimit(500)

exception_array = {Menge.KC_TAB, Menge.KC_OEM_4, Menge.KC_OEM_6, Menge.KC_F1, Menge.KC_F2, Menge.KC_F3, Menge.KC_F4, Menge.KC_F5, Menge.KC_F6, Menge.KC_F7, Menge.KC_F, Menge.KC_F9, Menge.KC_F10, Menge.KC_F11, Menge.KC_F12}

def onPreparation(isDebug):
    return True

def onFocus(value):
    Notification.notify(Notificator.onFocus, value)

def onAppMouseEnter(event):
    Notification.notify(Notificator.onAppMouseEnter, event)

def onAppMouseLeave(event):
    Notification.notify(Notificator.onAppMouseLeave, event)

def onInitialize(*args):
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

    print
    "==========================================="
    print
    "----------------RUN SYSTEMS----------------"
    print
    "==========================================="
    if Bootstrapper.loadSystems("Database", "Systems") is False:
        return False
        pass

    arrow = Menge.getArrow()

    if Menge.hasTouchpad() is True:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultMobileArrowRadius", 15.0)
    else:
        DefaultArrowRadius = DefaultManager.getDefaultFloat("DefaultArrowRadius", 10.0)

    arrow.node.setRadius(DefaultArrowRadius)

    # setup build version text for production user
    build_alias_id, build_text_id = "$AliasBuildVersion", "ID_TEXT_BUILD_VERSION"
    if Menge.existText(build_text_id) is True:
        Menge.setTextAlias("", build_alias_id, build_text_id)
        if Menge.getGameParamBool("ShowBuildVersion", True) is True:
            Menge.setTextAliasArguments("", build_alias_id, _BUILD_VERSION)
        else:
            Menge.setTextAliasArguments("", build_alias_id, "")

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
    param = Menge.getGameParamUnicode("SurveyUrl")
    SurveyLink = Menge.getGameParamBool("SurveyLink", False)

    def isSurvey():
        """ copy from Foundation.Utils (cause crash if we import this method) """
        if Menge.getGameParamUnicode("BuildModeCheckVersion") == u"2.0":
            return Menge.getGameParamUnicode("BuildMode") == u"Survey"
        else:
            return Menge.getGameParamBool("Survey", False)

    if SurveyLink is True and isSurvey() is True:
        Menge.openUrlInDefaultBrowser(param)

    Notification.notify(Notificator.onFinalize)

    Bootstrapper.shutdown()

def onDestroy():
    pass

def onHandleKeyEvent(event):
    if not Menge.hasOption('cheats'):
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
    if Menge.hasCurrentAccountSetting("Fullscreen") is True:
        Menge.changeCurrentAccountSetting("Fullscreen", unicode(fullscreen))
    Notification.notify(Notificator.onFullscreen, fullscreen)

def onFixedContentResolution(widescreen):
    if Menge.hasCurrentAccountSetting("Widescreen") is True:
        Menge.changeCurrentAccountSetting("Widescreen", unicode(widescreen))
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

def changeTutorial(value):
    Notification.notify(Notificator.onTutorialChange, value)

def onInitializeRenderResources():
    Notification.notify(Notificator.onInitializeRenderResources)

def onFinalizeRenderResources():
    Notification.notify(Notificator.onFinalizeRenderResources)

def onCreateAccount(accountID, isGlobal):
    AccountManager.callCreateAccount(accountID, isGlobal)

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

def oniOSApplicationDidEnterBackground():
    # ios app is now in the background
    if _DEVELOPMENT is True:
        print("oniOSApplicationDidEnterBackground -- app is now in the background")
    Notification.notify(Notificator.oniOSApplicationDidEnterBackground)

def oniOSApplicationDidBecomeActive():
    # ios app has become active
    if _DEVELOPMENT is True:
        print("oniOSApplicationDidBecomeActive -- app has become active")
    Notification.notify(Notificator.oniOSApplicationDidBecomeActive)

def oniOSApplicationWillEnterForeground():
    # ios app is about to enter the foreground
    if _DEVELOPMENT is True:
        print("oniOSApplicationWillEnterForeground -- app is about to enter the foreground")
    Notification.notify(Notificator.oniOSApplicationWillEnterForeground)

def oniOSApplicationWillResignActive():
    # ios app is about to become inactive
    if _DEVELOPMENT is True:
        print("oniOSApplicationWillResignActive -- app is about to become inactive")
    Notification.notify(Notificator.oniOSApplicationWillResignActive)

def oniOSApplicationWillTerminate():
    # ios app is about to terminate
    if _DEVELOPMENT is True:
        print("oniOSApplicationWillTerminate -- app is about to terminate")
    Notification.notify(Notificator.oniOSApplicationWillTerminate)