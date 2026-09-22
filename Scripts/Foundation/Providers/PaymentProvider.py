from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.Providers.ProductsProvider import ProductsProvider


class PaymentProvider(BaseProvider):
    s_allowed_methods = [
        "pay",
        "restorePurchases",
        "isOwnedInAppProduct",
        "querySubscriptionStatus",
        "openSubscriptionManagement",
    ]

    @classmethod
    def getTaskSourceInjections(cls):
        return (
            ("addPaymentProviderPay", "TaskFunction", dict(Fn=cls.pay)),
            ("addPaymentProviderRestorePurchases", "TaskFunction", dict(Fn=cls.restorePurchases)),
        )

    @staticmethod
    def _setDevProvider():
        DummyPayment.setProvider()

    @staticmethod
    def pay(product_id):
        """ starts payment process,
             - onPaySuccess prod_id: all ok
             - onPayFailed prod_id: error """
        from Foundation.Systems.SystemMonetization import SystemMonetization
        if SystemMonetization.checkPurchaseReady(product_id) is False:
            return False
        return PaymentProvider._call("pay", product_id)

    @staticmethod
    def restorePurchases():
        """ check player previous non-consumable purchases and call onPaySuccess for each of them
            when restore completed - sends onRestorePurchasesResult(successful)
        """
        return PaymentProvider._call("restorePurchases")

    @staticmethod
    def isOwnedInAppProduct(product_id):
        """ check if product is owned by user """
        return bool(PaymentProvider._call("isOwnedInAppProduct", product_id))

    @staticmethod
    def querySubscriptionStatus(product_id, callback):
        """Return True when the provider accepts responsibility for the callback."""
        return PaymentProvider._call("querySubscriptionStatus", product_id, callback)

    @staticmethod
    def openSubscriptionManagement(product_id):
        return bool(PaymentProvider._call("openSubscriptionManagement", product_id))

class DummyPayment(object):
    @staticmethod
    def setProvider():
        PaymentProvider.setProvider("Dummy", dict(
            pay=DummyPayment.pay,
            restorePurchases=DummyPayment.restorePurchases,
            isOwnedInAppProduct=DummyPayment.isOwnedInAppProduct,
        ))

    @staticmethod
    def pay(product_id):
        from Foundation.TaskManager import TaskManager

        if TaskManager.existTaskChain("DummyPaymentProcessing_{}".format(product_id)) is True:
            Trace.log("Provider", 0, "Payment {} already in processing...".format(product_id))
            return True

        prod_params = ProductsProvider.getProductInfo(product_id)

        transaction_id = "dummy:" + Mengine.makeUID(32)
        success = Mengine.rand(100) >= 15    # 85% chance

        with TaskManager.createTaskChain(Name="DummyPaymentProcessing_{}".format(product_id)) as tc:
            tc.addPrint("DUMMY payment processing {!r} 3s... ({})".format(product_id, prod_params))
            tc.addDelay(3000)

            if success is True:
                tc.addPrint("DUMMY payment {!r} OK".format(product_id))
                successful_holder = Holder(False)
                def _filter(rewarded_id, rewarded_transaction_id, successful):
                    if rewarded_id != product_id or rewarded_transaction_id != transaction_id:
                        return False
                    successful_holder.set(successful)
                    return True

                with tc.addParallelTask(2) as (response, request):
                    response.addListener(Notificator.onPayRewardResult, Filter=_filter)
                    request.addNotify(Notificator.onPaySuccess, product_id, transaction_id)
                with tc.addIfTask(successful_holder.get) as (applied, failed):
                    applied.addNotify(Notificator.onPayFinalized, product_id, transaction_id)
                    failed.addNotify(Notificator.onPayFailed, product_id)
            else:
                tc.addNotify(Notificator.onPayFailed, product_id)
            tc.addNotify(Notificator.onPayComplete, product_id)

        return True

    @staticmethod
    def restorePurchases():
        Trace.msg("DUMMY restorePurchases - no actions")
        Notification.notify(Notificator.onRestorePurchasesResult, True)

    @staticmethod
    def isOwnedInAppProduct(product_id):
        Trace.msg("DUMMY isOwnedInAppProduct {!r} - always False".format(product_id))
        return False


