from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.Providers.ProductsProvider import ProductsProvider


class PaymentProvider(BaseProvider):
    s_allowed_methods = [
        "pay",
        "restorePurchases",
        "queryProducts",
        "canUserMakePurchases",
        "completeOrder",
    ]

    @staticmethod
    def _setDevProvider():
        DummyPayment.setProvider()

    @staticmethod
    def pay(product_id):
        """ starts payment process,
             - onPaySuccess prod_id: all ok
             - onPayFailed prod_id: error """
        return PaymentProvider._call("pay", product_id)

    @staticmethod
    def restorePurchases():
        """ check player previous non-consumable purchases and call onPaySuccess for each of them """
        return PaymentProvider._call("restorePurchases")

    @staticmethod
    def queryProducts():
        """ query products from provider
            - onProductsUpdate dict: when we got products from provider
            - onProductsUpdateDone: when update complete """
        products_id = ProductsProvider.getQueryProductIds()
        if products_id is None:
            Trace.log("Provider", 0, "ProductsProvider.getQueryProductIds return None - queryProducts fail")
            return
        if len(products_id) == 0:
            Trace.log("Provider", 0, "ProductsProvider.queryProducts got empty products_id list!")
            return
        return PaymentProvider._call("queryProducts", products_id)

    @staticmethod
    def _queryProductsNotFoundCb():
        Notification.notify(Notificator.onProductsUpdateDone)

    @staticmethod
    def canUserMakePurchases():
        return bool(PaymentProvider._call("canUserMakePurchases"))

    @staticmethod
    def _canUserMakePurchasesNotFoundCb():
        return True

    @staticmethod
    def completeOrder(order_id):
        return bool(PaymentProvider._call("completeOrder", order_id))


class DummyPayment(object):

    @staticmethod
    def setProvider():
        PaymentProvider.setProvider("Dummy", dict(
            pay=DummyPayment.pay,
            restorePurchases=DummyPayment.restorePurchases,
            queryProducts=DummyPayment.queryProducts,
            canUserMakePurchases=DummyPayment.canUserMakePurchases
        ))

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
    def queryProducts(product_ids):
        Trace.msg("DUMMY queryProducts {} - no actions, products are the same".format(product_ids))
        Notification.notify(Notificator.onProductsUpdateDone)

    @staticmethod
    def canUserMakePurchases():
        Trace.msg("DUMMY user CAN make purchases")
        return True

    @staticmethod
    def completeOrder(order_id):
        Trace.msg("DUMMY completeOrder {!r}".format(order_id))
        return True


