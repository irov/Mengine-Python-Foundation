from Foundation.Providers.BaseProvider import BaseProvider


class ProductsProvider(BaseProvider):

    s_allowed_methods = [
        "getProductsInfo",
        "getProductReward",
        "getProductPrice",
        "getProductInfo",
        "hasProductInfo",
    ]

    @staticmethod
    def getProductsInfo():
        """ returns dict (key=product_id, value=instance)"""
        return ProductsProvider._call("getProductsInfo")

    @staticmethod
    def getProductReward(product_id):
        return ProductsProvider._call("getProductReward", product_id)

    @staticmethod
    def getProductPrice(product_id):
        """ returns float price """
        return ProductsProvider._call("getProductPrice", product_id)

    @staticmethod
    def getProductInfo(product_id):
        """ returns None or product instance """
        return ProductsProvider._call("getProductInfo", product_id)

    @staticmethod
    def hasProductInfo(product_id):
        """ returns True if product with that id exists """
        return bool(ProductsProvider._call("hasProductInfo", product_id))