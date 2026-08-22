from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Foundation.Providers.RateAppProvider import RateAppProvider
from Foundation.Providers.PaymentProvider import PaymentProvider
from Foundation.Providers.ProductsProvider import ProductsProvider
from Foundation.Providers.AchievementsProvider import AchievementsProvider
from Foundation.Providers.ConsentProvider import ConsentProvider
from Foundation.Providers.LeaderboardProvider import LeaderboardProvider
from Foundation.TaskManager import TaskManager

_Log = SimpleLogger("SystemiOSServices", option="ios")

PLUGIN_GAME_CENTER = "iOSGameCenterPlugin"
PLUGIN_STORE_REVIEW = "iOSStoreReviewPlugin"
PLUGIN_IN_APP_PURCHASE = "iOSStoreInAppPurchasePlugin"
PLUGIN_USER_MESSAGING_PLATFORM = "iOSUserMessagingPlatformPlugin"

class SystemiOSServices(System):
    """
        How to connect to the GameCenter:
            1. setGameCenterConnectProvider()
            2. connectToGameCenter()
    """

    b_plugins = {
        PLUGIN_GAME_CENTER: Mengine.isAvailablePlugin(PLUGIN_GAME_CENTER),
        PLUGIN_STORE_REVIEW: Mengine.isAvailablePlugin(PLUGIN_STORE_REVIEW),
        PLUGIN_IN_APP_PURCHASE: Mengine.isAvailablePlugin(PLUGIN_IN_APP_PURCHASE),
        PLUGIN_USER_MESSAGING_PLATFORM: Mengine.isAvailablePlugin(PLUGIN_USER_MESSAGING_PLATFORM)
    }

    _GameCenter_authenticated = False
    _GameCenter_synchronized = False
    _GameCenter_provider_status = False
    _InAppPurchase_provider_status = False
    _can_use_payment = False

    _products = {}
    EVENT_PRODUCTS_RESPONDED = Event("iOSInAppPurchaseProductsResponded")
    _restore_in_progress = False
    _restore_queue_finished = False
    _restore_pending_transactions = 0

    def _onInitialize(self):
        if self.b_plugins[PLUGIN_IN_APP_PURCHASE] is True:
            if self.canUserMakePurchases() is True:
                SystemiOSServices._can_use_payment = True
                self.setInAppPurchaseProvider()

        if self.b_plugins[PLUGIN_STORE_REVIEW] is True:
            RateAppProvider.setProvider("iOS", dict(rateApp=self.rateApp))

        if self.b_plugins[PLUGIN_USER_MESSAGING_PLATFORM] is True:
            ConsentProvider.setProvider("iOS", dict(
                ShowConsentFlow=self.showConsentFlow,
                IsConsentFlow=self.isConsentFlow,
            ))

        if self.b_plugins[PLUGIN_GAME_CENTER] is True:
            SystemiOSServices.setGameCenterConnectProvider()
            SystemiOSServices.connectToGameCenter()

            AchievementsProvider.setProvider("iOS", dict(
                unlockAchievement=self.unlockAchievement,
                setAchievementProgress=self.setAchievementProgress,
            ))

            LeaderboardProvider.setProvider("iOS", dict(
                submitLeaderboardScore=self.submitLeaderboardScore,
                showLeaderboard=self.showLeaderboard,
            ))

        # todo: promocodes handling in onRequestPromoCodeResult

        self.__addDevToDebug()

    def _onFinalize(self):
        self.__remDevToDebug()

        if SystemiOSServices._GameCenter_provider_status is True:
            self.removeGameCenterConnectProvider()
        if SystemiOSServices._InAppPurchase_provider_status is True:
            self.removeInAppPurchaseProvider()

    # --- AppleGameCenter - connection ---------------------------------------------------------------------------------

    @staticmethod
    def setGameCenterConnectProvider():
        _Log("[GameCenter] set provider...", optional=True)
        SystemiOSServices._GameCenter_provider_status = True

    @staticmethod
    def removeGameCenterConnectProvider():
        _Log("[GameCenter] remove provider...", optional=True)
        SystemiOSServices._GameCenter_provider_status = False

    @staticmethod
    def connectToGameCenter():
        status = Mengine.iOSGameCenterConnect({
            "oniOSGameCenterAuthenticate": SystemiOSServices.__cbGameCenterAuthenticate,
            "oniOSGameCenterSynchronize": SystemiOSServices.__cbGameCenterSynchronize
        })  # check is request to GameCenter was sent
        # if True, cb provider will return bool that means player connected or not

        _Log("[GameCenter] CONNECT STATUS: {}".format("wait response" if status else "request sent failed!!"))

        return status

    @staticmethod
    def __cbGameCenterAuthenticate(status, *args):
        """ callback for oniOSGameCenterAuthenticate """
        _Log("[GameCenter] (callback) AUTHENTICATE: {} [{}] args: {}".format("successful" if status else "failed", status, args), force=True)

        SystemiOSServices._GameCenter_authenticated = status

        if status is True:
            Mengine.activateSemaphore("GameCenterAuthenticated")

    @staticmethod
    def __cbGameCenterSynchronize(status, *args):
        """ callback for oniOSGameCenterSynchronize """
        _Log("[GameCenter] (callback) SYNCHRONIZE: {} [{}] args: {}".format("successful" if status else "failed", status, args), force=True)

        SystemiOSServices._GameCenter_synchronized = status

    @staticmethod
    def isGameCenterConnected(report=False, on_status=False):
        b_status = SystemiOSServices._GameCenter_authenticated

        if report is True and on_status is b_status:
            _Log("[GameCenter] CONNECT STATUS: {}".format(b_status), err=not b_status)

        return b_status

    # --- AppleGameCenter - interaction --------------------------------------------------------------------------------

    @staticmethod
    def __cbGameCenterAchievementReporter(status, achievement_name, percent_complete, *args):
        _Log("[GameCenter] (callback) ACHIEVEMENTS status: {} [{}] achievement: {!r} percent: {} args: {}".format("success" if status else "failed", status, achievement_name, percent_complete, args))
        return status

    @staticmethod
    def unlockAchievement(achievement_name):
        return SystemiOSServices._sendAchievementToGameCenter(achievement_name, percent_complete=100.0)

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

        return SystemiOSServices._sendAchievementToGameCenter(achievement_name, percent_complete=percent)

    @staticmethod
    def _sendAchievementToGameCenter(achievement_name, percent_complete):
        _Log("[GameCenter] SEND ACHIEVEMENT {!r} (complete {}%%)...".format(achievement_name, percent_complete), force=True)

        if SystemiOSServices.isGameCenterConnected(report=True) is False:
            Trace.log("System", 0, "Plugin '{}' fail to send achievement - Game Center is not connected!".format(PLUGIN_GAME_CENTER))
            return

        Mengine.iOSGameCenterReportAchievement(achievement_name, percent_complete,
                                                 SystemiOSServices.__cbGameCenterAchievementReporter,
                                                 achievement_name, percent_complete)

    @staticmethod
    def checkGameCenterAchievement(achievement_name):
        if SystemiOSServices.isGameCenterConnected(report=True) is False:
            return False

        b_check = Mengine.iOSGameCenterCheckAchievement(achievement_name)
        _Log("[GameCenter] CHECK ACHIEVEMENT {!r} RESULT: {}".format(achievement_name, b_check), force=True)
        return b_check

    # --- Leaderboard -------------------------------------------------------------------------------------------------

    @staticmethod
    def __cbGameCenterLeaderboardReporter(status, leaderboard_id, score, *args):
        _Log("[GameCenter] (callback) LEADERBOARD status: {} [{}] leaderboard_id: {!r} score: {} args: {}"
             .format("success" if status else "failed", status, leaderboard_id, score, args), force=True)
        return status

    @staticmethod
    def submitLeaderboardScore(leaderboard_id, score):
        _Log("[Leaderboard] submitLeaderboardScore {!r} {}...".format(leaderboard_id, score), force=True)

        if SystemiOSServices.isGameCenterConnected(report=True) is False:
            Trace.log("System", 0, "Plugin '{}' fail to submit leaderboard score - Game Center is not connected!"
                      .format(PLUGIN_GAME_CENTER))
            return False

        status = Mengine.iOSGameCenterReportScore(
            leaderboard_id,
            score,
            SystemiOSServices.__cbGameCenterLeaderboardReporter,
            leaderboard_id,
            score
        )

        if status is False:
            Trace.log("System", 0, "Plugin '{}' fail to submit leaderboard score '{}' ({})"
                      .format(PLUGIN_GAME_CENTER, leaderboard_id, score))

        return status

    @staticmethod
    def showLeaderboard(leaderboard_id):
        _Log("[Leaderboard] showLeaderboard {!r} is not supported by iOSGameCenter plugin".format(leaderboard_id), force=True, err=True)
        return False

    # --- Rate us ------------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        _Log("[Reviews] rateApp...", force=True)
        Mengine.iOSStoreReviewLaunchTheInAppReview()
        Notification.notify(Notificator.onAppRated)

    # --- Consent ------------------------------------------------------------------------------------------------------

    @staticmethod
    def showConsentFlow():
        Mengine.iOSUserMessagingPlatformShowConsentFlow()

        return True

    @staticmethod
    def isConsentFlow():
        return Mengine.iOSUserMessagingPlatformIsConsentFlowUserGeographyGDPR()

    # --- In-App Purchases ---------------------------------------------------------------------------------------------

    @staticmethod
    def canUserMakePurchases():
        """ returns True if user could do purchases (not a child) or False, if not """
        status = Mengine.iOSStoreInAppPurchaseCanMakePayments()
        _Log("[InAppPurchase] Can user make purchases? {}".format(status), optional=True)
        SystemiOSServices._can_use_payment = status
        return status

    @staticmethod
    def setInAppPurchaseProvider():
        """ setup payment callbacks """
        _Log("[InAppPurchase] set provider...", optional=True)
        Mengine.iOSStoreInAppPurchaseSetPaymentTransactionProvider({
            "onPaymentQueueUpdatedTransactionPurchasing": SystemiOSServices._cbPaymentPurchasing,
            "onPaymentQueueUpdatedTransactionPurchased": SystemiOSServices._cbPaymentPurchased,
            "onPaymentQueueUpdatedTransactionFailed": SystemiOSServices._cbPaymentFailed,
            "onPaymentQueueUpdatedTransactionRestored": SystemiOSServices._cbPaymentRestored,
            "onPaymentQueueUpdatedTransactionDeferred": SystemiOSServices._cbPaymentDeferred,
            "onPaymentQueueRestoreCompletedTransactionsFinished": SystemiOSServices._cbRestoreFinished,
            "onPaymentQueueRestoreCompletedTransactionsFailed": SystemiOSServices._cbRestoreFailed,
        })

        PaymentProvider.setProvider("iOS", dict(
            pay=SystemiOSServices.pay,
            restorePurchases=SystemiOSServices.restorePurchases,
            isOwnedInAppProduct=SystemiOSServices.isOwnedInAppProduct,
        ))

        _Log("[InAppPurchase] AppleStoreInAppPurchase is ready", optional=True)
        consumableIds, nonconsumableIds = ProductsProvider.getQueryProductIds()
        SystemiOSServices.requestProducts(consumableIds, nonconsumableIds)

        SystemiOSServices._InAppPurchase_provider_status = True

    @staticmethod
    def removeInAppPurchaseProvider():
        """ finish InAppPurchase callbacks provider """
        _Log("[InAppPurchase] remove provider...", optional=True)
        Mengine.iOSStoreInAppPurchaseRemovePaymentTransactionProvider()
        SystemiOSServices._InAppPurchase_provider_status = False

    @staticmethod
    def requestProducts(consumableIds, nonconsumableIds):
        _Log("[InAppPurchase] request product details for consumable: {} nonconsumable: {}".format(consumableIds, nonconsumableIds), optional=True)
        Mengine.iOSStoreInAppPurchaseRequestProducts(consumableIds, nonconsumableIds, {
            "onProductResponse": SystemiOSServices._cbProductResponse,
            "onProductFinish": SystemiOSServices._cbProductFinish,
            "onProductFail": SystemiOSServices._cbProductFail,
        })

    @staticmethod
    def restorePurchases():
        """ returns list of purchased products via cb _cbPaymentRestored """
        _Log("[InAppPurchase] restore purchases...", optional=True)
        SystemiOSServices._restore_in_progress = True
        SystemiOSServices._restore_queue_finished = False
        SystemiOSServices._restore_pending_transactions = 0
        Mengine.iOSStoreInAppPurchaseRestoreCompletedTransactions()

    @staticmethod
    def isOwnedInAppProduct(product_id):
        """
            Check if product with `product_id` is owned by user.
            Returns True if product is owned, False if not.
        """
        _Log("[InAppPurchase] isOwnedInAppProduct {!r}...".format(product_id), optional=True)
        return Mengine.iOSStoreInAppPurchaseIsOwnedProduct(product_id)

    @staticmethod
    def pay(product_id):
        _Log("[InAppPurchase] pay {!r}...".format(product_id), optional=True)

        if SystemiOSServices._can_use_payment is False:
            Notification.notify(Notificator.onPayFailed, product_id)
            Notification.notify(Notificator.onPayComplete, product_id)
            Trace.log("System", 0, "This user can't use payment (product_id={})".format(product_id))
            return

        product = SystemiOSServices._products.get(product_id)
        if product is None:
            Notification.notify(Notificator.onPayFailed, product_id)
            Notification.notify(Notificator.onPayComplete, product_id)
            Trace.log("System", 0, "Product with id {} not found in responded products {}!!!".format(product_id, list(SystemiOSServices._products.keys())))
            return

        Mengine.iOSStoreInAppPurchasePurchaseProduct(product)

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

            SystemiOSServices._products[product_id] = product

        currency = products[0].getProductCurrencyCode()
        Notification.notify(Notificator.onProductsUpdate, game_products, currency)

    @staticmethod
    def _cbProductFinish(request):
        """ (CALLBACK) Product Response Finish"""
        _Log("[InAppPurchase] (callback) Product Response Finish")
        SystemiOSServices.EVENT_PRODUCTS_RESPONDED(True)

    @staticmethod
    def _cbProductFail(request):
        """ (CALLBACK) Product Response Fail"""
        _Log("[InAppPurchase] (callback) Product Response Fail", err=True)
        SystemiOSServices.EVENT_PRODUCTS_RESPONDED(False)

    @staticmethod
    def _cbPaymentPurchasing(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionPurchasing) start purchase process """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment Purchasing start {}".format(product_id))

    @staticmethod
    def _cbPaymentPurchased(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionPurchased) payment complete """
        product_id = str(transaction.getProductIdentifier())
        transaction_id = transaction.getTransactionIdentifier()

        if transaction_id is None:
            raise RuntimeError("StoreKit returned purchase without transaction identifier for {!r}".format(product_id))

        transaction_id = str(transaction_id)
        _Log("[InAppPurchase] (callback) Payment Purchased (success) {}".format(product_id))

        Notification.notify(Notificator.onPayTransaction, product_id, transaction_id)
        SystemiOSServices._finishPaymentTransaction(transaction, product_id)

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

        if SystemiOSServices._restore_in_progress is True:
            SystemiOSServices._restore_pending_transactions += 1

        SystemiOSServices._finishProductRestoreTransaction(transaction, product_id)

    @staticmethod
    def _cbRestoreFinished():
        _Log("[InAppPurchase] (callback) Restore transactions queue finished")
        SystemiOSServices._restore_queue_finished = True
        SystemiOSServices._tryCompleteRestore()

    @staticmethod
    def _cbRestoreFailed():
        _Log("[InAppPurchase] (callback) Restore transactions queue failed", err=True, force=True)
        SystemiOSServices._restore_queue_finished = True
        SystemiOSServices._tryCompleteRestore()

    @staticmethod
    def _tryCompleteRestore():
        if SystemiOSServices._restore_in_progress is False:
            return
        if SystemiOSServices._restore_queue_finished is False:
            return
        if SystemiOSServices._restore_pending_transactions != 0:
            return

        SystemiOSServices._restore_in_progress = False
        Notification.notify(Notificator.onRestorePurchasesDone)

    @staticmethod
    def _completeRestoreTransaction():
        if SystemiOSServices._restore_in_progress is False:
            return

        SystemiOSServices._restore_pending_transactions -= 1
        SystemiOSServices._tryCompleteRestore()

    @staticmethod
    def _cbPaymentDeferred(transaction):
        """ (CALLBACK onPaymentQueueUpdatedTransactionDeferred) something went wrong during purchase """
        product_id = str(transaction.getProductIdentifier())
        _Log("[InAppPurchase] (callback) Payment Deferred {}".format(product_id))
        Notification.notify(Notificator.onPayPending, product_id)
        Notification.notify(Notificator.onPayComplete, product_id)

    @staticmethod
    def _finishPaymentTransaction(transaction, product_id):
        with TaskManager.createTaskChain(Global=True) as tc:
            with tc.addParallelTask(2) as (reward, complete):
                reward.addListener(Notificator.onPayRewardHandled, Filter=lambda prod_id: prod_id == product_id)
                complete.addNotify(Notificator.onPaySuccess, product_id)
                complete.addNotify(Notificator.onPayComplete, product_id)

            tc.addFunction(transaction.finish)

    @staticmethod
    def _finishProductRestoreTransaction(transaction, product_id):
        with TaskManager.createTaskChain(Global=True) as tc:
            with tc.addParallelTask(2) as (response, request):
                response.addListener(
                    Notificator.onPayRewardHandled,
                    Filter=lambda prod_id: prod_id == product_id)
                request.addNotify(Notificator.onProductAlreadyOwned, product_id)

            tc.addFunction(transaction.finish)
            tc.addFunction(SystemiOSServices._completeRestoreTransaction)

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab("iOSServices"):
            return
        if any([self.b_plugins[PLUGIN_GAME_CENTER], self.b_plugins[PLUGIN_STORE_REVIEW], self.b_plugins[PLUGIN_IN_APP_PURCHASE]]) is False:
            return

        tab = Mengine.addDevToDebugTab("iOSServices")
        widgets = []

        # achievements
        if self.b_plugins[PLUGIN_GAME_CENTER] is True:
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
        if self.b_plugins[PLUGIN_IN_APP_PURCHASE] is True:
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
        if self.b_plugins[PLUGIN_STORE_REVIEW] is True:
            w_rate = Mengine.createDevToDebugWidgetButton("rate_app")
            w_rate.setTitle("Show Rate App window")
            w_rate.setClickEvent(self.rateApp)
            widgets.append(w_rate)

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        if Mengine.hasDevToDebugTab("iOSServices"):
            Mengine.removeDevToDebugTab("iOSServices")
