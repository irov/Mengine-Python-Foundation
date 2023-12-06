from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Foundation.Providers.RatingAppProvider import RatingAppProvider
from Foundation.Providers.PaymentProvider import PaymentProvider
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from Notification import Notification


_Log = SimpleLogger("SystemAppleServices", option="apple")


class SystemAppleServices(System):
    b_plugins = {
        "GameCenter": _PLUGINS.get("AppleGameCenter", False),
        "Review": _PLUGINS.get("AppleStoreReview", False),
        "Tracking": _PLUGINS.get("AppleAppTracking", False),
        "InAppPurchase": _PLUGINS.get("AppleStoreInAppPurchase", False),
    }

    _GameCenter_authenticate = False
    _GameCenter_synchronizate = False
    _GameCenter_provider_status = False
    _InAppPurchase_provider_status = False
    _Tracking_status = False
    _can_use_payment = False

    _products = {}
    EVENT_PRODUCTS_RESPONDED = Event("AppleInAppPurchaseProductsResponded")

    # How to connect to GameCenter:
    # 1. setGameCenterConnectProvider()
    # 2. connectToGameCenter()

    def _onInitialize(self):
        if self.b_plugins["InAppPurchase"] is True:
            if self.canUserMakePurchases() is True:
                SystemAppleServices._can_use_payment = True
                self.setInAppPurchaseProvider()

                if Mengine.getConfigBool("Monetization", "AutoQueryProducts", True) is True:
                    PaymentProvider.queryProducts()
                else:
                    _Log("Auto query products disabled, do it manually in code")

        if self.b_plugins["Review"] is True:
            RatingAppProvider.setProvider("Apple", dict(rateApp=self.rateApp))

        if self.b_plugins["GameCenter"] is True:
            SystemAppleServices.setGameCenterConnectProvider()
            SystemAppleServices.connectToGameCenter()

            AchievementsProvider.setProvider("Apple", dict(
                unlockAchievement=self.unlockAchievement,
                setAchievementProgress=self.setAchievementProgress,
            ))

        if self.b_plugins["Tracking"] is True:
            SystemAppleServices.appTrackingAuthorization()

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
            _Log("[GameCenter] set provider - plugin 'AppleGameCenter' not active", err=True, force=True)
            return False

        b_status = Mengine.appleGameCenterSetProvider({
            "onAppleGameCenterAuthenticate": SystemAppleServices.__cbGameCenterAuthenticate,
            "onAppleGameCenterSynchronizate": SystemAppleServices.__cbGameCenterSynchronizate
        })
        SystemAppleServices._GameCenter_provider_status = b_status
        _Log("[GameCenter] set provider - {}".format("wait response!" if b_status else "not initialized"))

    @staticmethod
    def removeGameCenterConnectProvider():
        if SystemAppleServices._GameCenter_provider_status is False:
            _Log("[GameCenter] can't remove provider - not active", err=True)
            return

        Mengine.appleGameCenterRemoveProvider()
        SystemAppleServices._GameCenter_provider_status = False
        _Log("[GameCenter] removed provider")

    @staticmethod
    def connectToGameCenter():
        status = lambda b: "wait response" if b else "request sent failed"

        if SystemAppleServices.b_plugins["GameCenter"] is True:
            b_result = Mengine.appleGameCenterConnect()  # check is request to GameCenter was sent
            # if True, cb provider will return bool that means player connected or not
        else:
            b_result = False

        _Log("GAME CENTER CONNECT STATUS: {}".format(status(b_result)))
        return b_result

    @staticmethod
    def __cbGameCenterAuthenticate(status, *args):
        descr = lambda b: "successful" if b else "failed"

        log_message = "[GameCenter] (callback) AUTHENTICATE: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)

        SystemAppleServices._GameCenter_authenticate = status

    @staticmethod
    def __cbGameCenterSynchronizate(status, *args):
        descr = lambda b: "successful" if b else "failed"

        log_message = "[GameCenter] (callback) SYNCHRONIZE: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)

        SystemAppleServices._GameCenter_synchronizate = status

    @staticmethod
    def isGameCenterConnected(report=False, on_status=False):
        b_status = SystemAppleServices._GameCenter_authenticate

        if report is True and on_status is b_status:
            _Log("GAME CENTER CONNECT STATUS: {}".format(b_status), err=not b_status)

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
            Trace.log("System", 0, "Apple Service plugin 'GameCenter' fail to send achievement - Game Center is not connected!")
            return

        Mengine.appleGameCenterReportAchievement(achievement_name, percent_complete,
                                                 SystemAppleServices.__cbGameCenterAchievementReporter,
                                                 achievement_name, percent_complete)

    @staticmethod
    def checkGameCenterAchievement(achievement_name):
        if SystemAppleServices.b_plugins["GameCenter"] is False:
            Trace.log("System", 0, "Apple Service plugin 'GameCenter' is not active to check achievement {!r}".format(achievement_name))
            return False
        if SystemAppleServices.isGameCenterConnected(report=True) is False:
            return False

        b_check = Mengine.appleGameCenterCheckAchievement(achievement_name)
        _Log("[GameCenter] CHECK ACHIEVEMENT {!r} RESULT: {}".format(achievement_name, b_check), force=True)
        return b_check

    # --- AppleAppTracking ---------------------------------------------------------------------------------------------

    @staticmethod
    def __cbAppTrackingAuth(_status, _idfa, *args):
        log_message = "cbAppTrackingAuth : status={} idfa={}".format(_status, _idfa)
        log_message += " | args: {}".format(args) if len(args) > 0 else ""
        _Log(log_message)
        SystemAppleServices._Tracking_status = _status

    @staticmethod
    def appTrackingAuthorization():
        _Log("Apple app tracking authorization...")
        Mengine.appleAppTrackingAuthorization(SystemAppleServices.__cbAppTrackingAuth)

    # --- Rate us ------------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        if SystemAppleServices.b_plugins["Review"] is False:
            Trace.log("System", 0, "SystemAppleServices try to rateApp, but plugin 'AppleStoreReview' is not active")
            return
        _Log("[Reviews] rateApp...", force=True)
        Mengine.appleStoreReviewLaunchTheInAppReview()
        Notification.notify(Notificator.onAppRated)

    # --- In-App Purchases ---------------------------------------------------------------------------------------------

    @staticmethod
    def canUserMakePurchases():
        """ returns True if user could do purchases (not a child) or False, if not """
        status = Mengine.appleStoreInAppPurchaseCanMakePayments()
        SystemAppleServices._can_use_payment = status
        return status

    @staticmethod
    def setInAppPurchaseProvider():
        """ setup payment callbacks """
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
            queryProducts=SystemAppleServices.requestProducts,
            restorePurchases=SystemAppleServices.restorePurchases,
        ))
        SystemAppleServices._InAppPurchase_provider_status = True

    @staticmethod
    def removeInAppPurchaseProvider():
        """ finish InAppPurchase callbacks provider """

        if SystemAppleServices._InAppPurchase_provider_status is False:
            _Log("[InAppPurchase] can't remove provider - not active", err=True)
            return False

        Mengine.appleStoreInAppPurchaseRemovePaymentTransactionProvider()
        SystemAppleServices._InAppPurchase_provider_status = False
        _Log("[InAppPurchase] removed provider")

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
    def _cbProductResponse(products):
        """
            input: AppleStoreInAppPurchaseProductInterface[]

            .def( "getProductIdentifier", &AppleStoreInAppPurchaseProductInterface::getProductIdentifier )
            .def( "getProductTitle", &AppleStoreInAppPurchaseProductInterface::getProductTitle )
            .def( "getProductDescription", &AppleStoreInAppPurchaseProductInterface::getProductDescription )
            .def( "getProductCurrencyCode", &AppleStoreInAppPurchaseProductInterface::getProductCurrencyCode )
            .def( "getProductPriceFormatted", &AppleStoreInAppPurchaseProductInterface::getProductPriceFormatted )
            .def( "getProductPrice", &AppleStoreInAppPurchaseProductInterface::getProductPrice )

        """

        _Log("(CALLBACK) Product Response: {}".format([p.getProductIdentifier() for p in products]))

        game_products = {}

        for product in products:
            product_id = product.getProductIdentifier()

            params = {
                "price": round(product.getProductPriceFormatted(), 2),
                "descr": str(product.getProductDescription()),
                "name": str(product.getProductTitle())
            }
            game_products[product_id] = params

            SystemAppleServices._products[product_id] = product

        currency = products[0].getProductCurrencyCode()
        Notification.notify(Notificator.onProductsUpdate, game_products, currency)

    @staticmethod
    def _cbProductFinish():
        """ (CALLBACK) Product Response Finish"""
        _Log("(callback) Product Response Finish")
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(True)

    @staticmethod
    def _cbProductFail():
        """ (CALLBACK) Product Response Fail"""
        _Log("(callback) Product Response Fail", err=True)
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(False)

    @staticmethod
    def _cbPaymentPurchasing(transaction):
        """ (CALLBACK) start purchase process """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Purchasing start {}".format(product_id))

    @staticmethod
    def _cbPaymentPurchased(transaction):
        """ (CALLBACK) payment complete """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Purchased (success) {}".format(product_id))

        Notification.notify(Notificator.onPaySuccess, product_id)
        Notification.notify(Notificator.onPayComplete, product_id)
        transaction.finish()

    @staticmethod
    def _cbPaymentFailed(transaction):
        """ (CALLBACK) payment failed """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment purchase Failed {}".format(product_id))

        Notification.notify(Notificator.onPayFailed, product_id)
        Notification.notify(Notificator.onPayComplete, product_id)
        transaction.finish()

    @staticmethod
    def _cbPaymentRestored(transaction):
        """ (CALLBACK) purchased product """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Restored {}".format(product_id))

        Notification.notify(Notificator.onPaySuccess, product_id)
        Notification.notify(Notificator.onPayComplete, product_id)

        transaction.finish()

    @staticmethod
    def _cbPaymentDeferred(transaction):
        """ (CALLBACK) something went wrong during purchase """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Deferred {}".format(product_id))

    @staticmethod
    def _cbPaymentQueueShouldShowPriceConsent(transaction):
        """
            Sent if there is a pending price consent confirmation from the App Store for the current user.
        Return YES to immediately show the price consent UI.
        Return NO if you intend to show it at a later time. Defaults to YES.
            This may be called at any time that you have transaction observers on the payment queue,
        so make sure to set the delegate before adding any transaction observers
        if you intend to implement this method.
        """
        _Log("(callback) _cbPaymentQueueShouldShowPriceConsent: {}".format(transaction))

    @staticmethod
    def _cbPaymentQueueShouldContinueTransaction():
        """ Sent when the storefront changes while a payment is processing. """
        _Log("(callback) _cbPaymentQueueShouldContinueTransaction")

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

            w_update_products = Mengine.createDevToDebugWidgetButton("update_products")
            w_update_products.setTitle("Update products (update prices and prod params)")
            w_update_products.setClickEvent(PaymentProvider.queryProducts)
            widgets.append(w_update_products)

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