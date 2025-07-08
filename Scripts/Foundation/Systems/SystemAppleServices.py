from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Foundation.Providers.RatingAppProvider import RatingAppProvider
from Foundation.Providers.PaymentProvider import PaymentProvider
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from Foundation.TaskManager import TaskManager


_Log = SimpleLogger("SystemAppleServices", option="apple")
PLUGIN_GAME_CENTER = "AppleGameCenter"
PLUGIN_STORE_REVIEW = "AppleStoreReview"
PLUGIN_APP_TRACKING = "AppleAppTracking"
PLUGIN_IN_APP_PURCHASE = "AppleStoreInAppPurchase"


class SystemAppleServices(System):

    """
        How to connect to the GameCenter:
            1. setGameCenterConnectProvider()
            2. connectToGameCenter()
    """

    b_plugins = {
        "GameCenter": Mengine.isAvailablePlugin(PLUGIN_GAME_CENTER),
        "Review": Mengine.isAvailablePlugin(PLUGIN_STORE_REVIEW),
        "Tracking": Mengine.isAvailablePlugin(PLUGIN_APP_TRACKING),
        "InAppPurchase": Mengine.isAvailablePlugin(PLUGIN_IN_APP_PURCHASE),
    }

    _GameCenter_authenticated = False
    _GameCenter_synchronized = False
    _GameCenter_provider_status = False
    _InAppPurchase_provider_status = False
    _Tracking_status = False
    _can_use_payment = False

    _products = {}
    EVENT_PRODUCTS_RESPONDED = Event("AppleInAppPurchaseProductsResponded")

    def _onInitialize(self):
        if self.b_plugins["InAppPurchase"] is True:
            if self.canUserMakePurchases() is True:
                SystemAppleServices._can_use_payment = True
                self.setInAppPurchaseProvider()

        if self.b_plugins["Review"] is True:
            RatingAppProvider.setProvider("Apple", dict(rateApp=self.rateApp))

        if self.b_plugins["GameCenter"] is True:
            SystemAppleServices.setGameCenterConnectProvider()
            SystemAppleServices.connectToGameCenter()

            AchievementsProvider.setProvider("Apple", dict(
                unlockAchievement=self.unlockAchievement,
                setAchievementProgress=self.setAchievementProgress,
            ))

        if self.b_plugins["Tracking"] is True and Mengine.getGameParamBool("AppleAppTrackingTransparency", False) is True:
            SystemAppleServices.appTrackingAuthorization()

        # todo: promocodes handling in onRequestPromoCodeResult

        self.__addDevToDebug()

    def _onFinalize(self):
        self.__remDevToDebug()

        if SystemAppleServices._GameCenter_provider_status is True:
            self.removeGameCenterConnectProvider()
        if SystemAppleServices._InAppPurchase_provider_status is True:
            self.removeInAppPurchaseProvider()

    # --- AppleGameCenter - connection ---------------------------------------------------------------------------------

    @staticmethod
    def setGameCenterConnectProvider():
        if SystemAppleServices.b_plugins["GameCenter"] is False:
            _Log("[GameCenter] set provider - plugin '{}' not active".format(PLUGIN_GAME_CENTER), err=True, force=True)
            return False

        _Log("[GameCenter] set provider...", optional=True)
        SystemAppleServices._GameCenter_provider_status = True

    @staticmethod
    def removeGameCenterConnectProvider():
        if SystemAppleServices._GameCenter_provider_status is False:
            _Log("[GameCenter] can't remove provider - not active", err=True)
            return

        _Log("[GameCenter] remove provider...", optional=True)
        SystemAppleServices._GameCenter_provider_status = False

    @staticmethod
    def connectToGameCenter():
        if SystemAppleServices.b_plugins["GameCenter"] is True:
            status = Mengine.appleGameCenterConnect({
            "onAppleGameCenterAuthenticate": SystemAppleServices.__cbGameCenterAuthenticate,
            "onAppleGameCenterSynchronizate": SystemAppleServices.__cbGameCenterSynchronize
        })  # check is request to GameCenter was sent
            # if True, cb provider will return bool that means player connected or not
        else:
            status = False

        describe = lambda result: "wait response" if result else "request sent failed!!"
        _Log("[GameCenter] CONNECT STATUS: {}".format(describe(status)))
        return status

    @staticmethod
    def __cbGameCenterAuthenticate(status, *args):
        """ callback for onAppleGameCenterAuthenticate """
        describe = lambda b: "successful" if b else "failed"

        log_message = "[GameCenter] (callback) AUTHENTICATE: {} [{}]".format(describe(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message, force=True)

        SystemAppleServices._GameCenter_authenticated = status

    @staticmethod
    def __cbGameCenterSynchronize(status, *args):
        """ callback for onAppleGameCenterSynchronizate """
        describe = lambda b: "successful" if b else "failed"

        log_message = "[GameCenter] (callback) SYNCHRONIZE: {} [{}]".format(describe(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message, force=True)

        SystemAppleServices._GameCenter_synchronized = status

    @staticmethod
    def isGameCenterConnected(report=False, on_status=False):
        b_status = SystemAppleServices._GameCenter_authenticated

        if report is True and on_status is b_status:
            _Log("[GameCenter] CONNECT STATUS: {}".format(b_status), err=not b_status)

        return b_status

    # --- AppleGameCenter - interaction --------------------------------------------------------------------------------

    @staticmethod
    def __cbGameCenterAchievementReporter(status, achievement_name, percent_complete, *args):
        descr = lambda b: "success {!r} (complete {}%%)".format(
            achievement_name, percent_complete) if b else "game center not received last achievement"
        log_message = "[GameCenter] (callback) ACHIEVEMENTS: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)
        return status

    @staticmethod
    def unlockAchievement(achievement_name):
        return SystemAppleServices._sendAchievementToGameCenter(achievement_name, percent_complete=100.0)

    @staticmethod
    def setAchievementProgress(achievement_name, current_step, total_steps):
        if current_step < 1 or total_steps < 1:
            Trace.log("System", 0, "current={}, total={} steps must be 1 or bigger".format(current_step, total_steps))
            return

        if current_step > total_steps:
            Trace.log("System", 0, "current={} must be equal or lower than total={}".format(current_step, total_steps))
            percent = 100.0
        elif current_step == total_steps:
            percent = 100.0
        else:
            percent = round((float(current_step) / float(total_steps)) * 100.0, 1)

        return SystemAppleServices._sendAchievementToGameCenter(achievement_name, percent_complete=percent)

    @staticmethod
    def _sendAchievementToGameCenter(achievement_name, percent_complete):
        _Log("[GameCenter] SEND ACHIEVEMENT {!r} (complete {}%%)...".format(achievement_name, percent_complete), force=True)

        if SystemAppleServices.isGameCenterConnected(report=True) is False:
            Trace.log("System", 0, "Plugin '{}' fail to send achievement - Game Center is not connected!".format(PLUGIN_GAME_CENTER))
            return

        Mengine.appleGameCenterReportAchievement(achievement_name, percent_complete,
                                                 SystemAppleServices.__cbGameCenterAchievementReporter,
                                                 achievement_name, percent_complete)

    @staticmethod
    def checkGameCenterAchievement(achievement_name):
        if SystemAppleServices.b_plugins["GameCenter"] is False:
            Trace.log("System", 0, "SystemAppleServices is not active to check achievement {!r}".format(achievement_name))
            return False
        if SystemAppleServices.isGameCenterConnected(report=True) is False:
            return False

        b_check = Mengine.appleGameCenterCheckAchievement(achievement_name)
        _Log("[GameCenter] CHECK ACHIEVEMENT {!r} RESULT: {}".format(achievement_name, b_check), force=True)
        return b_check

    # --- AppleAppTracking ---------------------------------------------------------------------------------------------

    @staticmethod
    def __cbAppTrackingAuth(_status, _idfa, *args):
        log_message = "[AppTracking] (callback) auth: status={} idfa={}".format(_status, _idfa)
        log_message += " | args: {}".format(args) if len(args) > 0 else ""
        _Log(log_message)
        SystemAppleServices._Tracking_status = _status

    @staticmethod
    def appTrackingAuthorization():
        _Log("[AppTracking] start authorization...")
        Mengine.appleAppTrackingAuthorization(SystemAppleServices.__cbAppTrackingAuth)

    # --- Rate us ------------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        if SystemAppleServices.b_plugins["Review"] is False:
            Trace.log("System", 0, "SystemAppleServices try to rateApp, but plugin '{}' is not active".format(PLUGIN_STORE_REVIEW))
            return
        _Log("[Reviews] rateApp...", force=True)
        Mengine.appleStoreReviewLaunchTheInAppReview()
        Notification.notify(Notificator.onAppRated)

    # --- In-App Purchases ---------------------------------------------------------------------------------------------

    @staticmethod
    def canUserMakePurchases():
        """ returns True if user could do purchases (not a child) or False, if not """
        status = Mengine.appleStoreInAppPurchaseCanMakePayments()
        _Log("[InAppPurchase] Can user make purchases? {}".format(status), optional=True)
        SystemAppleServices._can_use_payment = status
        return status

    @staticmethod
    def setInAppPurchaseProvider():
        """ setup payment callbacks """
        if SystemAppleServices.b_plugins["InAppPurchase"] is False:
            _Log("[InAppPurchase] set provider - plugin '{}' not active".format(PLUGIN_IN_APP_PURCHASE), err=True, force=True)
            return False

        _Log("[InAppPurchase] set provider...", optional=True)
        Mengine.appleStoreInAppPurchaseSetPaymentTransactionProvider({
            "onPaymentQueueUpdatedTransactionPurchasing": SystemAppleServices._cbPaymentPurchasing,
            "onPaymentQueueUpdatedTransactionPurchased": SystemAppleServices._cbPaymentPurchased,
            "onPaymentQueueUpdatedTransactionFailed": SystemAppleServices._cbPaymentFailed,
            "onPaymentQueueUpdatedTransactionRestored": SystemAppleServices._cbPaymentRestored,
            "onPaymentQueueUpdatedTransactionDeferred": SystemAppleServices._cbPaymentDeferred,
            "onPaymentQueueShouldShowPriceConsent": SystemAppleServices._cbPaymentQueueShouldShowPriceConsent,
            "onPaymentQueueShouldContinueTransaction": SystemAppleServices._cbPaymentQueueShouldContinueTransaction,
        })
        PaymentProvider.setProvider("Apple", dict(
            pay=SystemAppleServices.pay,
            canUserMakePurchases=SystemAppleServices.canUserMakePurchases,
            restorePurchases=SystemAppleServices.restorePurchases,
        ))
        SystemAppleServices._InAppPurchase_provider_status = True

    @staticmethod
    def removeInAppPurchaseProvider():
        """ finish InAppPurchase callbacks provider """

        if SystemAppleServices._InAppPurchase_provider_status is False:
            _Log("[InAppPurchase] can't remove provider - not active", err=True)
            return False

        _Log("[InAppPurchase] remove provider...", optional=True)
        Mengine.appleStoreInAppPurchaseRemovePaymentTransactionProvider()
        SystemAppleServices._InAppPurchase_provider_status = False

    @staticmethod
    def requestProducts(products_ids):
        _Log("[InAppPurchase] request product details for {}".format(products_ids), optional=True)
        Mengine.appleStoreInAppPurchaseRequestProducts(products_ids, {
            "onProductResponse": SystemAppleServices._cbProductResponse,
            "onProductFinish": SystemAppleServices._cbProductFinish,
            "onProductFail": SystemAppleServices._cbProductFail,
        })

    @staticmethod
    def restorePurchases():
        """ returns list of purchased products via cb _cbPaymentRestored """
        _Log("[InAppPurchase] restore purchases...", optional=True)
        Mengine.appleStoreInAppPurchaseRestoreCompletedTransactions()
        Notification.notify(Notificator.onRestorePurchasesDone)
        # TODO: it would be better to know when we complete all _cbPaymentRestored

    @staticmethod
    def pay(product_id):
        _Log("[InAppPurchase] pay {!r}...".format(product_id), optional=True)

        if SystemAppleServices._can_use_payment is False:
            Notification.notify(Notificator.onPayFailed, product_id)
            Notification.notify(Notificator.onPayComplete, product_id)
            Trace.log("System", 0, "This user can't use payment (product_id={})".format(product_id))
            return

        product = SystemAppleServices._products.get(product_id)
        if product is None:
            Notification.notify(Notificator.onPayFailed, product_id)
            Notification.notify(Notificator.onPayComplete, product_id)
            Trace.log("System", 0, "Product with id {} not found in responded products!!!".format(product_id))
            return

        Mengine.appleStoreInAppPurchasePurchaseProduct(product)

    # callbacks

    @staticmethod
    def _cbProductResponse(request, products):
        """
            input: AppleStoreInAppPurchaseProductInterface[]

            .def( "getProductIdentifier", &AppleStoreInAppPurchaseProductInterface::getProductIdentifier )
            .def( "getProductTitle", &AppleStoreInAppPurchaseProductInterface::getProductTitle )
            .def( "getProductDescription", &AppleStoreInAppPurchaseProductInterface::getProductDescription )
            .def( "getProductCurrencyCode", &AppleStoreInAppPurchaseProductInterface::getProductCurrencyCode )
            .def( "getProductPriceFormatted", &AppleStoreInAppPurchaseProductInterface::getProductPriceFormatted )
            .def( "getProductPrice", &AppleStoreInAppPurchaseProductInterface::getProductPrice )

        """

        if len(products) == 0:
            _Log("[InAppPurchase] (callback) Product Response Empty", err=True, force=True)
            return

        _Log("[InAppPurchase] (CALLBACK) Product Response: {}".format([p.getProductIdentifier() for p in products]))

        game_products = {}

        for product in products:
            product_id = str(product.getProductIdentifier())

            params = {
                "price": product.getProductPrice(),
                "descr": str(product.getProductDescription()),
                "name": str(product.getProductTitle())
            }
            game_products[product_id] = params

            SystemAppleServices._products[product_id] = product

        currency = products[0].getProductCurrencyCode()
        Notification.notify(Notificator.onProductsUpdate, game_products, currency)

    @staticmethod
    def _cbProductFinish(request):
        """ (CALLBACK) Product Response Finish"""
        _Log("[InAppPurchase] (callback) Product Response Finish")
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(True)

    @staticmethod
    def _cbProductFail(request):
        """ (CALLBACK) Product Response Fail"""
        _Log("[InAppPurchase] (callback) Product Response Fail", err=True)
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(False)

    @staticmethod
    def _cbPaymentPurchasing(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionPurchasing) start purchase process """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment Purchasing start {}".format(product_id))

    @staticmethod
    def _cbPaymentPurchased(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionPurchased) payment complete """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment Purchased (success) {}".format(product_id))

        SystemAppleServices._finishPaymentTransaction(transaction, product_id)

    @staticmethod
    def _cbPaymentFailed(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionFailed) payment failed """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment purchase Failed {}".format(product_id))

        Notification.notify(Notificator.onPayFailed, product_id)
        Notification.notify(Notificator.onPayComplete, product_id)
        transaction.finish()

    @staticmethod
    def _cbPaymentRestored(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionRestored) purchased product """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Product Restored {}".format(product_id))

        SystemAppleServices._finishProductRestoreTransaction(transaction, product_id)

    @staticmethod
    def _cbPaymentDeferred(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionDeferred) something went wrong during purchase """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment Deferred {}".format(product_id))

    @staticmethod
    def _cbPaymentQueueShouldShowPriceConsent(transaction):
        """
            (CALLBACK onPaymentQueueShouldShowPriceConsent)
            Sent if there is a pending price consent confirmation from the App Store for the current user.
        Return YES to immediately show the price consent UI.
        Return NO if you intend to show it at a later time. Defaults to YES.
            This may be called at any time that you have transaction observers on the payment queue,
        so make sure to set the delegate before adding any transaction observers
        if you intend to implement this method.
        """
        _Log("[InAppPurchase] (callback) _cbPaymentQueueShouldShowPriceConsent: {}".format(transaction))

    @staticmethod
    def _cbPaymentQueueShouldContinueTransaction():
        """ (CALLBACK onPaymentQueueShouldContinueTransaction)
            Sent when the storefront changes while a payment is processing. """
        _Log("[InAppPurchase] (callback) _cbPaymentQueueShouldContinueTransaction")

    @staticmethod
    def _finishPaymentTransaction(transaction, product_id):
        with TaskManager.createTaskChain(Name="ApplePaymentFinisher_%s" % product_id) as tc:
            with tc.addParallelTask(2) as (reward, complete):
                reward.addListener(Notificator.onGameStoreSentRewards, Filter=lambda prod_id, _: prod_id == product_id)
                complete.addNotify(Notificator.onPaySuccess, product_id)
                complete.addNotify(Notificator.onPayComplete, product_id)

            tc.addFunction(transaction.finish)

    @staticmethod
    def _finishProductRestoreTransaction(transaction, product_id):
        with TaskManager.createTaskChain(Name="AppleProductRestoreFinisher_%s" % product_id) as tc:
            with tc.addParallelTask(2) as (response, request):
                response.addListener(Notificator.onPayComplete, Filter=lambda prod_id: prod_id == product_id)
                # SystemMonetization sends onPayComplete when done
                request.addNotify(Notificator.onProductAlreadyOwned, product_id)

            tc.addFunction(transaction.finish)

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab("AppleServices"):
            return
        if any([self.b_plugins["GameCenter"], self.b_plugins["Review"], self.b_plugins["InAppPurchase"]]) is False:
            return

        tab = Mengine.addDevToDebugTab("AppleServices")
        widgets = []

        # achievements
        if self.b_plugins["GameCenter"] is True:
            def _send_achievement(text):
                """ input text allow 2 words separated by space:
                        first word - achievement_id
                        second optional word - is percentage digits from 0 to 100 """
                params = text.split(" ")
                achievement_name = params[0]
                percent_complete = int(params[1]) if len(params) > 1 else 100
                self._sendAchievementToGameCenter(achievement_name, percent_complete)

            w_achievement = Mengine.createDevToDebugWidgetCommandLine("send_achievement")
            w_achievement.setTitle("Send achievement to GameCenter")
            w_achievement.setPlaceholder("syntax: <achievement_id> [0-100]")
            w_achievement.setCommandEvent(_send_achievement)
            widgets.append(w_achievement)

        # purchases
        if self.b_plugins["InAppPurchase"] is True:
            w_restore = Mengine.createDevToDebugWidgetButton("restore_purchases")
            w_restore.setTitle("Restore Purchases")
            w_restore.setClickEvent(self.restorePurchases)
            widgets.append(w_restore)

            w_buy = Mengine.createDevToDebugWidgetCommandLine("buy")
            w_buy.setTitle("Buy product")
            w_buy.setPlaceholder("syntax: <prod_id>")
            w_buy.setCommandEvent(self.pay)
            widgets.append(w_buy)

        # rateApp
        if self.b_plugins["Review"] is True:
            w_rate = Mengine.createDevToDebugWidgetButton("rate_app")
            w_rate.setTitle("Show Rate App window")
            w_rate.setClickEvent(self.rateApp)
            widgets.append(w_rate)

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        if Mengine.hasDevToDebugTab("AppleServices"):
            Mengine.removeDevToDebugTab("AppleServices")
