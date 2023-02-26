import json

from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager
from Foundation.Utils import getCurrentPlatformParams, getCurrentPublisher, getCurrentBusinessModel
from Foundation.Utils import isCollectorEdition
from Notification import Notification

class CurrencyManager(object):
    """ Util for MonetizationManager"""

    s_current_currency = None

    CURRENCY_TEXTS_IDS = {# find them in Framework Texts.xml
        "ID_CURRENCY_DOLLAR": ["USD"], "ID_CURRENCY_POUND": ["GBP"], "ID_CURRENCY_EURO": ["EUR"], "ID_CURRENCY_HRYVNIA": ["UAH"], "ID_CURRENCY_YEN": ["CNY", "JPY"], }

    @classmethod
    def addCurrencyCode(cls, currency_code, text_id):
        cls.CURRENCY_TEXTS_IDS.setdefault(text_id, [])
        if currency_code in cls.CURRENCY_TEXTS_IDS[text_id]:
            return
        cls.CURRENCY_TEXTS_IDS[text_id].append(currency_code)

    @staticmethod
    def setCurrentCurrencyCode(currency_code):
        """ set current ISO 4217 currency code. `currency_code` must be str! """
        if currency_code is None:
            CurrencyManager.s_current_currency = None
            return True
        if isinstance(currency_code, str) is False:
            Trace.log("Manager", 0, "setCurrentCurrencyCode {!r} must be str, not {}".format(currency_code, type(currency_code)))
            return False
        if len(currency_code) != 3:
            Trace.log("Manager", 0, "setCurrentCurrencyCode {!r} length must be 3".format(currency_code))
            return False

        if currency_code not in CurrencyManager._getCurrencyTextIds():
            if _DEVELOPMENT is True:
                Trace.msg_err("CurrencyManager: your currency {!r} has no text id".format(currency_code))

        CurrencyManager.s_current_currency = currency_code.upper()
        return True

    @staticmethod
    def getCurrentCurrencyCode():
        return CurrencyManager.s_current_currency

    @staticmethod
    def _getCurrencyTextIds():
        """ util for getCurrentCurrencySymbol. Returns: dict = {currency_code: currency_text_id} """
        currency_text_ids = {}
        for text_id, currencies in CurrencyManager.CURRENCY_TEXTS_IDS.items():
            for currency in currencies:
                currency_text_ids[currency] = text_id
        return currency_text_ids

    @staticmethod
    def getCurrentCurrencySymbol(only_text_id=False, code_if_none=True):
        """ :returns: currency symbol or None if it doesn't exist
            @param only_text_id: (bool) return text_id instead of symbol, if it exists
            @param code_if_none: (bool) return code if symbol is not setup """

        cur_currency = CurrencyManager.getCurrentCurrencyCode()

        currency_text_ids = CurrencyManager._getCurrencyTextIds()
        symbol_text_id = currency_text_ids.get(cur_currency, None)

        if symbol_text_id is None:
            if code_if_none is True:
                return cur_currency
            return None

        if Menge.existText(symbol_text_id) is False:
            if _DEVELOPMENT is True:
                Trace.log("Manager", 1, "textId {} not found for currency {}".format(symbol_text_id, cur_currency))
            if code_if_none is True:
                return cur_currency
            return None

        if only_text_id is True:
            return symbol_text_id

        symbol = Menge.getTextFromID(symbol_text_id)
        return symbol

