from Event import Event
from Foundation.PolicyManager import PolicyManager
from Foundation.Providers.RatingAppProvider import RatingAppProvider
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from Foundation.Providers.PaymentProvider import PaymentProvider
from Foundation.Providers.ProductsProvider import ProductsProvider
from Foundation.Providers.AuthProvider import AuthProvider
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemGoogleServices")

BILLING_CLIENT_STATUS_NOT_CONNECTED = 0
BILLING_CLIENT_STATUS_OK = 1
BILLING_CLIENT_STATUS_FAIL = 2

GOOGLE_GAME_SOCIAL_PLUGIN = "MengineGGameSocial"
GOOGLE_PLAY_BILLING_PLUGIN = "MengineGPlayBilling"
GOOGLE_IN_APP_REVIEWS_PLUGIN = "MengineGInAppReviews"
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
        FIREBASE_CRASHLYTICS_PLUGIN: Mengine.isAvailablePlugin(FIREBASE_CRASHLYTICS_PLUGIN),
    }

    login_event = Event("GoogleGameSocialLoginEvent")
    logout_event = Event("GoogleGameSocialLogoutEvent")
    login_status = False
    __on_auth_achievements = {}
    __on_auth_cbs = {}
    sku_response_event = Event("SkuListResponse")   # todo: check is deprecated

    s_products = {}
    __billing_client_status = BILLING_CLIENT_STATUS_NOT_CONNECTED

    def _onInitialize(self):

        if self.b_plugins[GOOGLE_GAME_SOCIAL_PLUGIN] is True:
            def _setCallback(method_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_GAME_SOCIAL_PLUGIN, method_name, *callback)

            # sign in:
            _setCallback("onGoogleGameSocialSignInIntentSuccess", self.__cbSignSuccess)
            _setCallback("onGoogleGameSocialSignInIntentFailed", self.__cbSignFailed)
            _setCallback("onGoogleGameSocialSignInIntentError", self.__cbSignError)
            # auth:
            _setCallback("onGoogleGameSocialOnAuthenticatedSuccess", self.__cbSignSuccess)
            _setCallback("onGoogleGameSocialOnAuthenticatedFailed", self.__cbSignFailed)
            _setCallback("onGoogleGameSocialOnAuthenticatedError", self.__cbSignError)
            # incrementAchievement:
            _setCallback("onGoogleGameSocialIncrementAchievementSuccess", self.__cbAchievementIncSuccess)
            _setCallback("onGoogleGameSocialIncrementAchievementError", self.__cbAchievementIncError)
            # unlockAchievement:
            _setCallback("onGoogleGameSocialUnlockAchievementSuccess", self.__cbAchievementUnlockSuccess)
            _setCallback("onGoogleGameSocialUnlockAchievementError", self.__cbAchievementUnlockError)
            # revealAchievement:
            _setCallback("onGoogleGameSocialRevealAchievementSuccess", self.__cbAchievementRevealSuccess)
            _setCallback("onGoogleGameSocialRevealAchievementError", self.__cbAchievementRevealError)
            # showAchievements:
            _setCallback("onGoogleGameSocialShowAchievementSuccess", self.__cbAchievementShowSuccess)
            _setCallback("onGoogleGameSocialShowAchievementError", self.__cbAchievementShowError)

            _setCallback("onGoogleGameSocialIncrementEventSuccess", self.__cbEventIncrementSuccess)
            _setCallback("onGoogleGameSocialIncrementEventError", self.__cbEventIncrementError)


            _setCallback("onGoogleGameSocialLeaderboardScoreSuccess", self.__cbLeaderboardScoreSuccess)
            _setCallback("onGoogleGameSocialLeaderboardScoreError", self.__cbLeaderboardScoreError)



            AchievementsProvider.setProvider("Google", dict(
                unlockAchievement=self.unlockAchievement,
                incrementAchievement=self.incrementAchievement,
                showAchievements=self.showAchievements,
            ))
            AuthProvider.setProvider("Google", dict(
                login=self.signIn,
                logout=self.signOut,
                isLoggedIn=self.isLoggedIn,
            ))
            PolicyManager.setPolicy("Authorize", "PolicyAuthGoogleService")    # deprecated

        if self.b_plugins[GOOGLE_PLAY_BILLING_PLUGIN] is True:
            def _setCallback(method_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_PLAY_BILLING_PLUGIN, method_name, *callback)

            # purchase status
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceTimeout", self.__cbBillingPurchaseError, "ServiceTimeout")
            _setCallback("onGooglePlayBillingPurchasesUpdatedFeatureNotSupported", self.__cbBillingPurchaseError, "FeatureNotSupported")
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceDisconnected", self.__cbBillingPurchaseError, "ServiceDisconnected")
            _setCallback("onGooglePlayBillingPurchasesUpdatedServiceUnavailable", self.__cbBillingPurchaseError, "ServiceUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedBillingUnavailable", self.__cbBillingPurchaseError, "BillingUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemUnavailable", self.__cbBillingPurchaseError, "ItemUnavailable")
            _setCallback("onGooglePlayBillingPurchasesUpdatedDeveloperError", self.__cbBillingPurchaseError, "DeveloperError")
            _setCallback("onGooglePlayBillingPurchasesUpdatedError", self.__cbBillingPurchaseError, "Error")
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemAlreadyOwned", self.__cbBillingPurchaseItemAlreadyOwned)
            _setCallback("onGooglePlayBillingPurchasesUpdatedItemNotOwned", self.__cbBillingPurchaseError, "ItemNotOwned")
            _setCallback("onGooglePlayBillingPurchasesUpdatedNetworkError", self.__cbBillingPurchaseError, "NetworkError")
            _setCallback("onGooglePlayBillingPurchasesUpdatedUnknown", self.__cbBillingPurchaseErrorUnknown)
            _setCallback("onGooglePlayBillingPurchasesUpdatedUserCanceled", self.__cbBillingPurchaseError, "UserCanceled")
            _setCallback("onGooglePlayBillingPurchasesUpdatedOk", self.__cbBillingPurchaseOk)
            # query products & purchases (for restore)
            _setCallback("onGooglePlayBillingQueryProductSuccess", self.__cbBillingQueryProductsSuccess)
            _setCallback("onGooglePlayBillingQueryProductFailed", self.__cbBillingQueryProductsFail)
            _setCallback("onGooglePlayBillingQueryProductError", self.__cbBillingQueryProductsError)
            _setCallback("onGooglePlayBillingQueryPurchasesSuccess", self.__cbBillingQueryPurchasesSuccess)
            _setCallback("onGooglePlayBillingQueryPurchasesFailed", self.__cbBillingQueryPurchasesFailed)
            _setCallback("onGooglePlayBillingQueryPurchasesError", self.__cbBillingQueryPurchasesError)
            # purchase flow
            _setCallback("onGooglePlayBillingPurchaseUnspecifiedState", self.__cbBillingPurchaseUnspecifiedState)
            _setCallback("onGooglePlayBillingPurchaseIsConsumable", self.__cbBillingPurchaseIsConsumable)
            _setCallback("onGooglePlayBillingPurchasePending", self.__cbBillingPurchasePending)

            _setCallback("onGooglePlayBillingBuyInAppSuccess", self.__cbBillingBuyInAppSucces)
            _setCallback("onGooglePlayBillingBuyInAppFailed", self.__cbBillingBuyInAppFailed)
            _setCallback("onGooglePlayBillingBuyInAppError", self.__cbBillingBuyInAppError)
            #  - consumable
            _setCallback("onGooglePlayBillingPurchasesOnConsumeSuccess", self.__cbBillingPurchaseConsumeSuccess)
            _setCallback("onGooglePlayBillingPurchasesOnConsumeFailed", self.__cbBillingPurchaseConsumeFail)
            #  - non-consumable
            _setCallback("onGooglePlayBillingPurchaseAcknowledged", self.__cbBillingPurchaseAcknowledged)
            _setCallback("onGooglePlayBillingPurchaseAcknowledgeSuccess", self.__cbBillingPurchaseAcknowledgeSuccess)
            _setCallback("onGooglePlayBillingPurchaseAcknowledgeFailed", self.__cbBillingPurchaseAcknowledgeFail)

            self.startBillingClient()

            PaymentProvider.setProvider("Google", dict(
                pay=self.buy,
                queryProducts=self.queryProducts,
                restorePurchases=self.restorePurchases
            ))

        if self.b_plugins[GOOGLE_IN_APP_REVIEWS_PLUGIN] is True:
            def _setCallback(callback_name, *callback):
                Mengine.addAndroidCallback(GOOGLE_IN_APP_REVIEWS_PLUGIN, callback_name, *callback)

            Mengine.waitSemaphore("onGoogleInAppReviewsGettingReviewObject", self.__cbReviewsGettingReviewObject)

            _setCallback("onGoogleInAppReviewsRequestReviewError", self.__cbReviewsRequestError)
            _setCallback("onGoogleInAppReviewsLaunchingTheReviewSuccess", self.__cbReviewsLaunchingSuccess)
            _setCallback("onGoogleInAppReviewsLaunchingTheReviewError", self.__cbReviewsLaunchingError)

            RatingAppProvider.setProvider("Google", dict(rateApp=self.rateApp))

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
        return SystemGoogleServices.login_status

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

        with TaskManager.createTaskChain(Name="SystemGoogleServices_SignIn") as tc:
            with tc.addParallelTask(2) as (respond, request):
                with request.addIfTask(Mengine.androidBooleanMethod, GOOGLE_GAME_SOCIAL_PLUGIN, "isAuthenticated") as (success, fail):
                    success.addFunction(_Log, "[Auth] silence auth success!")

                    fail.addFunction(_Log, "[Auth] silence auth failed, try intent...")
                    fail.addFunction(SystemGoogleServices._signInIntent)

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
        SystemGoogleServices.login_status = True
        SystemGoogleServices.login_event(True)
        Notification.notify(Notificator.onUserLoggedIn)

        SystemGoogleServices.__cbRestoreTasks()
        _Log("[Auth cb] successfully login in")

    @staticmethod
    def __cbSignFailed():
        SystemGoogleServices.login_event(False)
        _Log("[Auth cb] login failed", err=True, force=True)

    @staticmethod
    def __cbSignError(exception):
        SystemGoogleServices.login_event(False)
        _Log("[Auth cb] login error: {}".format(exception), err=True, force=True)

    @staticmethod
    def __cbNeedIntentSign():
        _Log("[Auth cb] silent login error - call intent login this time", err=True)
        SystemGoogleServices._signInIntent()

    @staticmethod
    def __cbSignOutSuccess():
        SystemGoogleServices.login_status = False
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
        SystemGoogleServices.login_status = False
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
    def startBillingClient():
        # callbacks:
        #    __cbBillingClientDisconnected
        #    __cbBillingClientSetupFinishedFail
        #    __cbBillingClientSetupFinishedSuccess   - OK

        _Log("Start connect to the billing client...")
        #Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "billingConnect")

    @staticmethod
    def getBillingClientStatus():
        return SystemGoogleServices.__billing_client_status

    @staticmethod
    def queryProducts(product_ids):
        # setup product's list and response via callbacks
        #    - __cbBillingQueryProductsSuccess <- product details - OK
        #    - __cbBillingQueryProductsFail
        if SystemGoogleServices.getBillingClientStatus() != BILLING_CLIENT_STATUS_OK:
            _Log("[Billing] queryProducts fail: billing client is not connected", err=True, force=True)
            SystemGoogleServices.__cbBillingClientUnavailable()
            return False

        query_list = filter(lambda x: isinstance(x, str), product_ids)
        _Log("[Billing] queryProducts: query_list={!r}".format(query_list))
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "queryProducts", query_list)
        return True

    @staticmethod
    def buy(product_id):
        if SystemGoogleServices.getBillingClientStatus() != BILLING_CLIENT_STATUS_OK:
            _Log("[Billing] buy fail: billing client is not connected", err=True, force=True)
            SystemGoogleServices.__cbBillingClientUnavailable()
            return

        if SystemGoogleServices.isLoggedIn() is False:
            _Log("[Billing error] buy {!r} failed: not authorized, try auth...".format(product_id), err=True, force=True)
            SystemGoogleServices.__on_auth_cbs["buy"] = product_id
            SystemGoogleServices.signIn(only_intent=True)
            return

        _Log("[Billing] buy {!r}".format(product_id))
        SystemGoogleServices.__lastProductId = product_id
        Mengine.androidBooleanMethod(GOOGLE_PLAY_BILLING_PLUGIN, "buyInApp", product_id)

    @staticmethod
    def restorePurchases():
        _Log("[Billing] restore purchases...")
        #Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "queryPurchases")

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
        for prod_id in products:
            isConsumable = ProductsProvider.isProductConsumable(prod_id)
            _Log("[Billing cb] onGooglePlayBillingPurchaseIsConsumable: {!r} consumable={!r}".format(prod_id, isConsumable))
            cb(True, dict(isConsumable=isConsumable))

    @staticmethod
    def __cbBillingPurchasePending(products):
        # this callback is called when we call buyInApp, but purchase is pending
        #    - products is list of product ids
        _Log("[Billing cb] onGooglePlayBillingPurchasePending: {!r}".format(products))
        for prod_id in products:
            Notification.notify(Notificator.onPayPending, prod_id)

    @staticmethod
    def __cbBillingBuyInAppSucces(prod_id):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppSuccess: prod_id={!r}".format(prod_id))
        Notification.notify(Notificator.onPayComplete, prod_id)

    @staticmethod
    def __cbBillingBuyInAppFailed(prod_id, code, subCode):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppFailed: prod_id={!r} code={!r} subCode={!r}".format(prod_id, code, subCode))
        Notification.notify(Notificator.onPayFailed, prod_id)

    @staticmethod
    def __cbBillingBuyInAppError(prod_id, code, exception):
        _Log("[Billing cb] onGooglePlayBillingBuyInAppError: prod_id={!r} code={!r} exception={!r}".format(prod_id, code, exception))
        Notification.notify(Notificator.onPayFailed, prod_id)

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
    def __cbBillingPurchaseConsumeSuccess(products):
        # pay success for consumable
        _Log("[Billing cb] purchase consumable successful: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, True)

    @staticmethod
    def __cbBillingPurchaseConsumeFail(products):
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

    @staticmethod
    def __cbBillingQueryPurchasesSuccess():
        _Log("[Billing cb] query purchases success")

    @staticmethod
    def __cbBillingQueryPurchasesFailed():
        _Log("[Billing cb] query purchases failed", err=True, force=True)

    @staticmethod
    def __cbBillingQueryPurchasesError(code, exception):
        #  error while query purchases
        _Log("[Billing cb] query purchases error: code={!r} exception={!r}".format(code, exception), err=True, force=True)

    # --- Achievements --------------------------------------------------------------------------------------------

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        # auth is not required
        _Log("[Achievements] try incrementAchievement {!r} for {} steps".format(achievement_id, steps), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "incrementAchievement", achievement_id, steps)

    @staticmethod
    def unlockAchievement(achievement_id):
        # auth is not required
        _Log("[Achievements] try unlockAchievement: {!r}".format(achievement_id), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "unlockAchievement", achievement_id)

    @staticmethod
    def showAchievements():
        # auth is not required
        _Log("[Achievements] try showAchievements...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "showAchievements")

    @staticmethod
    def incrementEvent(event_id, value):
        # increment event
        _Log("[Achievements] try incrementEvent: {!r} by {}".format(event_id, value), force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "incrementEvent", event_id, value)

    # utils

    @staticmethod
    def __checkAuthForAchievements(method, *args):
        if SystemGoogleServices.isLoggedIn() is True:
            return
        _Log("[Achievements] Not logged in to perform {!r} {}, save task...".format(method, args), err=True)
        SystemGoogleServices.__on_auth_achievements[method].append(args)

    # callbacks

    @staticmethod
    def __cbAchievementIncSuccess(achievement_id, steps):
        # cb on incrementAchievement
        _Log("[Achievements cb] AchievementIncrement Success: {!r} steps: {}".format(achievement_id, steps))

    @staticmethod
    def __cbAchievementIncError(achievement_id, steps, exception):
        # cb on incrementAchievement
        _Log("[Achievements cb] AchievementIncrement Error: {!r} steps: {} exception: {}".format(achievement_id, steps, exception), force=True, err=True)

    @staticmethod
    def __cbAchievementUnlockSuccess(achievement_id):
        # cb on unlockAchievement
        _Log("[Achievements cb] AchievementUnlock Success: {!r}".format(achievement_id))

    @staticmethod
    def __cbAchievementRevealSuccess(achievement_id):
        # cb on revealAchievement
        _Log("[Achievements cb] AchievementReveal Success: {!r}".format(achievement_id))

    @staticmethod
    def __cbAchievementRevealError(achievement_id, exception):
        # cb on revealAchievement
        _Log("[Achievements cb] AchievementReveal Error: {!r} exception: {}".format(achievement_id, exception), force=True, err=True)

    @staticmethod
    def __cbAchievementUnlockError(achievement_id, exception):
        # cb on unlockAchievement
        _Log("[Achievements cb] AchievementUnlock achivement: {!r} exception: {}".format(achievement_id, exception), force=True, err=True)

    @staticmethod
    def __cbAchievementShowSuccess():
        # cb on showAchievements
        _Log("[Achievements cb] show achievement: Success")

    @staticmethod
    def __cbAchievementShowError(error):
        # cb on showAchievements
        _Log("[Achievements cb] show achievement error: {}".format(error), force=True, err=True)

    @staticmethod
    def __cbEventIncrementSuccess(eventId, value):
        # cb on incrementEvent
        _Log("[Achievements cb] EventIncrement Success: eventId={!r} value={}".format(eventId, value))

    @staticmethod
    def __cbEventIncrementError(eventId, value, exception):
        # cb on incrementEvent
        _Log("[Achievements cb] EventIncrement Error: eventId={!r} value={} exception: {}".format(eventId, value, exception), force=True, err=True)

    @staticmethod
    def __cbLeaderboardScoreSuccess(leaderboard_id, score):
        # cb on setLeaderboardScore
        _Log("[Achievements cb] LeaderboardScore Success: {!r} score: {}".format(leaderboard_id, score))

    @staticmethod
    def __cbLeaderboardScoreError(leaderboard_id, score, exception):
        # cb on setLeaderboardScore
        _Log("[Achievements cb] LeaderboardScore Error: {!r} score: {} error: {}".format(leaderboard_id, score, exception), force=True, err=True)

    # --- InAppReviews -------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        # starts rate app process
        if SystemGoogleServices.b_plugins[GOOGLE_IN_APP_REVIEWS_PLUGIN] is False:
            Trace.log("System", 0, "SystemGoogleServices try to rateApp, but plugin '{}' is not active".format(GOOGLE_IN_APP_REVIEWS_PLUGIN))
            return
        Mengine.androidMethod(GOOGLE_IN_APP_REVIEWS_PLUGIN, "launchTheInAppReview")
        _Log("[Reviews] rateApp...")

    # callbacks

    @staticmethod
    def __cbReviewsGettingReviewObject():
        # on initialize success
        _Log("[Reviews cb] GettingReviewObject")

    @staticmethod
    def __cbReviewsRequestError(exception):
        # reviews was not requested
        _Log("[Reviews cb] RequestError {}".format(exception), force=True)

    @staticmethod
    def __cbReviewsLaunchingSuccess():
        # reviews was launched
        Notification.notify(Notificator.onAppRated)
        _Log("[Reviews cb] LaunchingSuccess", force=True)

    @staticmethod
    def __cbReviewsLaunchingError(exception):
        # reviews was not launched
        _Log("[Reviews cb] LaunchingError {}".format(exception), force=True)

    # --- FirebaseCrashlytics ------------------------------------------------------------------------------------------

    @staticmethod
    def testCrash():
        if SystemGoogleServices.b_plugins[FIREBASE_CRASHLYTICS_PLUGIN] is False:
            Trace.log("System", 0, "try to testCrash, but plugin '{}' is not active".format(FIREBASE_CRASHLYTICS_PLUGIN))
            return
        _Log("[FirebaseCrashlytics] testCrash...")
        Mengine.androidMethod(FIREBASE_CRASHLYTICS_PLUGIN, "testCrash")

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
            def _login_status():
                return "Current account id: {}".format(SystemGoogleServices.login_status)

            w_login_status = Mengine.createDevToDebugWidgetText("login_status")
            w_login_status.setText(_login_status)
            widgets.append(w_login_status)

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

            w_update_products = Mengine.createDevToDebugWidgetButton("query_products")
            w_update_products.setTitle("Query products")
            w_update_products.setClickEvent(PaymentProvider.queryProducts)
            widgets.append(w_update_products)

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
