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
    """ Google service that provides
        - authentication in Google Account
        - Billing
        - Google Play Social
        - InAppReviews
    """

    __lastProductId = None

    b_plugins = {
        "GoogleGameSocial": Mengine.isAvailablePlugin(GOOGLE_GAME_SOCIAL_PLUGIN),
        "GooglePlayBilling": Mengine.isAvailablePlugin(GOOGLE_PLAY_BILLING_PLUGIN),
        "GoogleInAppReviews": Mengine.isAvailablePlugin(GOOGLE_IN_APP_REVIEWS_PLUGIN),
        "FirebaseCrashlytics": Mengine.isAvailablePlugin(FIREBASE_CRASHLYTICS_PLUGIN),
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

        if self.b_plugins["GoogleGameSocial"] is True:
            def setSocialCallback(callback_name, *callback):
                method_name = "onGoogleGameSocial" + callback_name
                Mengine.setAndroidCallback(GOOGLE_GAME_SOCIAL_PLUGIN, method_name, *callback)

            # auth:
            setSocialCallback("OnAuthenticatedSuccess", self.__cbSignSuccess)
            setSocialCallback("OnAuthenticatedFailed", self.__cbSignFailed)
            setSocialCallback("OnAuthenticatedError", self.__cbSignError)
            # incrementAchievement:
            setSocialCallback("AchievementIncrementSuccess", self.__cbAchievementIncSuccess)
            setSocialCallback("AchievementIncrementError", self.__cbAchievementIncError)
            # unlockAchievement:
            setSocialCallback("UnlockAchievementSuccess", self.__cbAchievementUnlockSuccess)
            setSocialCallback("UnlockAchievementError", self.__cbAchievementUnlockError)
            # showAchievements:
            setSocialCallback("ShowAchievementSuccess", self.__cbAchievementShowSuccess)
            setSocialCallback("ShowAchievementError", self.__cbAchievementShowError)

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

        if self.b_plugins["GooglePlayBilling"] is True:
            def setBillingCallback(callback_name, *callback):
                method_name = "onGooglePlayBilling" + callback_name
                Mengine.setAndroidCallback(GOOGLE_PLAY_BILLING_PLUGIN, method_name, *callback)

            # purchase status
            setBillingCallback("PurchasesUpdatedServiceTimeout", self.__cbBillingPurchaseError, "ServiceTimeout")
            setBillingCallback("PurchasesUpdatedFeatureNotSupported", self.__cbBillingPurchaseError, "FeatureNotSupported")
            setBillingCallback("PurchasesUpdatedServiceDisconnected", self.__cbBillingPurchaseError, "ServiceDisconnected")
            setBillingCallback("PurchasesUpdatedServiceUnavailable", self.__cbBillingPurchaseError, "ServiceUnavailable")
            setBillingCallback("PurchasesUpdatedBillingUnavailable", self.__cbBillingPurchaseError, "BillingUnavailable")
            setBillingCallback("PurchasesUpdatedItemUnavailable", self.__cbBillingPurchaseError, "ItemUnavailable")
            setBillingCallback("PurchasesUpdatedDeveloperError", self.__cbBillingPurchaseError, "DeveloperError")
            setBillingCallback("PurchasesUpdatedError", self.__cbBillingPurchaseError, "Error")
            setBillingCallback("PurchasesUpdatedItemAlreadyOwned", self.__cbBillingPurchaseItemAlreadyOwned)
            setBillingCallback("PurchasesUpdatedItemNotOwned", self.__cbBillingPurchaseError, "ItemNotOwned")
            setBillingCallback("PurchasesUpdatedUnknown", self.__cbBillingPurchaseError)
            setBillingCallback("PurchasesUpdatedUserCanceled", self.__cbBillingPurchaseError, "UserCanceled")
            setBillingCallback("PurchasesUpdatedOk", self.__cbBillingPurchaseOk)
            # query products & purchases (for restore)
            setBillingCallback("QueryProductSuccess", self.__cbBillingQueryProductsSuccess)
            setBillingCallback("QueryProductFailed", self.__cbBillingQueryProductsFail)
            setBillingCallback("QueryPurchasesSuccess", self.__cbBillingQueryPurchasesStatus, True)
            setBillingCallback("QueryPurchasesFailed", self.__cbBillingQueryPurchasesStatus, False)
            # purchase flow
            setBillingCallback("PurchaseIsConsumable", self.__cbBillingPurchaseIsConsumable)
            setBillingCallback("BuyInAppSuccess", self.__cbBillingBuyInAppStatus, True)
            setBillingCallback("BuyInAppFailed", self.__cbBillingBuyInAppStatus, False)
            #  - consumable
            setBillingCallback("PurchasesOnConsumeSuccess", self.__cbBillingPurchaseConsumeSuccess)
            setBillingCallback("PurchasesOnConsumeFailed", self.__cbBillingPurchaseConsumeFail)
            #  - non-consumable
            setBillingCallback("PurchaseAcknowledged", self.__cbBillingPurchaseAcknowledged)
            setBillingCallback("PurchasesAcknowledgeSuccess", self.__cbBillingPurchaseAcknowledgeSuccess)
            setBillingCallback("PurchasesAcknowledgeFailed", self.__cbBillingPurchaseAcknowledgeFail)
            # billingConnect callbacks:
            setBillingCallback("ConnectServiceDisconnected", self.__cbBillingClientDisconnected)
            setBillingCallback("ConnectSetupFinishedFailed", self.__cbBillingClientSetupFinishedFail)
            setBillingCallback("ConnectSetupFinishedSuccess", self.__cbBillingClientSetupFinishedSuccess)

            self.startBillingClient()

            PaymentProvider.setProvider("Google", dict(
                pay=self.buy,
                queryProducts=self.queryProducts,
                restorePurchases=self.restorePurchases
            ))

        if self.b_plugins["GoogleInAppReviews"] is True:
            def setReviewsCallback(callback_name, *callback):
                method_name = "onGoogleInAppReviews" + callback_name
                Mengine.setAndroidCallback(GOOGLE_IN_APP_REVIEWS_PLUGIN, method_name, *callback)

            Mengine.waitSemaphore("onGoogleInAppReviewsGettingReviewObject", self.__cbReviewsGettingReviewObject)
            setReviewsCallback("LaunchingTheReviewSuccess", self.__cbReviewsLaunchingSuccess)
            setReviewsCallback("LaunchingTheReviewError", self.__cbReviewsLaunchingError)

            RatingAppProvider.setProvider("Google", dict(rateApp=self.rateApp))

        if self.b_plugins["GoogleGameSocial"] is True:
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
        if SystemGoogleServices.b_plugins["GoogleGameSocial"] is False:
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
                with respond.addRaceTask(2) as (success, fail):
                    success.addEvent(SystemGoogleServices.login_event, Filter=lambda status: status is True)
                    success.addFunction(_Log, "[Auth] silence auth success!")

                    fail.addEvent(SystemGoogleServices.login_event, Filter=lambda status: status is False)
                    fail.addFunction(_Log, "[Auth] silence auth failed, try intent...")
                    fail.addFunction(SystemGoogleServices._signInIntent)

                request.addFunction(_Log, "[Auth] try silence auth...")
                request.addFunction(SystemGoogleServices._signInSilently)

    @staticmethod
    def _signInIntent():
        _Log("[Auth] startSignIn Intent...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "startSignInIntent")

    @staticmethod
    def _signInSilently():
        _Log("[Auth] signIn Silently...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "signInSilently")

    @staticmethod
    def signOut():
        if SystemGoogleServices.b_plugins["GoogleGameSocial"] is False:
            _Log("[Auth] plugin {!r} is not active for signOut".format(GOOGLE_GAME_SOCIAL_PLUGIN))
            return
        _Log("[Auth] signOut...", force=True)
        Mengine.androidMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "signOut")

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
    def __cbSignError():
        SystemGoogleServices.login_event(False)
        _Log("[Auth cb] login error", err=True, force=True)

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
        """ callbacks:
            __cbBillingClientDisconnected
            __cbBillingClientSetupFinishedFail
            __cbBillingClientSetupFinishedSuccess   - OK
        """
        _Log("Start connect to the billing client...")
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "billingConnect")

    @staticmethod
    def getBillingClientStatus():
        return SystemGoogleServices.__billing_client_status

    @staticmethod
    def queryProducts(product_ids):
        """ setup product's list and response via callbacks
            - __cbBillingQueryProductsSuccess <- product details - OK
            - __cbBillingQueryProductsFail
        """
        if SystemGoogleServices.getBillingClientStatus() != BILLING_CLIENT_STATUS_OK:
            _Log("[Billing] queryProducts fail: billing client is not connected", err=True, force=True)
            SystemGoogleServices.__cbBillingPurchaseError("BillingClientUnavailable")
            return False

        query_list = filter(lambda x: isinstance(x, str), product_ids)
        _Log("[Billing] queryProducts: query_list={!r}".format(query_list))
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "queryProducts", query_list)
        return True

    @staticmethod
    def buy(product_id):
        """ start purchase flow
            1. onGooglePlayBillingPurchasesUpdatedOk or FAIL
            2. onGooglePlayBillingPurchaseIsConsumable - here we check is consumable and starts handling
            - consumable:
                3. onGooglePlayBillingPurchasesOnConsumeSuccess - OK
                   onGooglePlayBillingPurchasesOnConsumeFailed
            - non-consumable:
                3. onGooglePlayBillingPurchasesAcknowledgeSuccess - OK
                   onGooglePlayBillingPurchasesAcknowledgeFailed

        """
        if SystemGoogleServices.getBillingClientStatus() != BILLING_CLIENT_STATUS_OK:
            _Log("[Billing] buy fail: billing client is not connected", err=True, force=True)
            SystemGoogleServices.__cbBillingPurchaseError("BillingClientUnavailable")
            return

        if SystemGoogleServices.isLoggedIn() is False:
            _Log("[Billing error] buy {!r} failed: not authorized, try auth...".format(product_id), err=True, force=True)
            SystemGoogleServices.__on_auth_cbs["buy"] = product_id
            SystemGoogleServices.signIn(only_intent=True)
            return

        _Log("[Billing] buy {!r}".format(product_id))
        SystemGoogleServices.__lastProductId = product_id
        if Mengine.androidBooleanMethod(GOOGLE_PLAY_BILLING_PLUGIN, "buyInApp", product_id) is False:
            SystemGoogleServices.__cbBillingPurchaseError("BuyInApp return False")

    @staticmethod
    def restorePurchases():
        _Log("[Billing] restore purchases...")
        Mengine.androidMethod(GOOGLE_PLAY_BILLING_PLUGIN, "queryPurchases")

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
    def __cbBillingPurchaseIsConsumable(products, cb):
        """ after we call buyInApp, we need to setup consumable status for purchase
            cb is `MengineFunctorBoolean cb = (Boolean isConsumable)`
            if product is acknowledged, Mengine sends onGooglePlayBillingPurchaseAcknowledged
        """
        for prod_id in products:
            isConsumable = ProductsProvider.isProductConsumable(prod_id)
            _Log("[Billing cb] onGooglePlayBillingPurchaseIsConsumable: {!r} consumable={!r}".format(prod_id, isConsumable))
            cb(True, dict(isConsumable=isConsumable))

    @staticmethod
    def __cbBillingBuyInAppStatus(prod_id, status):
        """ purchase process status """
        if status is False:
            Notification.notify(Notificator.onPayFailed, prod_id)
            Notification.notify(Notificator.onPayComplete, prod_id)
        _Log("[Billing cb] onGooglePlayBillingBuyInAppSuccess: prod_id={!r}, status={!r}".format(prod_id, status))

    @staticmethod
    def __cbBillingQueryProductsSuccess(products):
        """ this callback receives details of every product in json format

            - productId - The product ID for the product.
            - type - "inapp"  for an in-app product or "subs" for subscriptions.
            - price - formatted price without taxes, i.e. "UAH 37.22".
            - price_amount_micros - Price in micro-units (1000000 micro-units = 1 unit), i.e. "EUR 7.99" is "7990000".
            - price_currency_code - ISO 4217 currency code for price, i.e. "GBP".
            - title - Title of the product with Game ID.
            - name - Just title of the product.
            - description - Description of the product.
        """

        _Log("[Billing cb] query products SUCCESS: {!r}".format(products))
        SystemGoogleServices.sku_response_event()

        # save
        SystemGoogleServices.s_products = {product["productId"]: product for product in products}
        SystemGoogleServices.responseProducts()

    @staticmethod
    def __cbBillingQueryProductsFail():
        _Log("[Billing cb] query products FAIL", err=True, force=True)

    @staticmethod
    def __cbBillingPurchaseConsumeSuccess(products):
        """ pay success for consumable """
        _Log("[Billing cb] purchase consumable successful: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, True)

    @staticmethod
    def __cbBillingPurchaseConsumeFail(products):
        """ pay fail for consumable  """
        _Log("[Billing cb] purchase consumable failed: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, False)

    @staticmethod
    def __cbBillingPurchaseAcknowledged(products):
        """ pay success if already purchased non-consumable """
        _Log("[Billing cb] purchase non-consumable already acknowledged: {!r}".format(products))
        for prod_id in products:
            Notification.notify(Notificator.onProductAlreadyOwned, prod_id)
            # SystemMonetization sends onPayComplete when done
        Notification.notify(Notificator.onRestorePurchasesDone)

    @staticmethod
    def __cbBillingPurchaseAcknowledgeSuccess(products):
        """ pay success for non-consumable """
        _Log("[Billing cb] purchase non-consumable successful: {!r}".format(products))
        SystemGoogleServices.handlePurchased(products, True)

    @staticmethod
    def __cbBillingPurchaseAcknowledgeFail(products):
        """ pay fail for non-consumable  """
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
    def __cbBillingPurchaseError(response_code):
        """  error while purchase """
        product_id = SystemGoogleServices.__lastProductId
        _Log("[Billing cb] purchase process error, product {!r}: {}".format(product_id, response_code), force=True, err=True)

        SystemGoogleServices.handlePurchased([product_id], False)

        if response_code == "BillingClientUnavailable":
            SystemGoogleServices.startBillingClient()

    @staticmethod
    def __cbBillingPurchaseItemAlreadyOwned():
        product_id = SystemGoogleServices.__lastProductId
        _Log("[Billing cb] purchase process error: ItemAlreadyOwned".format(product_id), force=True, err=True)
        SystemGoogleServices.handlePurchased([product_id], True)

    @staticmethod
    def __cbBillingPurchaseOk():
        """  item purchased successful """
        _Log("[Billing cb] purchase process ok: {}".format(SystemGoogleServices.__lastProductId))

    @staticmethod
    def __cbBillingClientDisconnected():
        _Log("[Billing cb] billing client disconnected")
        SystemGoogleServices.__billing_client_status = BILLING_CLIENT_STATUS_NOT_CONNECTED

    @staticmethod
    def __cbBillingClientSetupFinishedFail():
        _Log("[Billing cb] billing client setup finished with status: FAIL", err=True)
        SystemGoogleServices.__billing_client_status = BILLING_CLIENT_STATUS_FAIL

    @staticmethod
    def __cbBillingClientSetupFinishedSuccess():
        _Log("[Billing cb] billing client setup finished with status: SUCCESS")
        SystemGoogleServices.__billing_client_status = BILLING_CLIENT_STATUS_OK

        # we should call query products only with PaymentProvider
        if Mengine.getConfigBool("Monetization", "AutoQueryProducts", True) is True:
            PaymentProvider.queryProducts()
        else:
            _Log("Auto query products disabled, do it manually in code")

    @staticmethod
    def __cbBillingQueryPurchasesStatus(status):
        _Log("[Billing cb] query purchases status: {}".format(status))

    # --- Achievements --------------------------------------------------------------------------------------------

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        # auth is not required
        _Log("[Achievements] try incrementAchievement {!r} for {} steps".format(achievement_id, steps), force=True)
        Mengine.androidBooleanMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "incrementAchievement", achievement_id, steps)

    @staticmethod
    def unlockAchievement(achievement_id):
        # auth is not required
        _Log("[Achievements] try unlockAchievement: {!r}".format(achievement_id), force=True)
        Mengine.androidBooleanMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "unlockAchievement", achievement_id)

    @staticmethod
    def showAchievements():
        # auth is not required
        _Log("[Achievements] try showAchievements...", force=True)
        Mengine.androidBooleanMethod(GOOGLE_GAME_SOCIAL_PLUGIN, "showAchievements")

    # utils

    @staticmethod
    def __checkAuthForAchievements(method, *args):
        if SystemGoogleServices.isLoggedIn() is True:
            return
        _Log("[Achievements] Not logged in to perform {!r} {}, save task...".format(method, args), err=True)
        SystemGoogleServices.__on_auth_achievements[method].append(args)

    # callbacks

    @staticmethod
    def __cbAchievementIncSuccess(achievement_id):
        """ cb on incrementAchievement """
        _Log("[Achievements cb] AchievementIncrement Success: {!r}".format(achievement_id))

    @staticmethod
    def __cbAchievementIncError(achievement_id):
        """ cb on incrementAchievement """
        _Log("[Achievements cb] AchievementIncrement Error: {!r}".format(achievement_id), force=True, err=True)

    @staticmethod
    def __cbAchievementUnlockSuccess(achievement_id):
        """ cb on unlockAchievement """
        _Log("[Achievements cb] AchievementUnlock Success: {!r}".format(achievement_id))

    @staticmethod
    def __cbAchievementUnlockError(achievement_id):
        """ cb on unlockAchievement """
        _Log("[Achievements cb] AchievementUnlock Error: {!r}".format(achievement_id), force=True, err=True)

    @staticmethod
    def __cbAchievementShowSuccess():
        """ cb on showAchievements """
        _Log("[Achievements cb] show achievement: Success")

    @staticmethod
    def __cbAchievementShowError():
        """ cb on showAchievements """
        _Log("[Achievements cb] show achievement: Error", force=True, err=True)

    # --- InAppReviews -------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        """ starts rate app process """
        if SystemGoogleServices.b_plugins["GoogleInAppReviews"] is False:
            Trace.log("System", 0, "SystemGoogleServices try to rateApp, but plugin '{}' is not active".format(GOOGLE_IN_APP_REVIEWS_PLUGIN))
            return
        Mengine.androidMethod(GOOGLE_IN_APP_REVIEWS_PLUGIN, "launchTheInAppReview")
        _Log("[Reviews] rateApp...")

    # callbacks

    @staticmethod
    def __cbReviewsGettingReviewObject():
        """ on initialize success """
        _Log("[Reviews cb] GettingReviewObject")

    @staticmethod
    def __cbReviewsLaunchingSuccess():
        """ reviews was launched """
        Notification.notify(Notificator.onAppRated)
        _Log("[Reviews cb] LaunchingSuccess", force=True)

    @staticmethod
    def __cbReviewsLaunchingError():
        """ reviews was not launched """
        _Log("[Reviews cb] LaunchingError", force=True)

    # --- FirebaseCrashlytics ------------------------------------------------------------------------------------------

    @staticmethod
    def testCrash():
        if SystemGoogleServices.b_plugins["FirebaseCrashlytics"] is False:
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
        if self.b_plugins["GoogleGameSocial"] is True:
            w_achievement_unlock = Mengine.createDevToDebugWidgetCommandLine("unlock_achievement")
            w_achievement_unlock.setTitle("Unlock achievement")
            w_achievement_unlock.setPlaceholder("syntax: <achievement_id>")
            w_achievement_unlock.setCommandEvent(self.unlockAchievement)
            widgets.append(w_achievement_unlock)

            def _increment_achievement(text):
                """ input text allow 2 words separated by space:
                        first word - achievement_id
                        second optional word - is steps """
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

            w_sign_in_silence = Mengine.createDevToDebugWidgetButton("sign_in_silence")
            w_sign_in_silence.setTitle("Sign In [Silence]")
            w_sign_in_silence.setClickEvent(self._signInSilently)
            widgets.append(w_sign_in_silence)

            w_sign_in_intent = Mengine.createDevToDebugWidgetButton("sign_in_intent")
            w_sign_in_intent.setTitle("Sign In [Intent]")
            w_sign_in_intent.setClickEvent(self._signInIntent)
            widgets.append(w_sign_in_intent)

        # payment
        if self.b_plugins["GooglePlayBilling"] is True:
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
        if self.b_plugins["GoogleInAppReviews"] is True:
            w_rate = Mengine.createDevToDebugWidgetButton("rate_app")
            w_rate.setTitle("Show Rate App window")
            w_rate.setClickEvent(self.rateApp)
            widgets.append(w_rate)

        # Firebase Crashlytics
        if self.b_plugins["FirebaseCrashlytics"] is True:
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
