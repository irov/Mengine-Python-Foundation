from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.MonetizationManager import MonetizationManager


class PaymentProvider(BaseProvider):
    s_allowed_methods = [
        "pay",
        "restorePurchases",
        "queryProducts",
        "canUserMakePurchases"
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
        products_id = MonetizationManager.getProductsInfo().keys()
        return PaymentProvider._call("queryProducts", products_id)

    @staticmethod
    def queryProductsNotFoundCb():
        Notification.notify(Notificator.onProductsUpdateDone)

    @staticmethod
    def canUserMakePurchases():
        return bool(PaymentProvider._call("canUserMakePurchases"))


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
        prod_params = MonetizationManager.getProductInfo(product_id)

        Trace.msg("DUMMY success pay {} ({})".format(product_id, prod_params))
        Notification.notify(Notificator.onPaySuccess, product_id)

    @staticmethod
    def restorePurchases():
        Trace.msg("DUMMY restorePurchases - no actions")

    @staticmethod
    def queryProducts():
        Trace.msg("DUMMY queryProducts - no actions, products are the same")
        Notification.notify(Notificator.onProductsUpdateDone)

    @staticmethod
    def canUserMakePurchases():
        return True