class MonetizationManager(Manager, CurrencyManager):
    __PARAMS_TABLE_NAMES = {"general": "MonetizationGeneral", "store_items": "StoreItems", "store_images": "StoreImages", "products_info": "ProductsInfo", "special_promotions": "SpecialPromotions", "redirect": "MonetizationRedirect"}

    s_params = {}  # key
    s_cards = {}  # card_id
    s_images = {}  # card_id
    s_products = {}  # prod_id
    s_specials = {}  # prod_id

    s_components = {}

    s_alias_products = {}  # alias_prod_id

    class __Param(object):
        if _DEVELOPMENT is True:
            def __repr__(self):
                return "<{}: {}>".format(self.__class__.__name__, self.__dict__)

    class SpecialPromoParam(__Param):
        DEFAULT_TEXT_ID = "ID_EMPTY_TEXT"

        def __init__(self, record):
            self.id = MonetizationManager.getRecordValue(record, "ProductID", cast=str)
            self.tag = MonetizationManager.getRecordValue(record, "Tag", cast=str)
            self.limit_delay = MonetizationManager.getRecordValue(record, "LimitDelay")
            self.offer_delay = MonetizationManager.getRecordValue(record, "OfferDelay")
            product_params = MonetizationManager.getProductInfo(self.id)
            self.discount = MonetizationManager.getRecordValue(record, "Discount") or product_params.discount
            self._old_price = MonetizationManager.getRecordValue(record, "OldPrice")
            self.id_title = MonetizationManager.getRecordValue(record, "TitleTextID", default=self.DEFAULT_TEXT_ID)
            self.id_descr = MonetizationManager.getRecordValue(record, "DescrTextID", default=self.DEFAULT_TEXT_ID)
            self.id_new_price = MonetizationManager.getRecordValue(record, "NewPriceTextID", default=self.DEFAULT_TEXT_ID)
            self.id_old_price = MonetizationManager.getRecordValue(record, "OldPriceTextID", default=self.DEFAULT_TEXT_ID)
            self.use_reward_plate = MonetizationManager.getRecordValue(record, "UseRewardPlate", cast=bool, default=False)
            self.id_reward_gold = MonetizationManager.getRecordValue(record, "RewardGoldTextID", default=self.DEFAULT_TEXT_ID)
            self.id_reward_energy = MonetizationManager.getRecordValue(record, "RewardEnergyTextID", default=self.DEFAULT_TEXT_ID)

        @property
        def price(self):
            return MonetizationManager.getProductPrice(self.id)

        @property
        def old_price(self):
            if self._old_price:
                return self._old_price
            price = self.price
            old_price = (price / self.discount) if None not in [price, self.discount] else None
            return old_price

    class StoreImageParam(__Param):
        def __init__(self, record):
            default_proto = MonetizationManager.s_params.get("DefaultStoreImageProto")  # "Movie2_StoreImage
            default_layer = MonetizationManager.s_params.get("DefaultStoreImageLayer")  # "coins3"
            self.id = MonetizationManager.getRecordValue(record, "StoreItemID", cast=str)
            self.prototype = MonetizationManager.getRecordValue(record, "PrototypeName", default=default_proto)
            if self.prototype == default_proto:
                self.layer_name = MonetizationManager.getRecordValue(record, "LayerName", default=default_layer)
            else:
                self.layer_name = None

    class StoreItemParam(__Param):
        def __init__(self, record):
            default_descr = MonetizationManager.s_params.get("DefaultDescriptionTextID", "ID_EMPTY")
            default_proto = MonetizationManager.s_params.get("DefaultStoreCardProto")
            self.id = MonetizationManager.getRecordValue(record, "StoreItemID", cast=str)
            self.descr = MonetizationManager.getRecordValue(record, "DescriptionTextID", default=default_descr)
            prod_id = MonetizationManager.getRecordValue(record, "ProductID", cast=str)
            if MonetizationManager.hasProductInfo(prod_id):
                self.prod_id = MonetizationManager.getProductInfo(prod_id).id  # <- set actual prod_id
            else:
                self.prod_id = None
            self.prototype = MonetizationManager.getRecordValue(record, "PrototypeName", default=default_proto)

    class ProductInfoParam(__Param):
        def __init__(self, record):
            self.alias_id = MonetizationManager.getRecordValue(record, "ProductAliasID", cast=str)
            self.id = MonetizationManager.getRecordValue(record, "ProductID", cast=str)
            self.name = MonetizationManager.getRecordValue(record, "ProductName")
            self.descr = MonetizationManager.getRecordValue(record, "ProductDescr")

            # new version - dict (i.e. {'Gold': 50}) - use getProductReward
            self.reward = MonetizationManager._getRecordDict(record, "Reward", default={"Gold": 0})
            self.only_one_purchase = MonetizationManager.getRecordValue(record, "OnePurchase", default=False, cast=bool)

            self.price = MonetizationManager.getRecordValue(record, "AbstractPrice", default=0)
            self.discount = MonetizationManager.getRecordValue(record, "Discount")

            self.group_id = MonetizationManager.getRecordValue(record, "GroupID")
            self.subgroup_id = MonetizationManager.getRecordValue(record, "SubGroupID")

        @property
        def discount_price(self):
            if self.discount is None:
                return self.price
            discount_price = round(self.price / (1 - self.discount), 1)
            if discount_price - int(discount_price) == 0:
                return int(discount_price)
            return discount_price

    @staticmethod
    def _getRecordDict(record, key, default=None, delimiter=", "):
        """ takes value like 'key1=value1, key2=value' and returns dict {key1:value1, key2:value2}
            :default: default value if record hasn't this key, value must be dict for good work
            :delimiter: str that manage delimiter for multiple values, default is ', ' """

        value = record.get(key)
        if value is None:
            return default

        if "=" not in value:
            if _DEVELOPMENT is True:
                Trace.msg_err("MonetizationManager _getRecordDict [{}] val={!r} doesn't match pattern 'key=value'".format(key, value))
            return {}

        def _cast(val):
            if "." in val and val.count(".") == 1 and val.replace(".", "").isdigit():
                return float(val)
            if val.isdigit():
                return int(val)
            return val

        dict_out = value.split(delimiter)  # use delimiter for multiple values
        dict_out = [tuple(d.split("=")) for d in dict_out]
        dict_out = {key: _cast(val) for key, val in dict_out}

        return dict_out

    @staticmethod
    def getRecordValue(record, key, cast=None, default=None):
        """ :default: default value if given value is 'default'"""
        value = Manager.getRecordValue(record, key, cast=cast, default=default)

        if value == "default":
            value = default

        return value

    @staticmethod
    def loadWithClassParams(records, _class, _dict_save, _alias_dict_save=None):
        for record in records:
            params = _class(record)

            _dict_save[params.id] = params

            if _alias_dict_save is not None and "alias_id" in params.__dict__:
                alias_id = params.__dict__.get("alias_id")
                if alias_id is None:
                    continue
                _alias_dict_save[alias_id] = params

        # print "LOADED {} records FOR {}:".format(len(_dict_save), _class.__name__)  # print "   > ", _dict_save.keys()  # if _alias_dict_save: print "   > ", _alias_dict_save.keys()

    @staticmethod
    def loadGeneralParams(records):
        business_model = getCurrentBusinessModel()
        for record in records:
            key = record.get("Key")
            value = record.get(business_model)

            if isinstance(value, str):
                if value.startswith("[") and value.endswith("]"):
                    value = value[1:-1].split(", ")

            MonetizationManager.s_params[key] = value

        # check params
        allowed_providers = ["Store", "GameStore"]
        store_provider = MonetizationManager.getGeneralSetting("GameStoreName", "GameStore")
        if store_provider not in allowed_providers:
            Trace.log("Manager", 0, "MonetizationGeneral (General) param 'GameStoreName' - should be one of these: {}".format(allowed_providers))

    @staticmethod
    def loadRedirector(records):
        TYPES_BLACKLIST = ["redirect"]
        HUMAN_TABLE_NAMES = {value: key for key, value in MonetizationManager.__PARAMS_TABLE_NAMES.items() if key not in TYPES_BLACKLIST}

        current_publisher = getCurrentPublisher()
        if current_publisher is None:
            return

        for record in records:
            Publisher = record.get("Publisher")
            if Publisher != str(current_publisher):
                # print "!! PUBLISHER={!r} != config={!r}".format(Publisher, current_publisher)
                continue

            Type = HUMAN_TABLE_NAMES.get(record.get("Type"))
            if Type is None:
                redirect_table_name = MonetizationManager.__PARAMS_TABLE_NAMES["redirect"]
                Trace.log("Manager", 0, "{} has error in Type {!r} - choose one of them: {!r}".format(redirect_table_name, record.get("Type"), HUMAN_TABLE_NAMES))
                continue

            platforms = getCurrentPlatformParams()

            for platform, b_active in platforms.items():
                if b_active is False:
                    continue
                table_name = record.get(platform)
                if table_name is None:
                    # only one platform could be True, so we don't need to continue our loop
                    break
                table_name = table_name.format(tag=MonetizationManager.__PARAMS_TABLE_NAMES[Type], platform=Publisher, publisher=Publisher)
                MonetizationManager.__PARAMS_TABLE_NAMES[Type] = table_name

    @staticmethod
    def reportStatus():
        SIZE = 50
        HALF_SIZE = SIZE // 2

        Trace.msg("-" * SIZE)
        Trace.msg("MONETIZATION PARAMS".center(SIZE, " "))
        Trace.msg("-" * SIZE)

        cur_business_model = getCurrentBusinessModel()
        Trace.msg("Business model:  ".rjust(HALF_SIZE) + cur_business_model.ljust(HALF_SIZE))

        cur_publisher = str(getCurrentPublisher())
        Trace.msg("Publisher:  ".rjust(HALF_SIZE) + cur_publisher.ljust(HALF_SIZE))

        current_store_provider = MonetizationManager.getGeneralSetting("GameStoreName", "GameStore")
        Trace.msg("Store provider:  ".rjust(HALF_SIZE) + current_store_provider.ljust(HALF_SIZE))

        Trace.msg("--- Platform ---".center(SIZE, " "))
        platform_params = getCurrentPlatformParams()
        for platform, status in platform_params.items():
            Trace.msg("{}:  ".format(platform).rjust(HALF_SIZE) + str(status).ljust(HALF_SIZE))

        Trace.msg("--- Used tables ---".center(SIZE, " "))
        for key, table_name in MonetizationManager.__PARAMS_TABLE_NAMES.items():
            Trace.msg("{}:  ".format(key).rjust(HALF_SIZE) + table_name.ljust(HALF_SIZE))

        Trace.msg("-" * SIZE)

    @staticmethod
    def loadParams(module, name):
        records = DatabaseManager.getDatabaseRecords(module, name)

        store_provider = MonetizationManager.getGeneralSetting("GameStoreName", "GameStore")

        if name == MonetizationManager.__PARAMS_TABLE_NAMES["redirect"]:  # Always should be first !!!
            MonetizationManager.loadRedirector(records)
        elif name == MonetizationManager.__PARAMS_TABLE_NAMES["general"]:
            MonetizationManager.loadGeneralParams(records)
            MonetizationManager.reportStatus()
        elif name == MonetizationManager.__PARAMS_TABLE_NAMES["store_items"]:
            if store_provider == "Store":
                return True  # this store use own manager for store_items (see StoreButtons)
            MonetizationManager.loadWithClassParams(records, MonetizationManager.StoreItemParam, MonetizationManager.s_cards)
        elif name == MonetizationManager.__PARAMS_TABLE_NAMES["store_images"]:
            if store_provider == "Store":
                return True  # this store use own manager for manage icons (see StoreButtons)
            MonetizationManager.loadWithClassParams(records, MonetizationManager.StoreImageParam, MonetizationManager.s_images)
        elif name == MonetizationManager.__PARAMS_TABLE_NAMES["products_info"]:
            MonetizationManager.loadWithClassParams(records, MonetizationManager.ProductInfoParam, MonetizationManager.s_products, MonetizationManager.s_alias_products)
        elif name == MonetizationManager.__PARAMS_TABLE_NAMES["special_promotions"]:
            MonetizationManager.loadWithClassParams(records, MonetizationManager.SpecialPromoParam, MonetizationManager.s_specials)

        return True

    @classmethod
    def _onInitialize(cls, *args):
        # --- How to update products?
        cls.addObserver(Notificator.onProductsUpdate, MonetizationManager._cbProductsUpdate)
        # Optional step 1: call policy 'CurrentProductsCall' and do something with current products
        #   i.e. setSkuList and respond product's details from Google services by cur product's ids
        # Step 2: send push to `onProductsUpdate` with new params dict (see details in `_cbProductsUpdate` observer)
        # Step 3: `_cbProductsUpdate` called and changes ProductsParams
        # Step 4: on done sends push on `onProductsUpdateDone`

        cls.addObserver(Notificator.onGetRemoteConfig, MonetizationManager._cbGetRemoteConfig)

    @classmethod
    def _onFinalize(cls):
        cls.s_components = {}

        cls.s_params = {}
        cls.s_cards = {}
        cls.s_images = {}
        cls.s_specials = {}
        cls.s_products = {}
        cls.s_alias_products = {}

    @staticmethod
    def _cbProductsUpdate(upd_params_dict, currency=None):
        """     updates s_products params.
            @param upd_params_dict: dict with next template: {prod_id: {param: new_value}, ...};
            @param currency: ISO 4217 currency code;

            You can change only this values: price, name, descr
        """
        if isinstance(upd_params_dict, dict) is False:
            Trace.log("Manager", 0, "_cbProductsUpdate works only with dicts")
            return False

        whitelist_params = ["price", "name", "descr"]

        MonetizationManager.setCurrentCurrencyCode(currency)

        for prod_id, new_params_dict in upd_params_dict.items():
            if MonetizationManager.hasProductInfo(prod_id) is False:
                continue

            product = MonetizationManager.getProductInfo(prod_id)
            for key, value in new_params_dict.items():
                if key not in whitelist_params:
                    continue
                product.__dict__[key] = value

        Notification.notify(Notificator.onProductsUpdateDone)

        return False

    @staticmethod
    def _cbGetRemoteConfig(prod_id, json_string):
        """ Observer that updates product details:
            - discount
            - id
            - reward
        """
        if prod_id not in MonetizationManager.s_products:
            return False

        whitelist = {"discount": (int, float), "id": str, "reward": dict, }

        try:
            patch = json.loads(json_string)

            for key, value in patch.items():
                if key not in whitelist:
                    continue

                if key == "reward":
                    # fix for reward dict-like
                    value = MonetizationManager._getRecordDict(patch, "reward")

                allowed_types = whitelist[key]
                if isinstance(value, allowed_types) is False:  # noqa
                    Trace.msg_err("MonetizationManager can't patch {!r}: {} has wrong type '{}', must be {}".format(prod_id, key, type(value), allowed_types))
                    continue

                product = MonetizationManager.getProductInfo(prod_id)
                product.__dict__[key] = value

        except ValueError as e:
            if _DEVELOPMENT is True:
                Trace.log("Manager", 0, "Can't load product {!r} details: {}".format(prod_id, e))

        return False

    # -----------------

    @staticmethod
    def importComponents(module, names):
        from Foundation.Utils import importType

        for name in names:
            component = importType(module, name)
            MonetizationManager.s_components[name] = component

    @staticmethod
    def getComponentType(name):
        return MonetizationManager.s_components.get(name)

    @staticmethod
    def getComponentsType():
        return MonetizationManager.s_components

    # -----------------

    @staticmethod
    def isMonetizationEnable():
        if Menge.getConfigBool("Monetization", "Enable", False) is False:
            return False

        if Menge.getConfigBool("Monetization", "OnlyMobile", True) is True:
            if Menge.hasTouchpad() is False:
                return False

        if Menge.getConfigBool("Monetization", "OnlyCE", True) is True:
            if isCollectorEdition() is False:
                return False

        return True

    @staticmethod
    def getGeneralSettings():
        return MonetizationManager.s_params

    @staticmethod
    def getCardParams():
        return MonetizationManager.s_cards

    @staticmethod
    def getImageParams():
        return MonetizationManager.s_images

    @staticmethod
    def getProductsInfo():
        return MonetizationManager.s_products

    @staticmethod
    def getSpecialPromotionParams():
        return MonetizationManager.s_specials

    # specific

    @staticmethod
    def getGeneralSetting(key, default=None):
        return MonetizationManager.s_params.get(key) or default

    @staticmethod
    def getCardParamsById(card_id, default=None):
        return MonetizationManager.s_cards.get(card_id) or default

    @staticmethod
    def getImageParamsById(card_id, default=None):
        return MonetizationManager.s_images.get(card_id) or default

    @staticmethod
    def hasProductInfo(prod_id):
        if prod_id in MonetizationManager.s_alias_products:
            return True
        if prod_id in MonetizationManager.s_products:
            return True
        return False

    @staticmethod
    def getProductInfo(prod_id):
        """ alias_prod_id in priority """
        if prod_id in MonetizationManager.s_alias_products:
            return MonetizationManager.s_alias_products.get(prod_id)
        if prod_id in MonetizationManager.s_products:
            return MonetizationManager.s_products.get(prod_id)

        if _DEVELOPMENT is True:
            Trace.log("Manager", 0, "MonetizationManager::getProductInfo - wrong prod_id {} {}: {} & aliases: {}".format(prod_id, type(prod_id), MonetizationManager.s_products.keys(), MonetizationManager.s_alias_products.keys()))
        return None

    @staticmethod
    def getCardProductInfo(card_id):
        card = MonetizationManager.getCardParamsById(card_id)
        if card is None:
            Trace.log("Manager", 0, "MonetizationManager::getCardProductInfo - wrong card_id {}, possible: {}".format(card, MonetizationManager.s_cards.keys()))
            return None
        return MonetizationManager.getProductInfo(card.prod_id)

    @staticmethod
    def getProductPrice(prod_id):
        prod_params = MonetizationManager.getProductInfo(prod_id)
        if prod_params is None:
            Trace.msg_err("MonetizationManager doesn't found price for prod_id {}".format(prod_id))
            return None
        price = prod_params.price
        return price

    @staticmethod
    def getProductReward(prod_id, specific=None):
        """ Returns all reward for given product, also you can get specific reward if you specify param `specific` """
        prod_params = MonetizationManager.getProductInfo(prod_id)
        if prod_params is None:
            Trace.msg_err("MonetizationManager doesn't found reward for prod_id {}".format(prod_id))
            return None
        reward = prod_params.reward
        if specific is not None:
            return reward.get(specific)
        return reward

    @staticmethod
    def getGeneralProductInfo(key, default=None):
        """ util for products that has id in general settings but its alias """
        prod_id = MonetizationManager.getGeneralSetting(key, default)
        product = MonetizationManager.getProductInfo(str(prod_id))
        return product

    @staticmethod
    def getSpecialPromoById(prod_id, default=None):
        params = MonetizationManager.s_specials.get(prod_id)
        return params or default