from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.Providers.ProductsProvider import ProductsProvider


class PaymentProvider(BaseProvider):
    s_allowed_methods = [
        "pay",
        "restorePurchases",
        "isOwnedInAppProduct"
    ]

    @staticmethod
    def _setDevProvider():
        DummyPayment.setProvider()

    @staticmethod
    def isBillingSupported():
        """ check if billing supported on current platform """
        return bool(PaymentProvider._call("isBillingSupported"))

    @staticmethod
    def pay(product_id):
        """ starts payment process,
             - onPaySuccess prod_id: all ok
             - onPayFailed prod_id: error """
        return PaymentProvider._call("pay", product_id)

    @staticmethod
    def restorePurchases():
        """ check player previous non-consumable purchases and call onPaySuccess for each of them
            when restore completed - sends onRestorePurchasesDone
        """
        return PaymentProvider._call("restorePurchases")

    @staticmethod
    def isOwnedInAppProduct(product_id):
        """ check if product is owned by user """
        return bool(PaymentProvider._call("isOwnedInAppProduct", product_id))


class DummyPayment(object):
    @staticmethod
    def setProvider():
        PaymentProvider.setProvider("Dummy", dict(
            isBillingSupported=DummyPayment.isBillingSupported,
            pay=DummyPayment.pay,
            restorePurchases=DummyPayment.restorePurchases,
            isOwnedInAppProduct=DummyPayment.isOwnedInAppProduct,
        ))

    @staticmethod
    def isBillingSupported():
        return False

    @staticmethod
    def pay(product_id):
        from Foundation.TaskManager import TaskManager

        if TaskManager.existTaskChain("DummyPaymentProcessing_{}".format(product_id)) is True:
            Trace.log("Provider", 0, "Payment {} already in processing...".format(product_id))
            return True

        prod_params = ProductsProvider.getProductInfo(product_id)

        success = Mengine.rand(100) >= 15    # 85% chance

        with TaskManager.createTaskChain(Name="DummyPaymentProcessing_{}".format(product_id)) as tc:
            tc.addPrint("DUMMY payment processing {!r} 3s... ({})".format(product_id, prod_params))
            tc.addDelay(3000)

            if success is True:
                tc.addPrint("DUMMY payment {!r} OK".format(product_id))
                tc.addNotify(Notificator.onPaySuccess, product_id)
            else:
                tc.addNotify(Notificator.onPayFailed, product_id)
            tc.addNotify(Notificator.onPayComplete, product_id)

        return True

    @staticmethod
    def restorePurchases():
        Trace.msg("DUMMY restorePurchases - no actions")
        Notification.notify(Notificator.onRestorePurchasesDone)

    @staticmethod
    def isOwnedInAppProduct(product_id):
        Trace.msg("DUMMY isOwnedInAppProduct {!r} - always False".format(product_id))
        return False


