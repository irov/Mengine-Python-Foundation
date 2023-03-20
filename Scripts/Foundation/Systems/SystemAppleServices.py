from Foundation.PolicyManager import PolicyManager
from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemAppleServices")

class SystemAppleServices(System):
    b_plugins = {
        "GameCenter": _PLUGINS.get("AppleGameCenter", False),
        "Review": _PLUGINS.get("AppleStoreReview", False),
        "Tracking": _PLUGINS.get("AppleAppTracking", False),
        "InAppPurchase": _PLUGINS.get("AppleStoreInAppPurchase", False),
    }

    b_GameCenter_authenticate = False
    b_GameCenter_synchronizate = False
    b_provider = False
    b_tracking = False

    _products = {}
    b_can_pay = False
    EVENT_PRODUCTS_RESPONDED = Event("AppleInAppPurchaseProductsResponded")

    # How to connect to GameCenter:
    # 1. setGameCenterConnectProvider()
    # 2. connectToGameCenter()

    def _onInitialize(self):
        self.__addDevToDebug()

        if self.b_plugins["InAppPurchase"] is True:
            if self.canUserMakePurchases() is True:
                self.setInAppPurchaseProvider()
                self.updateProducts()

                PolicyManager.setPolicy("Purchase", "PolicyPurchaseAppleInApp")

    def _onFinalize(self):
        self.__remDevToDebug()

    def _onStop(self):
        self.removeGameCenterConnectProvider()
        self.removeInAppPurchaseProvider()

    # --- AppleGameCenter - connection ---------------------------------------------------------------------------------

    @staticmethod
    def setGameCenterConnectProvider():
        if SystemAppleServices.b_plugins["GameCenter"] is True:
            b_status = Mengine.appleGameCenterSetProvider({
                "onAppleGameCenterAuthenticate": SystemAppleServices.__cbGameCenterAuthenticate,
                "onAppleGameCenterSynchronizate": SystemAppleServices.__cbGameCenterSynchronizate
            })
            SystemAppleServices.b_provider = True
            _Log("GAME CENTER: set provider - {}".format("wait response!" if b_status else "not initialized"))
        else:
            _Log("GAME CENTER: set provider - plugin 'AppleGameCenter' not active")

    @staticmethod
    def removeGameCenterConnectProvider():
        if SystemAppleServices.b_plugins["GameCenter"] is True:
            if SystemAppleServices.b_provider is True:
                Mengine.appleGameCenterRemoveProvider()
                SystemAppleServices.b_provider = False
                _Log("GAME CENTER: removed provider")
            else:
                _Log("GAME CENTER: provider doesn't active")
        else:
            _Log("GAME CENTER: remove provider - plugin 'AppleGameCenter' not active")

    @staticmethod
    def connectToGameCenter():
        status = lambda b: "wait response" if b else "request sent failed"

        if SystemAppleServices.b_plugins["GameCenter"] is True:
            b_result = Mengine.appleGameCenterConnect()  # check is request to GameCenter was sent
            # if True, cb provider will return bool that means player connected or not

            PolicyManager.setPolicy("ExternalAchieveProgress", "PolicyExternalAchieveProgressAppleGameCenter")
        else:
            b_result = False

        _Log("GAME CENTER CONNECT STATUS: {}".format(status(b_result)))
        return b_result

    @staticmethod
    def __cbGameCenterAuthenticate(status, *args):
        descr = lambda b: "successful" if b else "failed"

        log_message = "GAME CENTER - cb AUTHENTICATE: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)

        SystemAppleServices.b_GameCenter_authenticate = status

    @staticmethod
    def __cbGameCenterSynchronizate(status, *args):
        descr = lambda b: "successful" if b else "failed"

        log_message = "GAME CENTER - cb SYNCHRONIZATE: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)

        SystemAppleServices.b_GameCenter_synchronizate = status

    @staticmethod
    def isGameCenterConnected(report=False, on_status=False):
        b_status = SystemAppleServices.b_GameCenter_authenticate

        if report is True and on_status is b_status:
            _Log("GAME CENTER CONNECT STATUS: {}".format(b_status), err=not b_status)

        return b_status

    # --- AppleGameCenter - interaction --------------------------------------------------------------------------------

    @staticmethod
    def __cbGameCenterAchievementReporter(status, achievement_name, percent_complete, *args):
        descr = lambda b: "success {!r} (complete {}%%)".format(achievement_name, percent_complete) if b else "game center not received last achievement"
        log_message = "GAME CENTER - cb ACHIEVEMENTS: {} [{}]".format(descr(status), status)
        log_message += " | args: {}".format(args) if args else ""
        _Log(log_message)
        return status

    @staticmethod
    def sendAchievementToGameCenter(achievement_name, percent_complete=100.0):
        SystemAppleServices.isGameCenterConnected(report=True)

        _Log("GAME CENTER: SEND ACHIEVEMENT {!r} (complete {}%%)...".format(achievement_name, percent_complete), force=True)
        if SystemAppleServices.b_plugins["GameCenter"] is False:
            return
        Mengine.appleGameCenterReportAchievement(achievement_name, percent_complete,
                                                 SystemAppleServices.__cbGameCenterAchievementReporter,
                                                 achievement_name, percent_complete)

    @staticmethod
    def checkGameCenterAchievement(achievement_name):
        SystemAppleServices.isGameCenterConnected(report=True)
        if SystemAppleServices.b_plugins["GameCenter"] is False:
            return True

        b_check = Mengine.appleGameCenterCheckAchievement(achievement_name)
        _Log("GAME CENTER: CHECK ACHIEVEMENT {!r} RESULT: {}".format(achievement_name, b_check), force=True)
        return b_check

    # --- AppleAppTracking ---------------------------------------------------------------------------------------------

    @staticmethod
    def __cbAppTrackingAuth(_status, _idfa, *args):
        log_message = "cbAppTrackingAuth : status={} idfa={}".format(_status, _idfa)
        log_message += " | args: {}".format(args) if len(args) > 0 else ""
        _Log(log_message)
        SystemAppleServices.b_tracking = _status

    @staticmethod
    def appTrackingAuthorization():
        if SystemAppleServices.b_plugins["Tracking"] is True:
            Mengine.appleAppTrackingAuthorization(SystemAppleServices.__cbAppTrackingAuth)
            _Log("Apple app tracking authorization...")
            return True
        return False

    # --- Rate us ------------------------------------------------------------------------------------------------------

    @staticmethod
    def rateApp():
        if SystemAppleServices.b_plugins["Review"] is False:
            Trace.log("System", 0, "SystemAppleServices try to rateApp, but plugin 'AppleStoreReview' is not active")
            return
        Mengine.appleStoreReviewLaunchTheInAppReview()
        Notification.notify(Notificator.onAppRated)
        _Log("[Reviews] rateApp...", force=True)

    # --- In-App Purchases ---------------------------------------------------------------------------------------------

    @staticmethod
    def canUserMakePurchases():
        """ returns True if user could do purchases (not a child) or False, if not """
        if SystemAppleServices.b_plugins["InAppPurchase"] is False:
            return False
        return Mengine.appleStoreInAppPurchaseCanMakePayments()

    @staticmethod
    def setInAppPurchaseProvider():
        """ setup payment callbacks """
        Mengine.appleStoreInAppPurchaseSetPaymentTransactionProvider({
            "onProductResponse": SystemAppleServices._cbProductResponse,
            "onProductFinish": SystemAppleServices._cbProductFinish,
            "onProductFail": SystemAppleServices._cbProductFail,
            "onPaymentUpdatedTransactionPurchasing": SystemAppleServices._cbPaymentPurchasing,
            "onPaymentUpdatedTransactionPurchased": SystemAppleServices._cbPaymentPurchased,
            "onPaymentUpdatedTransactionFailed": SystemAppleServices._cbPaymentFailed,
            "onPaymentUpdatedTransactionRestored": SystemAppleServices._cbPaymentRestored,
            "onPaymentUpdatedTransactionDeferred": SystemAppleServices._cbPaymentDeferred
        })

    @staticmethod
    def removeInAppPurchaseProvider():
        """ finish callbacks """
        if SystemAppleServices.b_plugins["InAppPurchase"] is False:
            return
        Mengine.appleStoreInAppPurchaseRemovePaymentTransactionProvider()

    @staticmethod
    def updateProducts():
        """ Must be called to get products and initialize payment """
        TaskManager.runAlias("AliasCurrentProductsCall", None, CallFunction=SystemAppleServices._requestProducts)

    @staticmethod
    def _requestProducts(products_ids):
        Mengine.appleStoreInAppPurchaseRequestProducts(products_ids)

    @staticmethod
    def restorePurchases():
        """ returns list of purchased products via cb _cbPaymentRestored """
        Mengine.appleStoreInAppPurchaseRestoreCompletedTransactions()

    @staticmethod
    def pay(product_id):
        if SystemAppleServices.b_can_pay is False:
            Notification.notify(Notificator.onPayFailed, product_id)
            Trace.log("System", 0, "This user can't use payment (product_id={})".format(product_id))
            return

        product = SystemAppleServices._products.get(product_id)
        if product is None:
            Notification.notify(Notificator.onPayFailed, product_id)
            Trace.log("System", 0, "Product with id {} not found in responded products!!!".format(product_id))
            return

        Mengine.appleStoreInAppPurchasePurchaseProduct(product)

    # callbacks

    @staticmethod
    def _cbProductResponse(products):
        _Log("(CALLBACK) Product Response: {}".format(products))
        for product in products:
            product_id = product.getProductIdentifier()
            SystemAppleServices._products[product_id] = product

    @staticmethod
    def _cbProductFinish():
        _Log("(CALLBACK) Product Response Finish")
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(True)
        SystemAppleServices.b_can_pay = True

    @staticmethod
    def _cbProductFail():
        _Log("(CALLBACK) Product Response Fail")
        SystemAppleServices.EVENT_PRODUCTS_RESPONDED(False)
        SystemAppleServices.b_can_pay = False

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
        transaction.finish()

    @staticmethod
    def _cbPaymentFailed(transaction):
        """ (CALLBACK) payment failed """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment purchase Failed {}".format(product_id))

        Notification.notify(Notificator.onPayFailed, product_id)
        transaction.finish()

    @staticmethod
    def _cbPaymentRestored(transaction):
        """ (CALLBACK) purchased product """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Restored {}".format(product_id))

        Notification.notify(Notificator.onPaySuccess, product_id)

        transaction.finish()

    @staticmethod
    def _cbPaymentDeferred(transaction):
        """ (CALLBACK) something went wrong during purchase """
        product_id = transaction.getProductIndetifier()
        _Log("(callback) Payment Deferred {}".format(product_id))

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab("AppleServices"):
            return
        if any([self.b_plugins["GameCenter"], self.b_plugins["Review"]]) is False:
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
                self.sendAchievementToGameCenter(achievement_name, percent_complete)

            w_achievement = Mengine.createDevToDebugWidgetCommandLine("send_achievement")
            w_achievement.setTitle("Send achievement to GameCenter")
            w_achievement.setPlaceholder("syntax: <achievement_id> [0-100]")
            w_achievement.setCommandEvent(_send_achievement)
            widgets.append(w_achievement)

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