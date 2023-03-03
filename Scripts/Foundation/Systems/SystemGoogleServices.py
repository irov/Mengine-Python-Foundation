import json

from Event import Event
from Foundation.PolicyManager import PolicyManager
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemGoogleServices")

class SystemGoogleServices(System):
    """ Google service that provides
        - authentication in Google Account
        - Billing
        - Google Play Social
        - InAppReviews
    """

    __lastProductId = None

    b_plugins = {
        "GoogleGameSocial": _PLUGINS.get("GoogleGameSocial", False),
        "GooglePlayBilling": _PLUGINS.get("GooglePlayBilling", False),
        "GoogleInAppReviews": _PLUGINS.get("GoogleInAppReviews", False)
    }

    login_event = Event("GoogleGameSocialLoginEvent")
    logout_event = Event("GoogleGameSocialLogoutEvent")
    login_data = None
    __on_auth_achievements = {}
    __on_auth_cbs = {}
    sku_response_event = Event("SkuListResponse")

    s_skus = {}

    def _onInitialize(self):
        if self.b_plugins["GoogleGameSocial"] is True:
            # auth:
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialOnSign", self.__cbSignSuccess)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialOnSignError", self.__cbSignError)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialOnSignFailed", self.__cbSignFail)

            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialSignOutSuccess", self.__cbSignOutSuccess)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialSignOutCanceled", self.__cbSignOutCanceled)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialSignOutFailure", self.__cbSignOutFailure)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialSignOutComplete", self.__cbSignOutComplete)

            # incrementAchievement:
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialAchievementIncrementError", self.__cbAchievementIncError)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialAchievementIncrementSuccess", self.__cbAchievementIncSuccess)
            # unlockAchievement:
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialAchievementSuccess", self.__cbAchievementUnlockSuccess)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialAchievementError", self.__cbAchievementUnlockError)
            # showAchievements:
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialShowAchievementSuccess", self.__cbAchievementShowSuccess)
            Mengine.setAndroidCallback("GoogleGameSocial", "onGoogleGameSocialShowAchievementError", self.__cbAchievementShowError)

            PolicyManager.setPolicy("ExternalAchieveProgress", "PolicyExternalAchieveProgressGooglePlay")
            PolicyManager.setPolicy("Authorize", "PolicyAuthGoogleService")

        if self.b_plugins["GooglePlayBilling"] is True:
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingBuyInAppSuccess", self.__cbBillingBuyInAppSuccess)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingOnSkuResponse", self.__cbBillingOnSkuResponse)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingOnConsume", self.__cbBillingOnConsume)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingIsAcknowledge", self.__cbBillingIsAcknowledge)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingAcknowledge", self.__cbBillingAcknowledge)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingDeveloperError", self.__cbBillingDeveloperError)
            Mengine.setAndroidCallback("GooglePlayBilling", "onGooglePlayBillingUserCanceled", self.__cbBillingUserCanceled)

            PolicyManager.setPolicy("Purchase", "PolicyPurchaseGoogleBilling")

        if self.b_plugins["GoogleInAppReviews"] is True:
            Mengine.setAndroidCallback("GoogleInAppReviews", "onGoogleInAppReviewsGettingReviewObject", self.__cbReviewsGettingReviewObject)
            Mengine.setAndroidCallback("GoogleInAppReviews", "onGoogleInAppReviewsLaunchingTheReviewCompleted", self.__cbReviewsLaunchingComplete)

        if self.b_plugins["GoogleGameSocial"] is True:
            self.signIn()

        self.__addDevToDebug()

    def _onFinalize(self):
        self.__remDevToDebug()

    def _onStop(self):
        pass

    def _onRun(self):
        self.__setDefaultSaves()

        return True

    def _onSave(self):
        dict_save = {"cbs": SystemGoogleServices.__on_auth_cbs, "achievements": SystemGoogleServices.__on_auth_achievements}
        return dict_save

    def _onLoad(self, dict_save):
        SystemGoogleServices.__on_auth_cbs = dict_save.get("cbs", {})
        SystemGoogleServices.__on_auth_achievements = dict_save.get("achievements", {})

    @staticmethod
    def __setDefaultSaves():
        SystemGoogleServices.__on_auth_cbs = {"showAchievements": False, "buy": None}
        SystemGoogleServices.__on_auth_achievements = {"increment": [], "unlock": []}

    # --- GoogleGameSocial ---------------------------------------------------------------------------------------------

    @staticmethod
    def isLoggedIn():
        b_login = SystemGoogleServices.login_data is not None
        return b_login

    @staticmethod
    def signIn(only_intent=False):
        if SystemGoogleServices.b_plugins["GoogleGameSocial"] is False:
            _Log("[Auth] plugin GoogleGameSocial is not active for signIn")
            return

        if only_intent is True:
            SystemGoogleServices._signInIntent()
            return

        if TaskManager.existTaskChain("GoogleGameSocialSignIn"):
            if _DEVELOPMENT:
                _Log("[Auth] GoogleGameSocialSignIn is already in process...", err=True)
            return

        with TaskManager.createTaskChain(Name="GoogleGameSocialSignIn") as tc:
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
        Mengine.androidMethod("GoogleGameSocial", "startSignInIntent")

    @staticmethod
    def _signInSilently():
        _Log("[Auth] signIn Silently...", force=True)
        Mengine.androidMethod("GoogleGameSocial", "signInSilently")

    @staticmethod
    def signOut():
        if SystemGoogleServices.b_plugins["GoogleGameSocial"] is False:
            _Log("[Auth] plugin GoogleGameSocial is not active for signOut")
            return
        _Log("[Auth] signOut...", force=True)
        Mengine.androidMethod("GoogleGameSocial", "signOut")

    # callbacks

    @staticmethod
    def __cbSignSuccess(account_id):
        if account_id is None or account_id == "":
            _Log("[Auth cb] account_id is None or empty string !!!!!!", err=True)
            account_id = "undefined"

        SystemGoogleServices.login_data = account_id
        SystemGoogleServices.updateProducts()
        SystemGoogleServices.login_event(True)

        SystemGoogleServices.__cbRestoreTasks()
        _Log("[Auth cb] successfully logged in: id={!r}".format(account_id))

    @staticmethod
    def __cbSignFail():
        SystemGoogleServices.login_event(False)
        _Log("[Auth cb] login failed", err=True, force=True)

    @staticmethod
    def __cbSignError():
        SystemGoogleServices.login_event(False)
        _Log("[Auth cb] login error", err=True, force=True)

    @staticmethod
    def __cbSignOutSuccess():
        SystemGoogleServices.login_data = None
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
        SystemGoogleServices.login_data = None
        SystemGoogleServices.logout_event(True)
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

        sku = SystemGoogleServices.__on_auth_cbs.get("buy", None)
        if sku is not None:
            SystemGoogleServices.buy(sku)

        SystemGoogleServices.__setDefaultSaves()

    # --- GooglePlayBilling --------------------------------------------------------------------------------------------

    @staticmethod
    def updateProducts():
        # this alias will call `setSkuList` with all products ids
        # then in callback `__cbBillingOnSkuResponse` calls `sendSkus`
        # and finally sends push to MonetizationManager for update products
        TaskManager.runAlias("AliasCurrentProductsCall", None, CallFunction=SystemGoogleServices.setSkuList)

    @staticmethod
    def setSkuList(skus):
        """ setup product's list and return details via callback `__cbBillingOnSkuResponse`
            @param skus: List<String> - product ids list. Each non-str value will be ignored """
        skus = filter(lambda x: isinstance(x, str), skus)
        _Log("[Billing] setSkuList: skus={!r}".format(skus))
        Mengine.androidMethod("GooglePlayBilling", "setSkuList", skus)

    @staticmethod
    def buy(sku):
        """ buy product, success callback is `__cbBillingOnConsume`
            @param sku: String - product id """
        if SystemGoogleServices.isLoggedIn() is False:
            _Log("[Billing error] buy: sku={!r} failed: not authorized, try auth...".format(sku), err=True, force=True)
            SystemGoogleServices.__on_auth_cbs["buy"] = sku
            SystemGoogleServices.signIn(only_intent=True)
            return

        _Log("[Billing] buy: sku={!r}".format(sku))
        Mengine.androidBooleanMethod("GooglePlayBilling", "buyInApp", sku)
        SystemGoogleServices.__lastProductId = sku

    @staticmethod
    def restorePurchases():  # todo: configure callbacks
        _Log("[Billing] restore purchases...")
        Mengine.androidMethod("GooglePlayBilling", "queryPurchases")

    # utils

    @staticmethod
    def skuJsonToDict(raw_sku):
        """ Returns python dict from raw sku json string or None if error """

        if raw_sku is None:
            Trace.log("System", 3, "Can't skuJsonToDict None, may be you put unknown product_id")
            return None

        # remove wrong characters
        raw = raw_sku.replace("\xc2\xa0", " ").replace("\n", "&#10;")
        raw = raw.replace("ProductDetails{jsonString='", "")
        raw = raw[:raw.index("}'") + 1]  # +1 because we want to get this bracket too in our slice
        # we do "}'", not "'", because game title could contain "'"

        try:
            sku = json.loads(raw)
        except ValueError as e:
            Trace.log("System", 0, "Can't json.loads [{}] from {!r}".format(e, raw))
            sku = None

        return sku

    @staticmethod
    def sendSkus():
        s_skus = SystemGoogleServices.s_skus
        if s_skus is None:
            return

        skus = {}
        for prod_id, sku in s_skus.items():
            params = {
                "price": round(float(sku["oneTimePurchaseOfferDetails"]["priceAmountMicros"]) / 1000000, 2),
                "descr": str(sku["description"]), "name": str(sku["name"])
            }
            skus[prod_id] = params

        _Log("[Billing sendSkus] skus={!r}".format(skus))

        if len(s_skus) > 0:
            _random_sku = s_skus.items()[0][1]
            currency = str(_random_sku["oneTimePurchaseOfferDetails"]["priceCurrencyCode"])
        else:
            currency = None

        Notification.notify(Notificator.onProductsUpdate, skus, currency)

    # callbacks

    @staticmethod
    def __cbBillingBuyInAppSuccess(prod_id, status):
        """ purchase process status """
        if status is False:
            Notification.notify(Notificator.onPayFailed, prod_id)

            if Mengine.getConfigBool("GoogleService", "RetryPurchaseOnFail", True) is True:
                if TaskManager.existTaskChain("SystemGoogleServices_RetryPurchase") is True:
                    return

                timeout_delay = Mengine.getConfigInt("GoogleService", "RetryPurchaseTimeout", 10) * 1000.0

                with TaskManager.createTaskChain(Name="SystemGoogleServices_RetryPurchase") as tc:
                    with tc.addRaceTask(2) as (timeout, retry):
                        timeout.addDelay(timeout_delay)

                        with retry.addParallelTask(2) as (respond, request):
                            respond.addListener(Notificator.onProductsUpdateDone)
                            respond.addFunction(SystemGoogleServices.buy, prod_id)
                            request.addFunction(SystemGoogleServices.updateProducts)

        _Log("[Billing cb] onGooglePlayBillingBuyInAppSuccess: prod_id={!r}, status={!r}".format(prod_id, status))

    @staticmethod
    def __cbBillingOnSkuResponse(raw_skus):
        """ this callback receives details of every product in json format
            :param raw_skus: list of strings in json format with prod details

            - productId - The product ID for the product.
            - type - "inapp"  for an in-app product or "subs" for subscriptions.
            - price - formatted price without taxes, i.e. "UAH 37.22".
            - price_amount_micros - Price in micro-units (1000000 micro-units = 1 unit), i.e. "EUR 7.99" is "7990000".
            - price_currency_code - ISO 4217 currency code for price, i.e. "GBP".
            - title - Title of the product with Game ID.
            - name - Just title of the product.
            - description - Description of the product.
        """

        _Log("[Billing cb] onGooglePlayBillingOnSkuResponse raw: {!r}".format(raw_skus))
        SystemGoogleServices.sku_response_event()

        # save skus
        list_skus = [params for params in [SystemGoogleServices.skuJsonToDict(sku) for sku in raw_skus] if params]
        dict_skus = {sku["productId"]: sku for sku in list_skus}
        SystemGoogleServices.s_skus = dict_skus
        SystemGoogleServices.sendSkus()

        _Log("[Billing cb] onGooglePlayBillingOnSkuResponse skus: {!r}".format(list_skus))

    @staticmethod
    def __cbBillingOnConsume(_prod_ids):
        """ pay success """
        prod_ids = filter(lambda x: x is not None, _prod_ids)
        for prod_id in prod_ids:
            Notification.notify(Notificator.onPaySuccess, prod_id)
        _Log("[Billing cb] onGooglePlayBillingOnConsume: {!r}".format(prod_ids))

    @staticmethod
    def __cbBillingIsAcknowledge(cb, skus):
        """ purchase completed + Cb """
        # todo
        _Log("[Billing cb] onGooglePlayBillingIsAcknowledge: cb={!r} skus={!r}".format(cb, skus))

    @staticmethod
    def __cbBillingAcknowledge(skus):
        """ callback from Google after successful product sale """
        # todo
        _Log("[Billing cb] onGooglePlayBillingAcknowledge: {!r}".format(skus))

    @staticmethod
    def __cbBillingDeveloperError():
        """  error in credentials or purchased products """
        Notification.notify(Notificator.onPayFailed, SystemGoogleServices.__lastProductId)
        _Log("[Billing cb] onGooglePlayBillingDeveloperError", force=True, err=True)

    @staticmethod
    def __cbBillingUserCanceled():
        """ user canceled a purchase  """
        Notification.notify(Notificator.onPayFailed, SystemGoogleServices.__lastProductId)
        _Log("[Billing cb] onGooglePlayBillingUserCanceled")

    # --- Achievements --------------------------------------------------------------------------------------------

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        if SystemGoogleServices.__checkAuthForAchievements("increment", achievement_id, steps) is False:
            return
        _Log("[Achievements] try incrementAchievement {!r} for {} steps".format(achievement_id, steps), force=True)
        Mengine.androidBooleanMethod("GoogleGameSocial", "incrementAchievement", achievement_id, steps)

    @staticmethod
    def unlockAchievement(achievement_id):
        if SystemGoogleServices.__checkAuthForAchievements("unlock", achievement_id) is False:
            return
        _Log("[Achievements] try unlockAchievement: {!r}".format(achievement_id), force=True)
        Mengine.androidBooleanMethod("GoogleGameSocial", "unlockAchievement", achievement_id)

    @staticmethod
    def showAchievements():
        if SystemGoogleServices.isLoggedIn() is False:
            _Log("[Achievements error] showAchievements failed: not authorized, try auth...", err=True)
            SystemGoogleServices.__on_auth_cbs["showAchievements"] = True
            SystemGoogleServices.signIn(only_intent=True)
            return
        _Log("[Achievements] try showAchievements...", force=True)
        Mengine.androidBooleanMethod("GoogleGameSocial", "showAchievements")

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
            Trace.log("System", 0, "SystemGoogleServices try to rateApp, but plugin 'GoogleInAppReviews' is not active")
            return
        Mengine.androidMethod("GoogleInAppReviews", "launchTheInAppReview")
        _Log("[Reviews] rateApp...")

    # callbacks

    @staticmethod
    def __cbReviewsGettingReviewObject():
        """ on initialize success """
        _Log("[Reviews cb] GettingReviewObject")

    @staticmethod
    def __cbReviewsLaunchingComplete():
        """ reviews was launched """
        Notification.notify(Notificator.onAppRated)
        _Log("[Reviews cb] LaunchingComplete", force=True)

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
            def _unlock_achievement(achievement_id):
                self.unlockAchievement(achievement_id)

            w_achievement_unlock = Mengine.createDevToDebugWidgetCommandLine("unlock_achievement")
            w_achievement_unlock.setTitle("Unlock achievement")
            w_achievement_unlock.setPlaceholder("syntax: <achievement_id>")
            w_achievement_unlock.setCommandEvent(_unlock_achievement)
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
                return "Current account id: {}".format(SystemGoogleServices.login_data)

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

        # payment
        if self.b_plugins["GooglePlayBilling"] is True:
            def _buy(prod_id):
                self.buy(prod_id)

            w_buy = Mengine.createDevToDebugWidgetCommandLine("buy_sku")
            w_buy.setTitle("Buy product")
            w_buy.setPlaceholder("syntax: <prod_id>")
            w_buy.setCommandEvent(_buy)
            widgets.append(w_buy)

            w_update_products = Mengine.createDevToDebugWidgetButton("update_products")
            w_update_products.setTitle("Update products (update prices and prod params)")
            w_update_products.setClickEvent(self.updateProducts)
            widgets.append(w_update_products)

        # rateApp
        if self.b_plugins["GoogleInAppReviews"] is True:
            w_rate = Mengine.createDevToDebugWidgetButton("rate_app")
            w_rate.setTitle("Show Rate App window")
            w_rate.setClickEvent(self.rateApp)
            widgets.append(w_rate)

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        if Mengine.hasDevToDebugTab("GoogleServices"):
            Mengine.removeDevToDebugTab("GoogleServices")