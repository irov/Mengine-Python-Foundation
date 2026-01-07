from Event import Event
from Foundation.PolicyManager import PolicyManager
from Foundation.Providers.RatingAppProvider import RatingAppProvider
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from Foundation.Providers.PaymentProvider import PaymentProvider
from Foundation.Providers.ProductsProvider import ProductsProvider
from Foundation.Providers.AuthProvider import AuthProvider
from Foundation.Providers.ConsentProvider import ConsentProvider
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger

_Log = SimpleLogger("SystemGoogleServices")

GOOGLE_GAME_SOCIAL_PLUGIN = "MengineGGameSocial"
GOOGLE_PLAY_BILLING_PLUGIN = "MengineGPlayBilling"
GOOGLE_IN_APP_REVIEWS_PLUGIN = "MengineGInAppReviews"
GOOGLE_CONSENT_PLUGIN = "MengineGConsent"
FIREBASE_CRASHLYTICS_PLUGIN = "MengineFBCrashlytics"

class SystemGoogleServices(System):
    # Google service that provides
    #    - authentication in Google Account
    #    - Billing
    #    - Google Play Social
    #    - InAppReviews

    __lastProductId = None

    b_plugins = {
        GOOGLE_GAME_SOCIAL_PLUGIN: Mengine.isAvailablePlugin(GOOGLE_GAME_SOCIAL_PLUGIN),
        GOOGLE_PLAY_BILLING_PLUGIN: Mengine.isAvailablePlugin(GOOGLE_PLAY_BILLING_PLUGIN),
        GOOGLE_IN_APP_REVIEWS_PLUGIN: Mengine.isAvailablePlugin(GOOGLE_IN_APP_REVIEWS_PLUGIN),
        GOOGLE_CONSENT_PLUGIN: Mengine.isAvailablePlugin(GOOGLE_CONSENT_PLUGIN),
        FIREBASE_CRASHLYTICS_PLUGIN: Mengine.isAvailablePlugin(FIREBASE_CRASHLYTICS_PLUGIN),
    }

    login_event = Event("GoogleGameSocialLoginEvent")
    logout_event = Event("GoogleGameSocialLogoutEvent")
    __on_auth_achievements = {}
    __on_auth_cbs = {}
    sku_response_event = Event("SkuListResponse")   # todo: check is deprecated

    s_products = {}

    def _onInitialize(self):
        if self.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is True:
            def _setCallback(method_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_GAME_SOCIAL_PLUGIN, method_name, *callback)

            # request achievements state
            _setCallback("onGoogleGameSocialRequestAchievementsStateSuccessful", SystemGoogleServices.__cbRequestAchievementsStateSuccessful)
            _setCallback("onGoogleGameSocialRequestAchievementsStateCanceled", SystemGoogleServices.__cbRequestAchievementsStateCanceled)
            _setCallback("onGoogleGameSocialRequestAchievementsStateError", SystemGoogleServices.__cbRequestAchievementsStateError)
            # incrementAchievement:
            _setCallback("onGoogleGameSocialIncrementAchievementSuccess", SystemGoogleServices.__cbAchievementIncSuccess)
            _setCallback("onGoogleGameSocialIncrementAchievementError", SystemGoogleServices.__cbAchievementIncError)
            # unlockAchievement:
            _setCallback("onGoogleGameSocialUnlockAchievementSuccess", SystemGoogleServices.__cbAchievementUnlockSuccess)
            _setCallback("onGoogleGameSocialUnlockAchievementError", SystemGoogleServices.__cbAchievementUnlockError)
            # revealAchievement:
            _setCallback("onGoogleGameSocialRevealAchievementSuccess", SystemGoogleServices.__cbAchievementRevealSuccess)
            _setCallback("onGoogleGameSocialRevealAchievementError", SystemGoogleServices.__cbAchievementRevealError)
            # showAchievements:
            _setCallback("onGoogleGameSocialShowAchievementSuccess", SystemGoogleServices.__cbAchievementShowSuccess)
            _setCallback("onGoogleGameSocialShowAchievementCanceled", SystemGoogleServices.__cbAchievementShowCanceled)
            _setCallback("onGoogleGameSocialShowAchievementError", SystemGoogleServices.__cbAchievementShowError)

            _setCallback("onGoogleGameSocialIncrementEventSuccess", SystemGoogleServices.__cbEventIncrementSuccess)
            _setCallback("onGoogleGameSocialIncrementEventError", SystemGoogleServices.__cbEventIncrementError)


            _setCallback("onGoogleGameSocialLeaderboardScoreSuccess", SystemGoogleServices.__cbLeaderboardScoreSuccess)
            _setCallback("onGoogleGameSocialLeaderboardScoreError", SystemGoogleServices.__cbLeaderboardScoreError)

            AchievementsProvider.setProvider("Google", dict(
                unlockAchievement=SystemGoogleServices.unlockAchievement,
                incrementAchievement=SystemGoogleServices.incrementAchievement,
                showAchievements=SystemGoogleServices.showAchievements,
            ))

            AuthProvider.setProvider("Google", dict(
                login=SystemGoogleServices.signIn,
                logout=SystemGoogleServices.signOut,
                isLoggedIn=SystemGoogleServices.isLoggedIn,
            ))

            PolicyManager.setPolicy("Authorize", "PolicyAuthGoogleService")    # deprecated

            Mengine.waitSemaphore("GoogleGameSocialAuthenticated", self.__cbSignSuccess)

        if self.b_plugins[GOOGLE_PLAY_BILLING_PLUGIN] is True:
            def _setCallback(method_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_PLAY_BILLING_PLUGIN, method_name, *callback)

            # purchase status
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceTimeout", SystemGoogleServices.__cbBillingPurchaseError, "ServiceTimeout")
            _setCallback("onGooglePlayBillingPurchasesUpdatedFeatureNotSupported", SystemGoogleServices.__cbBillingPurchaseError, "FeatureNotSupported")
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceDisconnected", SystemGoogleServices.__cbBillingPurchaseError, "ServiceDisconnected")
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceUnavailable", SystemGoogleServices.__cbBillingPurchaseError, "ServiceUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedBillingUnavailable", SystemGoogleServices.__cbBillingPurchaseError, "BillingUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemUnavailable", SystemGoogleServices.__cbBillingPurchaseError, "ItemUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedDeveloperError", SystemGoogleServices.__cbBillingPurchaseError, "DeveloperError")
            _setCallback("onGooglePlayBillingPurchasesUpdatedError", SystemGoogleServices.__cbBillingPurchaseError, "Error")
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemAlreadyOwned", SystemGoogleServices.__cbBillingPurchaseItemAlreadyOwned)
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemNotOwned", SystemGoogleServices.__cbBillingPurchaseError, "ItemNotOwned")
            _setCallback("onGooglePlayBillingPurchasesUpdatedNetworkError", SystemGoogleServices.__cbBillingPurchaseError, "NetworkError")
            _setCallback("onGooglePlayBillingPurchasesUpdatedUnknown", SystemGoogleServices.__cbBillingPurchaseErrorUnknown)
            _setCallback("onGooglePlayBillingPurchasesUpdatedUserCanceled", SystemGoogleServices.__cbBillingPurchaseError, "UserCanceled")
            _setCallback("onGooglePlayBillingPurchasesUpdatedOk", SystemGoogleServices.__cbBillingPurchaseOk)
            # query products & purchases (for restore)
            _setCallback("onGooglePlayBillingQueryProductSuccess", SystemGoogleServices.__cbBillingQueryProductsSuccess)
            _setCallback("onGooglePlayBillingQueryProductFailed", SystemGoogleServices.__cbBillingQueryProductsFail)
            _setCallback("onGooglePlayBillingQueryProductError", SystemGoogleServices.__cbBillingQueryProductsError)
            _setCallback("onGooglePlayBillingRestorePurchasesSuccess", SystemGoogleServices.__cbBillingRestorePurchasesSuccess)
            _setCallback("onGooglePlayBillingRestorePurchasesFailed", SystemGoogleServices.__cbBillingRestorePurchasesFailed)
            _setCallback("onGooglePlayBillingRestorePurchasesError", SystemGoogleServices.__cbBillingRestorePurchasesError)
            # purchase flow
            _setCallback("onGooglePlayBillingPurchaseUnspecifiedState", SystemGoogleServices.__cbBillingPurchaseUnspecifiedState)
            _setCallback("onGooglePlayBillingPurchaseIsConsumable", SystemGoogleServices.__cbBillingPurchaseIsConsumable)
            _setCallback("onGooglePlayBillingPurchasePending", SystemGoogleServices.__cbBillingPurchasePending)

            _setCallback("onGooglePlayBillingBuyInAppLaunchFlowSuccess", SystemGoogleServices.__cbBillingBuyInAppLaunchFlowSucces)
            _setCallback("onGooglePlayBillingBuyInAppLaunchFlowFailed", SystemGoogleServices.__cbBillingBuyInAppLaunchFlowFailed)
            _setCallback("onGooglePlayBillingBuyInAppLaunchFlowError", SystemGoogleServices.__cbBillingBuyInAppLaunchFlowError)
            #  - consumable
            _setCallback("onGooglePlayBillingPurchasesOnConsumeSuccess", SystemGoogleServices.__cbBillingPurchaseOnConsumeSuccess)
            _setCallback("onGooglePlayBillingPurchasesOnConsumeFailed", SystemGoogleServices.__cbBillingPurchaseOnConsumeFail)
            #  - non-consumable
            _setCallback("onGooglePlayBillingPurchaseAcknowledged", SystemGoogleServices.__cbBillingPurchaseAcknowledged)
            _setCallback("onGooglePlayBillingPurchaseAcknowledgeSuccess", SystemGoogleServices.__cbBillingPurchaseAcknowledgeSuccess)
            _setCallback("onGooglePlayBillingPurchaseAcknowledgeFailed", SystemGoogleServices.__cbBillingPurchaseAcknowledgeFail)

            PaymentProvider.setProvider("Google", dict(
                pay=SystemGoogleServices.buy,
                restorePurchases=SystemGoogleServices.restorePurchases,
                isOwnedInAppProduct=SystemGoogleServices.isOwnedInAppProduct,
            ))

            Mengine.waitSemaphore("GooglePlayBillingReady", SystemGoogleServices.__cbGooglePlayBillingInitialized)

        if self.b_plugins[GOOGLE_IN_APP_REVIEWS_PLUGIN] is True:
            def _setCallback(callback_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_IN_APP_REVIEWS_PLUGIN, callback_name, *callback)

            Mengine.waitSemaphore("GoogleInAppReviewsReady", SystemGoogleServices.__cbGoogleInAppReviewsReady)

            _setCallback("onGoogleInAppReviewsRequestReviewError", SystemGoogleServices.__cbReviewsRequestError)
            _setCallback("onGoogleInAppReviewsLaunchingTheReviewSuccess", SystemGoogleServices.__cbReviewsLaunchingSuccess)
            _setCallback("onGoogleInAppReviewsLaunchingTheReviewError", SystemGoogleServices.__cbReviewsLaunchingError)

            RatingAppProvider.setProvider("Google", dict(rateApp=SystemGoogleServices.rateApp))

        if self.b_plugins[GOOGLE_CONSENT_PLUGIN] is True:
            def _setCallback(method_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_CONSENT_PLUGIN, method_name, *callback)

            _setCallback("onAndroidGoogleConsentFlowCompleted", SystemGoogleServices.__cbConsentFlowCompleted)
            _setCallback("onAndroidGoogleConsentFlowError", SystemGoogleServices.__cbConsentFlowError)

            ConsentProvider.setProvider("GoogleConsent", dict(
                ShowConsentFlow=SystemGoogleServices.showConsentFlow,
                IsConsentFlow=SystemGoogleServices.isConsentFlow,
            ))

        if self.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is True:
            # google do auto login on create app, so we don't need to do it manually here
            if Mengine.getGameParamBool("GoogleAutoLogin", False) is True:
                self.signIn()

        # todo: promocodes handling in onRequestPromoCodeResult

        self.__addDevToDebug()

    def _onFinalize(self):
        self.__remDevToDebug()

    def _onStop(self):
        if TaskManager.existTaskChain("SystemGoogleServices_RetryPurchase") is True:
            TaskManager.cancelTaskChain("SystemGoogleServices_RetryPurchase")
        if TaskManager.existTaskChain("SystemGoogleServices_SignIn") is True:
            TaskManager.cancelTaskChain("SystemGoogleServices_SignIn")

    def _onRun(self):
        self.__setDefaultSaves()

        return True

    def _onSave(self):
        dict_save = {
            "cbs": SystemGoogleServices.__on_auth_cbs,
            "achievements": SystemGoogleServices.__on_auth_achievements
        }
        return dict_save

    def _onLoad(self, dict_save):
        SystemGoogleServices.__on_auth_cbs = dict_save.get("cbs", {})
        SystemGoogleServices.__on_auth_achievements = dict_save.get("achievements", {})

    @staticmethod
    def __setDefaultSaves():
        SystemGoogleServices.__on_auth_cbs = {
            "showAchievements": False,
            "buy": None
        }
        SystemGoogleServices.__on_auth_achievements = {
            "increment": [],
            "unlock": []
        }

    # --- GoogleGameSocial ---------------------------------------------------------------------------------------------

    @staticmethod
    def isLoggedIn():
        authenticated = Mengine.androidBooleanMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "isAuthenticated")
        return authenticated

    @staticmethod
    def signIn(only_intent=False, force=False):
        if SystemGoogleServices.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is False:
            _Log("[Auth] plugin {!r} is not active for signIn".format(GOOGLE_GAME_SOCIAL_PLUGIN))
            return

        if force is False and SystemGoogleServices.isLoggedIn() is True:
            _Log("[Auth] signIn canceled - user already logged in")
            return

        if only_intent is True:
            SystemGoogleServices._signInIntent()
            return

        if TaskManager.existTaskChain("SystemGoogleServices_SignIn"):
            if _DEVELOPMENT:
                _Log("[Auth] SystemGoogleServices_SignIn is already in process...", err=True)
            return

        _Log("[Auth] silence auth success!")

    @staticmethod
    def _signInIntent():
        _Log("[Auth] startSignIn Intent...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "signInIntent")

    @staticmethod
    def signOut():
        if SystemGoogleServices.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is False:
            _Log("[Auth] plugin {!r} is not active for signOut".format(GOOGLE_GAME_SOCIAL_PLUGIN))
            return
        _Log("[Auth] signOut...", force=True)
        #ToDo signOut is not implemented in GoogleGameSocial plugin

    # callbacks

    @staticmethod
    def __cbSignSuccess():
        _Log("[Auth cb] successfully login in")
        SystemGoogleServices.login_event(True)
        Notification.notify(Notificator.onUserLoggedIn)

        SystemGoogleServices.__cbRestoreTasks()

        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "requestAchievementsState")

    @staticmethod
    def __cbNeedIntentSign():
        _Log("[Auth cb] silent login error - call intent login this time", err=True)
        SystemGoogleServices._signInIntent()

    @staticmethod
    def __cbSignOutSuccess():
        SystemGoogleServices.logout_event(True)
        _Log("[Auth cb] logout success", force=True)

    @staticmethod
    def __cbSignOutCanceled():
        SystemGoogleServices.logout_event(False)
        _Log("[Auth cb] logout canceled", force=True)

    @staticmethod
    def __cbSignOutFailure():
        SystemGoogleServices.logout_event(False)
        _Log("[Auth cb] logout failed", err=True, force=True)

    @staticmethod
    def __cbSignOutComplete():
        SystemGoogleServices.logout_event(True)
        Notification.notify(Notificator.onUserLoggedOut)
        _Log("[Auth cb] logout complete", force=True)

    @staticmethod
    def __cbRestoreTasks():
        increment = SystemGoogleServices.__on_auth_achievements.get("increment", [])
        for (achievement_id, steps) in increment:
            SystemGoogleServices.incrementAchievement(achievement_id, steps)

        unlock = SystemGoogleServices.__on_auth_achievements.get("unlock", [])
        for achievement_id in unlock:
            SystemGoogleServices.unlockAchievement(achievement_id)

        if SystemGoogleServices.__on_auth_cbs.get("showAchievements", False) is True:
            SystemGoogleServices.showAchievements()

        product_id = SystemGoogleServices.__on_auth_cbs.get("buy", None)
        if product_id is not None:
            SystemGoogleServices.buy(product_id)

        SystemGoogleServices.__setDefaultSaves()

    # --- GooglePlayBilling --------------------------------------------------------------------------------------------

    @staticmethod
    def __cbGooglePlayBillingInitialized():
        _Log("Start connect to the billing client...")
        consumableIds, nonconsumableIds = ProductsProvider.getQueryProductIds()
        _Log("[Billing] query products consumable: {!r} nonconsumable: {!r}".format(consumableIds, nonconsumableIds))
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "queryProducts", consumableIds, nonconsumableIds)

    @staticmethod
    def buy(product_id):
        _Log("[Billing] buy {!r}".format(product_id))
        SystemGoogleServices.__lastProductId = product_id
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "buyInApp", product_id)

    @staticmethod
    def restorePurchases():
        _Log("[Billing] restore purchases...")
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "restorePurchases")

    @staticmethod
    def isOwnedInAppProduct(product_id):
        owned = Mengine.androidBooleanMethod(GOOGLE_PLAY_BILLING_PLUGIN, "isOwnedInAppProduct", product_id)
        _Log("[Billing] isOwnedInAppProduct {!r} - {}".format(product_id, owned))
        return owned

    @staticmethod
    def responseProducts():
        if SystemGoogleServices.s_products is None:
            return

        currency = None
        products = {}
        for prod_id, details in SystemGoogleServices.s_products.items():
            params = {
                # convert price from micros to normal with 2 digits after comma
                "price": round(float(details["oneTimePurchaseOfferDetails"]["priceAmountMicros"]) / 1000000, 2),
                "descr": str(details["description"]),
                "name": str(details["name"])
            }
            products[prod_id] = params

            if currency is None:
                currency = str(details["oneTimePurchaseOfferDetails"]["priceCurrencyCode"])

        _Log("[Billing] response on queryProducts: {}".format(products))

        Notification.notify(Notificator.onProductsUpdate, products, currency)

    # callbacks

    @staticmethod
    def __cbBillingPurchaseUnspecifiedState(products):
        # this callback is called when we call buyInApp, but purchase state is not known yet
        #    - products is list of product ids
        _Log("[Billing cb] onGooglePlayBillingPurchaseUnspecifiedState: {!r}".format(products))


    @staticmethod
    def __cbBillingPurchaseIsConsumable(products, cb):
        # after we call buyInApp, we need to setup consumable status for purchase
        #    cb is `MengineFunctorBoolean cb = (Boolean isConsumable)`
        #    if product is acknowledged, Mengine sends onGooglePlayBillingPurchaseAcknowledged
        isConsumable = False
        for prod_id in products:
            prod_consumable = ProductsProvider.isProductConsumable(prod_id)
            _Log("[Billing cb] onGooglePlayBillingPurchaseIsConsumable: {!r} consumable={!r}".format(prod_id, prod_consumable))
            if prod_consumable is True:
                isConsumable = True
            pass

        cb(True, dict(isConsumable=isConsumable))

    @staticmethod
    def __cbBillingPurchasePending(products):
        # this callback is called when we call buyInApp, but purchase is pending
        #    - products is list of product ids
        _Log("[Billing cb] onGooglePlayBillingPurchasePending: {!r}".format(products))
        for prod_id in products:
            Notification.notify(Notificator.onPayPending, prod_id)

    @staticmethod
    def __cbBillingBuyInAppLaunchFlowSucces(prod_id):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppSuccess: prod_id={!r}".format(prod_id))
        Notification.notify(Notificator.onPayLaunchFlowSuccess, prod_id)

    @staticmethod
    def __cbBillingBuyInAppLaunchFlowFailed(prod_id, code, subCode):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppFailed: prod_id={!r} code={!r} subCode={!r}".format(prod_id, code, subCode))
        Notification.notify(Notificator.onPayLaunchFlowFailed, prod_id)

    @staticmethod
    def __cbBillingBuyInAppLaunchFlowError(prod_id, code, exception):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppError: prod_id={!r} code={!r} exception={!r}".format(prod_id, code, exception))
        Notification.notify(Notificator.onPayLaunchFlowError, prod_id)

    @staticmethod
    def __cbBillingQueryProductsSuccess(products):
        # this callback receives details of every product in json format
        #    - productId - The product ID for the product.
        #    - type - "inapp"  for an in-app product or "subs" for subscriptions.
        #    - price - formatted price without taxes, i.e. "UAH 37.22".
        #    - price_amount_micros - Price in micro-units (1000000 micro-units = 1 unit), i.e. "EUR 7.99" is "7990000".
        #    - price_currency_code - ISO 4217 currency code for price, i.e. "GBP".
        #    - title - Title of the product with Game ID.
        #    - name - Just title of the product.
        #    - description - Description of the product.

        _Log("[Billing cb] query products SUCCESS: {!r}".format(products))
        SystemGoogleServices.sku_response_event()

        # save
        SystemGoogleServices.s_products = {product["productId"]: product for product in products}
        SystemGoogleServices.responseProducts()

    @staticmethod
    def __cbBillingQueryProductsFail():
        _Log("[Billing cb] query products FAIL", err=True, force=True)

    @staticmethod
    def __cbBillingQueryProductsError(code, exception):
        _Log("[Billing cb] query products ERROR: code={!r} exception={!r}".format(code, exception), err=True, force=True)

    @staticmethod
    def __cbBillingPurchaseOnConsumeSuccess(products):
        # pay success for consumable
        _Log("[Billing cb] purchase consumable successful: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, True)

    @staticmethod
    def __cbBillingPurchaseOnConsumeFail(products):
        # pay fail for consumable
        _Log("[Billing cb] purchase consumable failed: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, False)

    @staticmethod
    def __cbBillingPurchaseAcknowledged(products):
        # pay success if already purchased non-consumable
        _Log("[Billing cb] purchase non-consumable already acknowledged: {!r}".format(products))
        for prod_id in products:
            Notification.notify(Notificator.onProductAlreadyOwned, prod_id)
            # SystemMonetization sends onPayComplete when done
        Notification.notify(Notificator.onRestorePurchasesDone)

    @staticmethod
    def __cbBillingPurchaseAcknowledgeSuccess(products):
        # pay success for non-consumable
        _Log("[Billing cb] purchase non-consumable successful: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, True)

    @staticmethod
    def __cbBillingPurchaseAcknowledgeFail(products):
        # pay fail for non-consumable
        _Log("[Billing cb] purchase non-consumable failed: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, False)

    @staticmethod
    def handlePurchased(_products, status):
        products = filter(lambda x: x is not None, _products)
        for prod_id in products:
            if status is True:
                Notification.notify(Notificator.onPaySuccess, prod_id)
            else:
                Notification.notify(Notificator.onPayFailed, prod_id)
            Notification.notify(Notificator.onPayComplete, prod_id)

    @staticmethod
    def __cbRequestAchievementsStateSuccessful(achievements):
        _Log("[Billing cb] requestAchievementsState successful: achievements={!r}".format(achievements))
        pass

    @staticmethod
    def __cbRequestAchievementsStateCanceled():
        _Log("[Billing cb] requestAchievementsState canceled", err=True, force=True)

    @staticmethod
    def __cbRequestAchievementsStateError(exception):
        _Log("[Billing cb] requestAchievementsState error: exception={!r}".format(exception), err=True, force=True)

    @staticmethod
    def __cbBillingPurchaseError(reason):
        #  error while purchase
        product_id = SystemGoogleServices.__lastProductId
        _Log("[Billing cb] purchase process error, product {!r}: {}".format(product_id, reason), force=True, err=True)

        SystemGoogleServices.handlePurchased([product_id], False)

    @staticmethod
    def __cbBillingClientUnavailable():
        _Log("[Billing cb] billing client unavailable, try to reconnect", err=True)
        SystemGoogleServices.startBillingClient()

    @staticmethod
    def __cbBillingPurchaseErrorUnknown(response_code):
        #  error while purchase, unknown error
        product_id = SystemGoogleServices.__lastProductId
        _Log("[Billing cb] purchase process error, product {!r}: Unknown error: {}".format(product_id, response_code), force=True, err=True)

        SystemGoogleServices.handlePurchased([product_id], False)

    @staticmethod
    def __cbBillingPurchaseItemAlreadyOwned():
        product_id = SystemGoogleServices.__lastProductId
        _Log("[Billing cb] purchase process error: ItemAlreadyOwned".format(product_id), force=True, err=True)
        SystemGoogleServices.handlePurchased([product_id], True)

    @staticmethod
    def __cbBillingPurchaseOk():
        #  item purchased successful
        _Log("[Billing cb] purchase process ok: {}".format(SystemGoogleServices.__lastProductId))
        pass

    @staticmethod
    def __cbBillingRestorePurchasesSuccess(products):
        _Log("[Billing cb] restore purchases successful: products={!r}".format(products))
        pass

    @staticmethod
    def __cbBillingRestorePurchasesFailed():
        _Log("[Billing cb] restore purchases failed", err=True, force=True)
        pass

    @staticmethod
    def __cbBillingRestorePurchasesError(code, exception):
        #  error while query purchases
        _Log("[Billing cb] restore purchases error: code={!r} exception={!r}".format(code, exception), err=True, force=True)
        pass

    # --- Achievements --------------------------------------------------------------------------------------------

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        # auth is not required
        _Log("[Achievements] try incrementAchievement {!r} for {} steps".format(achievement_id, steps), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "incrementAchievement", achievement_id, steps)
        pass

    @staticmethod
    def unlockAchievement(achievement_id):
        # auth is not required
        _Log("[Achievements] try unlockAchievement: {!r}".format(achievement_id), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "unlockAchievement", achievement_id)
        pass

    @staticmethod
    def showAchievements():
        # auth is not required
        _Log("[Achievements] try showAchievements...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "showAchievements")
        pass

    @staticmethod
    def incrementEvent(event_id, value):
        # increment event
        _Log("[Achievements] try incrementEvent: {!r} by {}".format(event_id, value), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "incrementEvent", event_id, value)
        pass

    # utils

    @staticmethod
    def __checkAuthForAchievements(method, *args):
        _Log("[Achievements] Not logged in to perform {!r} {}, save task...".format(method, args), err=True)
        SystemGoogleServices.__on_auth_achievements[method].append(args)
        pass

    # callbacks

    @staticmethod
    def __cbAchievementIncSuccess(achievement_id, steps):
        # cb on incrementAchievement
        _Log("[Achievements cb] AchievementIncrement Success: {!r} steps: {}".format(achievement_id, steps))
        pass

    @staticmethod
    def __cbAchievementIncError(achievement_id, steps, exception):
        # cb on incrementAchievement
        _Log("[Achievements cb] AchievementIncrement Error: {!r} steps: {} exception: {}".format(achievement_id, steps, exception), force=True, err=True)
        pass

    @staticmethod
    def __cbAchievementUnlockSuccess(achievement_id):
        # cb on unlockAchievement
        _Log("[Achievements cb] AchievementUnlock Success: {!r}".format(achievement_id))
        pass

    @staticmethod
    def __cbAchievementRevealSuccess(achievement_id):
        # cb on revealAchievement
        _Log("[Achievements cb] AchievementReveal Success: {!r}".format(achievement_id))
        pass

    @staticmethod
    def __cbAchievementRevealError(achievement_id, exception):
        # cb on revealAchievement
        _Log("[Achievements cb] AchievementReveal Error: {!r} exception: {}".format(achievement_id, exception), force=True, err=True)
        pass

    @staticmethod
    def __cbAchievementUnlockError(achievement_id, exception):
        # cb on unlockAchievement
        _Log("[Achievements cb] AchievementUnlock achivement: {!r} exception: {}".format(achievement_id, exception), force=True, err=True)
        pass

    @staticmethod
    def __cbAchievementShowSuccess():
        # cb on showAchievements
        _Log("[Achievements cb] show achievement: Success")
        pass

    @staticmethod
    def __cbAchievementShowCanceled():
        # cb on showAchievements
        _Log("[Achievements cb] show achievement: Canceled")
        pass

    @staticmethod
    def __cbAchievementShowError(error):
        # cb on showAchievements
        _Log("[Achievements cb] show achievement error: {}".format(error), force=True, err=True)
        pass

    @staticmethod
    def __cbEventIncrementSuccess(eventId, value):
        # cb on incrementEvent
        _Log("[Achievements cb] EventIncrement Success: eventId={!r} value={}".format(eventId, value))
        pass

    @staticmethod
    def __cbEventIncrementError(eventId, value, exception):
        # cb on incrementEvent
        _Log("[Achievements cb] EventIncrement Error: eventId={!r} value={} exception: {}".format(eventId, value, exception), force=True, err=True)
        pass

    @staticmethod
    def __cbLeaderboardScoreSuccess(leaderboard_id, score):
        # cb on setLeaderboardScore
        _Log("[Achievements cb] LeaderboardScore Success: {!r} score: {}".format(leaderboard_id, score))
        pass

    @staticmethod
    def __cbLeaderboardScoreError(leaderboard_id, score, exception):
        # cb on setLeaderboardScore
        _Log("[Achievements cb] LeaderboardScore Error: {!r} score: {} error: {}".format(leaderboard_id, score, exception), force=True, err=True)
        pass

    # --- InAppReviews -------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        # starts rate app process
        _Log("[Reviews] rateApp...")
        if SystemGoogleServices.b_plugins[GOOGLE_IN_APP_REVIEWS_PLUGIN] is False:
            Trace.log("System", 0, "SystemGoogleServices try to rateApp, but plugin '{}' is not active".format(GOOGLE_IN_APP_REVIEWS_PLUGIN))
            return
        Mengine.androidMethod(GOOGLE_IN_APP_REVIEWS_PLUGIN, "launchTheInAppReview")
        pass

    # callbacks

    @staticmethod
    def __cbGoogleInAppReviewsReady():
        # on initialize success
        _Log("[Reviews cb] GettingReviewObject")
        pass

    @staticmethod
    def __cbReviewsRequestError(exception):
        # reviews was not requested
        _Log("[Reviews cb] RequestError {}".format(exception), force=True)
        pass

    @staticmethod
    def __cbReviewsLaunchingSuccess():
        # reviews was launched
        Notification.notify(Notificator.onAppRated)
        _Log("[Reviews cb] LaunchingSuccess", force=True)
        pass

    @staticmethod
    def __cbReviewsLaunchingError(exception):
        # reviews was not launched
        _Log("[Reviews cb] LaunchingError {}".format(exception), force=True)
        pass

    # --- GoogleConsent -------------------------------------------------------------------------------------------------

    @staticmethod
    def showConsentFlow():
        if SystemGoogleServices.b_plugins[GOOGLE_CONSENT_PLUGIN] is False:
            _Log("[Consent] plugin {!r} is not active for showConsentFlow".format(GOOGLE_CONSENT_PLUGIN))
            return False

        if _ANDROID:
            Mengine.androidMethod(GOOGLE_CONSENT_PLUGIN, "showConsentFlow")
            return True
        elif _IOS:
            # iOS implementation can be added here if needed
            return False
        return False

    @staticmethod
    def isConsentFlow():
        if SystemGoogleServices.b_plugins[GOOGLE_CONSENT_PLUGIN] is False:
            return False

        if _ANDROID:
            return Mengine.androidBooleanMethod(GOOGLE_CONSENT_PLUGIN, "isConsentFlowUserGeographyGDPR")
        elif _IOS:
            # iOS implementation can be added here if needed
            return False
        return False

    # callbacks

    @staticmethod
    def __cbConsentFlowCompleted():
        _Log("[Consent cb] Consent Flow Completed")
        pass

    @staticmethod
    def __cbConsentFlowError(exception):
        _Log("[Consent cb] Consent Flow Error: {}".format(exception), err=True, force=True)
        pass

    # --- FirebaseCrashlytics ------------------------------------------------------------------------------------------

    @staticmethod
    def testCrash():
        if SystemGoogleServices.b_plugins[FIREBASE_CRASHLYTICS_PLUGIN] is False:
            Trace.log("System", 0, "try to testCrash, but plugin '{}' is not active".format(FIREBASE_CRASHLYTICS_PLUGIN))
            return
        _Log("[FirebaseCrashlytics] testCrash...")
        Mengine.androidMethod(FIREBASE_CRASHLYTICS_PLUGIN, "testCrash")
        pass

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab("GoogleServices"):
            return
        if True not in SystemGoogleServices.b_plugins.values():
            return

        tab = Mengine.addDevToDebugTab("GoogleServices")
        widgets = []

        # achievements
        if self.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is True:
            w_achievement_unlock = Mengine.createDevToDebugWidgetCommandLine("unlock_achievement")
            w_achievement_unlock.setTitle("Unlock achievement")
            w_achievement_unlock.setPlaceholder("syntax: <achievement_id>")
            w_achievement_unlock.setCommandEvent(self.unlockAchievement)
            widgets.append(w_achievement_unlock)

            def _increment_achievement(text):
                # input text allow 2 words separated by space:
                #        first word - achievement_id
                #        second optional word - is steps
                params = text.split(" ")
                achievement_id = params[0]
                steps = int(params[1]) if len(params) > 1 else 100
                self.incrementAchievement(achievement_id, steps)

            w_achievement_inc = Mengine.createDevToDebugWidgetCommandLine("increment_achievement")
            w_achievement_inc.setTitle("Increment achievement by n steps")
            w_achievement_inc.setPlaceholder("syntax: <achievement_id> <steps>")
            w_achievement_inc.setCommandEvent(_increment_achievement)
            widgets.append(w_achievement_inc)

            w_show_achievements = Mengine.createDevToDebugWidgetButton("show_achievements")
            w_show_achievements.setTitle("Show achievements")
            w_show_achievements.setClickEvent(self.showAchievements)
            widgets.append(w_show_achievements)

            # login
            w_login = Mengine.createDevToDebugWidgetButton("sign_in")
            w_login.setTitle("Sign IN <--")
            w_login.setClickEvent(self.signIn)
            widgets.append(w_login)

            w_logout = Mengine.createDevToDebugWidgetButton("sign_out")
            w_logout.setTitle("Sign OUT -->")
            w_logout.setClickEvent(self.signOut)
            widgets.append(w_logout)

            w_sign_in_intent = Mengine.createDevToDebugWidgetButton("sign_in_intent")
            w_sign_in_intent.setTitle("Sign In [Intent]")
            w_sign_in_intent.setClickEvent(self._signInIntent)
            widgets.append(w_sign_in_intent)

        # payment
        if self.b_plugins[GOOGLE_PLAY_BILLING_PLUGIN] is True:
            w_buy = Mengine.createDevToDebugWidgetCommandLine("buy")
            w_buy.setTitle("Buy product")
            w_buy.setPlaceholder("syntax: <prod_id>")
            w_buy.setCommandEvent(self.buy)
            widgets.append(w_buy)

            w_connect_billing = Mengine.createDevToDebugWidgetButton("connect_billing")
            w_connect_billing.setTitle("Connect billing client")
            w_connect_billing.setClickEvent(self.startBillingClient)
            widgets.append(w_connect_billing)

            w_restore = Mengine.createDevToDebugWidgetButton("restore_products")
            w_restore.setTitle("Restore purchases")
            w_restore.setClickEvent(self.restorePurchases)
            widgets.append(w_restore)

        # rateApp
        if self.b_plugins[GOOGLE_IN_APP_REVIEWS_PLUGIN] is True:
            w_rate = Mengine.createDevToDebugWidgetButton("rate_app")
            w_rate.setTitle("Show Rate App window")
            w_rate.setClickEvent(self.rateApp)
            widgets.append(w_rate)

        # Firebase Crashlytics
        if self.b_plugins[FIREBASE_CRASHLYTICS_PLUGIN] is True:
            w_test_crash = Mengine.createDevToDebugWidgetButton("test_crash")
            w_test_crash.setTitle("FirebaseCrashlytics - Test Crash")
            w_test_crash.setClickEvent(self.testCrash)
            widgets.append(w_test_crash)

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        if Mengine.hasDevToDebugTab("GoogleServices"):
            Mengine.removeDevToDebugTab("GoogleServices")
