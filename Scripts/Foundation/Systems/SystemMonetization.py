from Foundation.DemonManager import DemonManager
from Foundation.GroupManager import GroupManager
from Foundation.MonetizationManager import MonetizationManager
from Foundation.PolicyManager import PolicyManager
from Foundation.SecureStringValue import SecureStringValue
from Foundation.SecureValue import SecureValue
from Foundation.System import System
from Foundation.SystemManager import SystemManager
from Foundation.Systems.SystemAnalytics import SystemAnalytics
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger, getCurrentPublisher
from Notification import Notification

_Log = SimpleLogger("SystemMonetization")

class SystemMonetization(System):
    storage = {}
    components = {}
    _session_purchased_products = []

    game_store_name = None

    @staticmethod
    def __isActive(send_debug_log=False):
        if MonetizationManager.isMonetizationEnable() is False:
            if _DEVELOPMENT is False:
                return False

            # send possible reasons for developers
            if send_debug_log is True and Menge.getConfigBool("Monetization", "Enable", False) is True:
                _Log("Monetization is enabled in Config, but it doesn't work. Possible reasons:"
                     "\n - you tries to enable it on PC, but `OnlyMobile` is True (set it to False)"
                     "\n - game is not CE, but `OnlyCE` is True (set it to False)", err=True)

            return False
        return True

    def _onInitialize(self):
        if self.__isActive() is False:
            return

        SystemMonetization.game_store_name = MonetizationManager.getGeneralSetting("GameStoreName", "GameStore")

        from Foundation.AccountManager import AccountManager
        AccountManager.addCreateAccountExtra(SystemMonetization.addExtraAccountSettings)

    def _onRun(self):
        if self.__isActive(send_debug_log=True) is False:
            return True

        self._setupParams()
        self._setupObservers()
        self._setupPolicies()
        self._addAnalytics()

        self.__addDevToDebug()

        return True

    def _onStop(self):
        if Menge.hasTouchpad() is False:
            return True

        for component in SystemMonetization.components.values():
            component.stop()
        SystemMonetization.components = {}

        # self.__remDevToDebug()

        return True

    # --- Policy -------------------------------------------------------------------------------------------------------

    @staticmethod
    def _setupPolicies():
        """ Setups policies for other modules """

        message_provider = MonetizationManager.getGeneralSetting("NotEnoughMessageProvider", "DialogWindow")
        if message_provider == "DialogWindow":
            if DemonManager.hasDemon("DialogWindow") is False:
                Trace.log("System", 0, "SystemMonetization NotEnoughGold policy can't be with DialogWindow - it's not active")
            else:
                PolicyManager.setPolicy("NotEnoughGoldMessage", "PolicyNotEnoughGoldDialog")
                PolicyManager.setPolicy("NotEnoughEnergyMessage", "PolicyNotEnoughEnergyDialog")
        elif message_provider == "MessageOK" or message_provider is None:
            PolicyManager.setPolicy("NotEnoughGoldMessage", "PolicyNotEnoughGoldMessage")
            PolicyManager.setPolicy("NotEnoughEnergyMessage", "PolicyNotEnoughEnergyMessage")
        else:
            Trace.log("System", 0, "SystemMonetization policies: param 'NotEnoughMessageProvider' should be DialogWindow or MessageOK ")

    # --- Payment ------------------------------------------------------------------------------------------------------

    @classmethod
    def pay(cls, prod_id):
        prod_params = MonetizationManager.getProductInfo(prod_id)

        PolicyPurchase = PolicyManager.getPolicy("Purchase", "PolicyPurchaseDummy")
        TaskManager.runAlias(PolicyPurchase, None, Product=prod_params)

    @classmethod
    def scopePay(cls, source, prod_id, scopeSuccess=None, scopeFail=None, scopeTimeout=None):
        TIMEOUT = 30 * 1000  # ms

        def __filter(_id):
            return str(_id) == str(prod_id)

        with source.addParallelTask(2) as (respond, pay):
            with respond.addRaceTask(3) as (timeout, success, fail):
                timeout.addDelay(TIMEOUT)
                timeout.addFunction(_Log, "[pay] timeout {}ms: {}".format(TIMEOUT, prod_id))
                if callable(scopeTimeout) is True:
                    timeout.addScope(scopeTimeout)

                success.addListener(Notificator.onPaySuccess, Filter=__filter)
                if callable(scopeSuccess) is True:
                    success.addScope(scopeSuccess)

                fail.addListener(Notificator.onPayFailed, Filter=__filter)
                if callable(scopeFail) is True:
                    fail.addScope(scopeFail)

            pay.addFunction(cls.pay, prod_id=prod_id)

    # observers

    @staticmethod
    def _onPaySuccess(prod_id):
        product = MonetizationManager.getProductInfo(prod_id)

        if product is None:
            _Log("Unknown product id {!r} ({})".format(prod_id, type(prod_id)), err=True, force=True)
            return False

        SystemMonetization.sendReward(prod_id=prod_id)

        if product.group_id is not None:
            if SystemMonetization.isProductGroupPurchased(product.group_id) is False:
                SystemMonetization.addStorageListValue("PurchasedProductGroups", product.group_id)

                if product.group_id in MonetizationManager.getGeneralSetting("DoubledGroupOnFirstPurchase", []):
                    SystemMonetization.sendReward(prod_id=prod_id)

        if product.only_one_purchase is False:
            return False

        SystemMonetization._session_purchased_products.append(prod_id)
        SystemMonetization.addStorageListValue("purchased", prod_id)

        return False

    @staticmethod
    def _onPayFailed(prod_id):
        _Log("Failed purchase {!r}".format(prod_id), err=True, force=True)
        return False

    # --- Gold ---------------------------------------------------------------------------------------------------------

    @classmethod
    def payGold(cls, gold=None, descr=None):
        """ Main method for pay gold, where 'gold' may be None, but you need
            setup special 'descr' (i.e. 'Hint', 'SkipPuzzle'... check more in class attr 'components') """
        component = cls.components[descr] if descr in cls.components else None

        if component is not None:
            gold = component.getProductPrice()

        if isinstance(gold, (int, float)) is False:
            Trace.log("System", 0, "SystemMonetization.payGold: can't pay gold if it's None or NaN (gold={!r}, descr={!r})".format(gold, descr))
            Notification.notify(Notificator.onGameStorePayGoldFailed, descr)
            return False

        if gold > 0:
            balance = cls.getBalance()
            if balance < gold:
                _Log("Not enough money: you have {} only, but you need {} (descr: {!r})".format(balance, gold, descr), err=True)
                Notification.notify(Notificator.onGameStoreNotEnoughGold, gold - balance, descr)
                return False

            cls.withdrawGold(gold)
        else:
            _Log("gold wasn't withdrawn - current price for {} is 0".format(descr))

        Notification.notify(Notificator.onGameStorePayGoldSuccess, gold, descr)
        return True

    @classmethod
    def scopePayGold(cls, source, gold=None, descr=None, scopeSuccess=None, scopeFail=None, **kwargs):
        """ Scope method with all payment logic. Params 'gold' and 'descr' used in SystemMonetization.payGold.
            - scopeSuccess: scope method will be called if gold is paid successfully;
            - scopeFail: scope method will be called if gold payment failed;
            Use this kwargs:
            - ShouldAcceptPrice: if user decline - payment will be failed """
        if cls.isGameStoreEnable() is False:
            source.addScope(scopeSuccess)
            return

        should_accept_price = kwargs.get("ShouldAcceptPrice", False) or cls.shouldAcceptPrice()

        def _isPriceAccepted():
            if should_accept_price is False:
                return True
            return cls.isPriceAccepted(descr) is True

        if should_accept_price is True:
            arg = cls.components[descr].getProductPrice() if descr in cls.components else " "
            source.addScope(cls._scopePGAcceptPrice, arg, descr=descr)

        with source.addIfTask(_isPriceAccepted) as (true, false):
            # ignores storage['acceptPrice'] if ShouldAcceptPrice is False, check _isPriceAccepted method
            with true.addParallelTask(2) as (response, pay):
                response.addScope(cls._scopePGResponse, scopeSuccess, scopeFail)
                pay.addFunction(cls.payGold, gold=gold, descr=descr)
            false.addDummy()

    @classmethod
    def _scopePGAcceptPrice(cls, source, gold, descr):
        """ Used for scopePayGold - shows DialogWindow 'AcceptPrice', if cancel - no payment """
        if DemonManager.hasDemon("DialogWindow") is False:
            _Log("_scopePGAcceptPrice demon DialogWindow not found", err=True, force=True)
            return

        GameStore = DemonManager.getDemon(SystemMonetization.game_store_name)
        DialogWindow = DemonManager.getDemon("DialogWindow")

        icon = GameStore.generateObjectUnique("Movie2_Coin", "Movie2_Coin_{}".format(getCurrentPublisher()), Enable=True)
        icon.setTextAliasEnvironment("DialogWindowIcon")
        Menge.setTextAlias("DialogWindowIcon", "$AliasCoinUsePrice", "ID_EMPTY")

        text_args = dict(icon_value=[gold])

        if cls.isPriceAccepted(descr) is True:
            return

        source.addFunction(DialogWindow.runPreset, "AcceptPrice", content_style="icon", icon_obj=icon, text_args=text_args)

        with source.addRaceTask(2) as (confirm, cancel):
            confirm.addListener(Notificator.onDialogWindowConfirm)
            confirm.addFunction(cls.acceptPrice, descr)
            cancel.addListener(Notificator.onDialogWindowCancel)

        with source.addRaceTask(2) as (close, leave):
            close.addEvent(DialogWindow.EVENT_WINDOW_DISAPPEAR)
            leave.addListener(Notificator.onSceneDeactivate)

        source.addTask("TaskObjectDestroy", Object=icon)

    @staticmethod
    def _scopePGResponse(source, scopeSuccess=None, scopeFail=None):
        """ Used for scopePayGold - responses on payGold """
        with source.addRaceTask(3) as (success, fail, no_money):
            success.addListener(Notificator.onGameStorePayGoldSuccess)
            if callable(scopeSuccess):
                success.addScope(scopeSuccess)

            fail.addListener(Notificator.onGameStorePayGoldFailed)
            if callable(scopeFail):
                fail.addScope(scopeFail)

            no_money.addListener(Notificator.onGameStoreNotEnoughGold)
            with no_money.addRaceTask(2) as (confirm, cancel):
                confirm.addListener(Notificator.onDialogWindowConfirm)
                cancel.addListener(Notificator.onDialogWindowCancel)

    @classmethod
    def withdrawGold(cls, num, immediately_save=True):
        _Log("withdrawGold num={}".format(num))
        cls.storage["gold"].subtractValue(num)
        if immediately_save is True:
            cls.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, cls.getBalance())
        return True

    @classmethod
    def addGold(cls, num, immediately_save=True):
        _Log("addGold num={}".format(num))
        cls.storage["gold"].additiveValue(num)
        if immediately_save is True:
            cls.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, cls.getBalance())
        return True

    @classmethod
    def setGold(cls, num, immediately_save=True):
        _Log("set num={}".format(num))
        cls.storage["gold"].setValue(num)
        if immediately_save is True:
            cls.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, cls.getBalance())
        return True

    @classmethod
    def rollbackGold(cls, prod_id=None, component_tag=None):
        _prod_id = None

        if prod_id is not None:
            _prod_id = prod_id
        elif component_tag in SystemMonetization.components:
            _prod_id = SystemMonetization.components[component_tag].getProductId()

        if _prod_id is None:
            return False

        price = MonetizationManager.getProductPrice(_prod_id)
        return cls.addGold(price)

    @staticmethod
    def getBalance():
        balance = SystemMonetization.getStorageValue("gold")
        _Log("balance={}".format(balance))
        return balance

    @staticmethod
    def isPriceAccepted(descr):
        accepted_price = SystemMonetization.getStorageListValues("acceptPrice")
        b_accept = descr in accepted_price
        return b_accept

    @staticmethod
    def acceptPrice(descr):
        accepted_price = SystemMonetization.getStorageListValues("acceptPrice")
        if descr in accepted_price:
            return

        SystemMonetization.addStorageListValue("acceptPrice", descr)
        return True

    # --- Rewards ------------------------------------------------------------------------------------------------------

    @classmethod
    def sendReward(cls, rew_dict=None, prod_id=None):
        """ sends reward according to custom dict or product reward info. Select one: `rew_dict` or `prod_id`.
            @param rew_dict: dict with reward info, allowed keys:
                "Gold" (adds gold), "Chapter" (unlocks chapter), "SceneUnlock" (unlocks scene),
                "Energy" (adds energy), "DisableInterstitialAds" (disable interstitial adverts)
            @param prod_id: id of product, which has reward info """

        reward = {}
        if prod_id is not None:
            reward = MonetizationManager.getProductReward(prod_id)
        elif rew_dict is not None:
            reward = rew_dict

        if not (isinstance(reward, dict) and len(reward) > 0):
            if _DEVELOPMENT is True:
                Trace.log("System", 0, "SystemMonetization.sendReward wrong reward dict {!r} (your input: {!r}, id={!r})".format(reward, rew_dict, prod_id))
            return False

        rewards = {"Gold": cls.addGold, "Chapter": cls.unlockChapter, "SceneUnlock": cls.unlockScene, "Energy": cls.addEnergy, "DisableInterstitialAds": cls.disableInterstitialAds}
        for reward_type, arg in reward.items():
            fn = rewards.get(reward_type)
            if callable(fn):
                fn(arg)
            else:
                _Log("Not found reward function for type {!r} (prod_id={})".format(reward_type, prod_id), err=True)

        Notification.notify(Notificator.onGameStoreSentRewards, prod_id, reward)
        return True

    @staticmethod
    def addEnergy(energy):
        Notification.notify(Notificator.onEnergyIncrease, energy)

    @staticmethod
    def unlockChapter(chapter_id):
        Notification.notify(Notificator.onChapterSelectionBlock, chapter_id, False)

        if chapter_id == "Bonus":
            bonus_prod_id = SystemMonetization.components["PaidBonusChapter"].getProductId()

            if SystemMonetization.isProductPurchased(bonus_prod_id) is False:
                SystemMonetization.addStorageListValue("purchased", bonus_prod_id)

        _Log("unlock chapter '{}'".format(chapter_id))

    @staticmethod
    def disableInterstitialAds(*args):
        if SystemManager.hasSystem("SystemAdvertising") is False:
            return
        SystemAdvertising = SystemManager.getSystem("SystemAdvertising")
        SystemAdvertising.disableForever()
        _Log("disabled interstitial ads")

    @staticmethod
    def unlockScene(name):  # todo
        _Log("DUMMY unlock scene '{}'".format(name))

    # --- Advertisements -----------------------------------------------------------------------------------------------

    @classmethod
    def showAd(cls, AdType="Rewarded"):
        if AdType == "Rewarded" and cls.isAdsEnded() is True:
            cls.updateAvailableAds()

            if cls.isAdsEnded() is True:
                _Log("ad limit reached today", err=True)
                Notification.notify(Notificator.onAvailableAdsEnded)
                return

        TaskManager.runAlias("AliasShowAdvert", None, AdType=AdType)

    @staticmethod
    def updateAvailableAds():
        """ resets `todayViewedAds` if `lastViewedAdDate` is different from today date"""
        today_date = SystemMonetization.__getTodayDate()
        if SystemMonetization.storage["lastViewedAdDate"].isEqual(today_date) is True:
            return  # reset `todayViewedAds` only if it's another day
        SystemMonetization.storage["todayViewedAds"].setValue(0)
        SystemMonetization.saveData("todayViewedAds")
        Notification.notify(Notificator.onAvailableAdsNew)

    @staticmethod
    def __getTodayDate():
        """ :return: 'YEAR/MONTH/DAY' """
        time = Menge.getLocalDateStruct()
        today_date = "{}/{}/{}".format(time.year, time.month, time.day)
        return today_date

    @staticmethod
    def isAdsEnded():
        """ :return: True if ads ended """
        today_viewed_ads = SystemMonetization.getStorageValue("todayViewedAds")
        ads_per_day = MonetizationManager.getGeneralSetting("AdsPerDay")
        return today_viewed_ads >= ads_per_day

    # callbacks

    @staticmethod
    def _onAdvertisementResult(label, result):  # react on showAd()
        _Log("onAdvertisementReward - [{}] {}".format(label, result))

        # if we have advert product - reward will be gathered from product info,
        # otherwise only gold from param GoldPerAd
        advert_prod_id = MonetizationManager.getGeneralSetting("AdvertProductID")
        reward = dict(Gold=MonetizationManager.getGeneralSetting("GoldPerAd"))

        last_date = SystemMonetization.getStorageValue("lastViewedAdDate")
        today_date = SystemMonetization.__getTodayDate()
        SystemMonetization.storage["lastViewedAdDate"].setValue(today_date)

        if SystemMonetization.isAdsEnded() is False:
            SystemMonetization.sendReward(rew_dict=reward, prod_id=advert_prod_id)

            if last_date == today_date:
                SystemMonetization.storage["todayViewedAds"].additiveValue(1)
            else:  # imagine if today was 0 viewed ads, and we increase it by 1
                SystemMonetization.storage["todayViewedAds"].setValue(1)

        SystemMonetization.saveData("todayViewedAds", "lastViewedAdDate", "gold")

        if SystemMonetization.isAdsEnded() is True:
            Notification.notify(Notificator.onAvailableAdsEnded)
            _Log("onAvailableAdsEnded")

        return False

    # --- Check components ---------------------------------------------------------------------------------------------

    @staticmethod
    def shouldAcceptPrice():
        return MonetizationManager.getGeneralSetting("ShouldAcceptPrice", True)

    @staticmethod
    def isGameStoreEnable():
        if GroupManager.hasGroup(SystemMonetization.game_store_name) is False:
            return False
        demon = DemonManager.getDemon(SystemMonetization.game_store_name)
        return demon.isStoreEnable()

    @staticmethod
    def isComponentEnable(name):
        if name not in SystemMonetization.components:
            return False

        b_run = SystemMonetization.__isActive()
        b_store = SystemMonetization.isGameStoreEnable() is True
        b_component = SystemMonetization.components[name].isEnable() is True

        return all([b_run, b_store, b_component])

    @staticmethod
    def getComponent(name):
        if SystemMonetization.hasComponent(name):
            return None
        return SystemMonetization.components[name]

    @staticmethod
    def hasComponent(name):
        if name not in SystemMonetization.components:
            return False
        return True

    @staticmethod
    def isProductPurchased(prod_id):
        if _DEVELOPMENT is True:
            if isinstance(prod_id, str) is False:
                Trace.log("System", 0, "Wrong product id type {}, must be str".format(type(prod_id)))
                return False

        items = SystemMonetization.getStorageListValues("purchased")
        if items is None:
            return False

        is_purchased = str(prod_id) in items

        # if _DEVELOPMENT is True:
        #     _Log("-- isProductPurchased {} in {}: {}".format(prod_id, items, is_purchased))

        return is_purchased

    @staticmethod
    def isProductGroupPurchased(group_id):
        items = SystemMonetization.getStorageListValues("PurchasedProductGroups")
        if items is None:
            return False

        is_purchased = str(group_id) in items
        return is_purchased

    # --- Observers ----------------------------------------------------------------------------------------------------

    def _setupObservers(self):
        self.addObserver(Notificator.onSelectAccount, self._onSelectAccount)

        # GameStore
        self.addObserver(Notificator.onGiftExchangeRedeemResult, self._onGiftExchangeRedeemResult)
        self.addObserver(Notificator.onAvailableAdsEnded, self._onAvailableAdsEnded)
        self.addObserver(Notificator.onGameStoreNotEnoughGold, self._onGameStoreNotEnoughGold)
        self.addObserver(Notificator.onEnergyNotEnough, self._onEnergyNotEnough)

        self.addObserver(Notificator.onLayerGroupEnable, self._cbLayerGroupEnable)

        # monetization features
        self.addObserver(Notificator.onAdvertRewarded, self._onAdvertisementResult)
        self.addObserver(Notificator.onAppRated, self._onAppRated)

        # payment
        self.addObserver(Notificator.onPaySuccess, self._onPaySuccess)
        self.addObserver(Notificator.onPayFailed, self._onPayFailed)

    def _cbLayerGroupEnable(self, group_name):
        if group_name in ["BalanceIndicator", SystemMonetization.game_store_name]:
            Notification.notify(Notificator.onUpdateGoldBalance, str(self.getBalance()))
        return False

    def _onSelectAccount(self, account_id):
        self._saveSessionPurchases()

        self.updateAvailableAds()
        return False

    @staticmethod
    def _onGiftExchangeRedeemResult(reward_type, reward_amount):
        """ todo: send reward to user (in progress) """
        _Log("onGiftExchangeRedeemResult DUMMY - {} {}".format(reward_type, reward_amount))
        return False

    @staticmethod
    def _onAvailableAdsEnded(*args, **kwargs):
        _Log("onAvailableAdsEnded - args:{} kwargs:{}".format(args, kwargs))
        return False

    def _onGameStoreNotEnoughGold(self, gold, descr):
        NotEnoughMoneyPageID = MonetizationManager.getGeneralSetting("NotEnoughMoneyPageID")

        TaskManager.runAlias("AliasNotEnoughGold", None, Gold=gold, Descr=descr, PageID=NotEnoughMoneyPageID)
        return False

    def _onEnergyNotEnough(self, action_name):
        NotEnoughMoneyPageID = MonetizationManager.getGeneralSetting("NotEnoughMoneyPageID")

        TaskManager.runAlias("AliasNotEnoughEnergy", None, Action=action_name, PageID=NotEnoughMoneyPageID)
        return False

    @staticmethod
    def _onChangeGold(account_id, value):
        """ `gold` observer in addExtraAccountSettings """
        balance = SystemMonetization.getBalance()
        Notification.notify(Notificator.onUpdateGoldBalance, balance)

    def _onAppRated(self):
        rate_reward = MonetizationManager.getGeneralSetting("RateUsReward")
        if rate_reward is None:
            return True

        self.sendReward(rew_dict={"Gold": int(rate_reward)})
        return True

    # --- Other --------------------------------------------------------------------------------------------------------

    def _addAnalytics(self):
        def _getExtraParams():
            return {"current_gold": self.getBalance()}

        SystemAnalytics.addExtraAnalyticParams(_getExtraParams)

        def _cbSentRewardParams(prod_id, rewards):
            params = {"product_id": prod_id}
            params.update({str(key): value for key, value in rewards.items()})
            return params

        def _cbEarnCurrency(prod_id, rewards):
            currencies = ['Gold', 'Energy']
            for key, amount in rewards.items():
                if key not in currencies:
                    continue
                return {'name': str(key.lower()), 'amount': amount}

        advert_prod_id = MonetizationManager.getGeneralSetting("AdvertProductID")

        SystemAnalytics.addSpecificAnalytic("earn_currency", "purchase", Notificator.onGameStoreSentRewards, lambda _, rewards: 'Gold' in rewards or 'Energy' in rewards, _cbEarnCurrency)
        SystemAnalytics.addSpecificAnalytic("spent_currency", "spent_gold", Notificator.onGameStorePayGoldSuccess, None, lambda gold, descr: {'amount': gold, 'description': descr, 'name': 'gold'})

        SystemAnalytics.addAnalytic("got_promocode_reward", Notificator.onGiftExchangeRedeemResult, None, lambda label, result: {'type': label, 'result': result})
        SystemAnalytics.addAnalytic("got_purchase_reward", Notificator.onGameStoreSentRewards, lambda prod_id, *_: prod_id != advert_prod_id, _cbSentRewardParams)
        SystemAnalytics.addAnalytic("got_ad_reward", Notificator.onGameStoreSentRewards, lambda prod_id, *_: prod_id == advert_prod_id, lambda prod_id, rewards: rewards)
        SystemAnalytics.addAnalytic("not_enough_gold", Notificator.onGameStoreNotEnoughGold, None, lambda value, descr: {"not_enough_value": value, "description": descr})
        SystemAnalytics.addAnalytic("rewarded_ads_reached_limit", Notificator.onAvailableAdsEnded, None, lambda: {"today_viewed_ads": SystemMonetization.getStorageValue("todayViewedAds"), "fingerprint": SystemMonetization.getStorageValue("lastViewedAdDate")})

    @staticmethod
    def __initStorage():
        storage = {"gold": SecureValue("gold", int(MonetizationManager.getGeneralSetting("StartBalance", 0))), "todayViewedAds": SecureValue("todayViewedAds", 0), "lastViewedAdDate": SecureStringValue("lastViewedAdDate", ""), "skippedMGs": SecureStringValue("skippedMGs", ""), "acceptPrice": SecureStringValue("acceptPrice", ""), "purchased": SecureStringValue("purchased", ""),  # "{}, "...
            "PurchasedProductGroups": SecureStringValue("PurchasedProductGroups", "")}
        SystemMonetization.storage = storage

    @staticmethod
    def _setupParams():
        SystemMonetization.__initStorage()

        if _DEVELOPMENT is True:
            default_currency_code = Menge.getConfigString("Monetization", "DebugCurrencyCode", "USD")
            if default_currency_code.lower() != "none":
                MonetizationManager.setCurrentCurrencyCode(default_currency_code)

        for name, new in MonetizationManager.getComponentsType().items():
            component = new()
            if component.initialize() is True:
                component.run()
                SystemMonetization.components[name] = component

    # --- Data Storage -------------------------------------------------------------------------------------------------

    # storage interaction ---

    @staticmethod
    def _saveSessionPurchases():
        """ We need to save again some products, because sometimes user can buy product and leave game
            Then SDK sends cbPaySuccess immediately after init, but user not selected yet
            So this purchase didn't save in user settings.json and may cause bugs
            EXAMPLE: https://drive.google.com/file/d/11thAK73I-gNxxwPmLhFquTOxY2CTU1xz/view """

        if len(SystemMonetization._session_purchased_products) == 0:
            return

        session_products = set(SystemMonetization._session_purchased_products)
        saved_products = set(SystemMonetization.getStorageListValues("purchased"))

        not_saved_products = session_products - saved_products
        _Log("_saveSessionPurchases found {} save candidates : {}".format(len(not_saved_products), not_saved_products))

        for prod_id in not_saved_products:
            SystemMonetization.addStorageListValue("purchased", prod_id)

    @staticmethod
    def addStorageListValue(key, value):
        raw_items = SystemMonetization.getStorageValue(key)
        if raw_items is None:
            return

        items = raw_items.strip(", ").split(", ")

        if str(value) in items:
            _Log("value {!r} is already in '{}': {}".format(value, key, items), err=True)
            return

        raw_items += "{}, ".format(str(value))
        SystemMonetization.storage[key].setValue(raw_items)

        SystemMonetization.saveData(key)

        _Log("successfully append {!r} to '{}' list: {}".format(value, key, raw_items))

    @staticmethod
    def getStorageListValues(key):
        raw_items = SystemMonetization.getStorageValue(key)
        if raw_items is None:
            return None
        items = raw_items.strip(", ").split(", ")
        return items

    @staticmethod
    def getStorageValue(key):
        if key not in SystemMonetization.storage:
            Trace.log("System", 0, "SystemMonetization getStorageValue {!r} not found".format(key))
            return

        value = SystemMonetization.storage[key].getValue()
        return value

    # --- storage interaction

    @staticmethod
    def saveData(*keys):
        """ Apply Menge.saveAccounts
            :param keys: str keys, they must be in storage.
                if 0 keys: saves all values from storage
        """

        if len(keys) == 0:
            _Log("Saver: save all data on device...")
            for key, value in SystemMonetization.storage.items():
                save = value.getSave()
                Menge.changeCurrentAccountSetting(key, unicode(save))

        else:
            for key in keys:
                if key not in SystemMonetization.storage:
                    _Log("Saver: storage key {!r} not found".format(key), err=True)
                    continue
                _Log("Saver: save {!r} on device...".format(key))
                save = SystemMonetization.storage[key].getSave()
                Menge.changeCurrentAccountSetting(key, unicode(save))

        Menge.saveAccounts()
        _Log("Saver: save complete...")

    @staticmethod
    def addExtraAccountSettings(account_id, isGlobal):
        if isGlobal is True:
            return

        observers = {# add here key from storage and function that will be called if setting would be changed
            "gold": SystemMonetization._onChangeGold}

        for key in SystemMonetization.storage.keys():
            fn = observers.get(key)
            Menge.addCurrentAccountSetting(key, u'None', fn)

        # calls only on Create Account

        _Log("added storage settings to account {} params".format(account_id))

    @staticmethod
    def loadData():
        if SystemMonetization.__isActive() is False:
            return
        _Log("restore storage from USER saves...")

        for key in SystemMonetization.storage.keys():
            value_save = str(Menge.getCurrentAccountSetting(key))
            if value_save == "None":
                SystemMonetization.saveData(key)
            else:
                SystemMonetization.storage[key].loadSave(value_save)

            _Log("--- key={!r} save={!r} value={!r}".format(key, value_save, SystemMonetization.getStorageValue(key)))

    def _onSave(self):
        if SystemMonetization.__isActive() is False:
            return {}

        # saves all data from storage
        self.saveData()

        return {}

    def _onLoad(self, save):
        if SystemMonetization.__isActive() is False:
            return

        # load saves from account params
        self.loadData()

        return

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return
        if self.__isActive() is False:
            return
        if Menge.hasDevToDebugTab("Monetization") is True:
            return

        tab = Menge.addDevToDebugTab("Monetization")

        # buttons

        w_show_ad = Menge.createDevToDebugWidgetButton("show_ad")
        w_show_ad.setTitle("Show ad with current provider")
        w_show_ad.setClickEvent(self.showAd)
        tab.addWidget(w_show_ad)

        w_upd_ads = Menge.createDevToDebugWidgetButton("update_ads")
        w_upd_ads.setTitle("Update available ads")
        w_upd_ads.setClickEvent(self.updateAvailableAds)
        tab.addWidget(w_upd_ads)

        # command lines

        def _addGold(text):
            gold = int(text)
            self.addGold(gold)

        w_add = Menge.createDevToDebugWidgetCommandLine("add_gold")
        w_add.setTitle("Add gold")
        w_add.setPlaceholder("Input here positive integer")
        w_add.setCommandEvent(_addGold)
        tab.addWidget(w_add)

        def _withdrawGold(text):
            gold = int(text)
            self.withdrawGold(gold)

        w_withdraw = Menge.createDevToDebugWidgetCommandLine("withdraw_gold")
        w_withdraw.setTitle("Withdraw gold")
        w_withdraw.setPlaceholder("Input here positive integer")
        w_withdraw.setCommandEvent(_withdrawGold)
        tab.addWidget(w_withdraw)

        def _setGold(text):
            gold = int(text)
            self.setGold(gold)

        w_set = Menge.createDevToDebugWidgetCommandLine("set_gold")
        w_set.setTitle("Set gold")
        w_set.setPlaceholder("Input here positive integer")
        w_set.setCommandEvent(_setGold)
        tab.addWidget(w_set)

        def _sendReward(product_id):
            self.sendReward(prod_id=product_id)

        w_send_reward = Menge.createDevToDebugWidgetCommandLine("send_reward")
        w_send_reward.setTitle("Send reward from product")
        w_send_reward.setPlaceholder("Syntax: <product_id>")
        w_send_reward.setCommandEvent(_sendReward)
        tab.addWidget(w_send_reward)

        def _payGold(text):
            params = [int(param) if param.isdigit() else param for param in text.split()]
            if len(params) < 1 or len(params) > 2:
                _Log("[DevToDebug] wrong params: syntax <gold_num> [descr]", err=True)
                return
            gold = params[0]
            descr = None if len(params) < 2 else params[1]
            self.payGold(gold, descr)

        w_pay_gold = Menge.createDevToDebugWidgetCommandLine("pay_gold")
        w_pay_gold.setTitle("Pay gold")
        w_pay_gold.setPlaceholder("Syntax: <gold_num> [descr]")
        w_pay_gold.setCommandEvent(_payGold)
        tab.addWidget(w_pay_gold)

        w_pay = Menge.createDevToDebugWidgetCommandLine("pay")
        w_pay.setTitle("Payment with `{}`".format(PolicyManager.getPolicy("Purchase", "PolicyPurchaseDummy")))
        w_pay.setPlaceholder("Syntax: <product_id>")
        w_pay.setCommandEvent(self.pay)
        tab.addWidget(w_pay)

        def _showSpecialPromo(special_prod_id):
            if DemonManager.hasDemon("SpecialPromotion") is False:
                _Log("[DevToDebug] SpecialPromotion demon not found", err=True)
                return
            SpecialPromotion = DemonManager.getDemon("SpecialPromotion")
            _Log("[DevToDebug] run SpecialPromotion {}".format(special_prod_id))
            SpecialPromotion.run(special_prod_id)

        w_special_promo = Menge.createDevToDebugWidgetCommandLine("special_promo")
        w_special_promo.setTitle("Show special promotion")
        w_special_promo.setPlaceholder("Syntax: <product_id>")
        w_special_promo.setCommandEvent(_showSpecialPromo)
        tab.addWidget(w_special_promo)

        # info texts

        def _getSettingsWidgetTitle():
            title = "**Monetization settings**"
            title += "".join(["\n* {}: `{}`".format(key, val) for key, val in MonetizationManager.getGeneralSettings().items()])
            return title

        w_settings_descr = Menge.createDevToDebugWidgetText("monetization_settings_descr")
        w_settings_descr.setText(_getSettingsWidgetTitle)
        tab.addWidget(w_settings_descr)

        def _updateSetting(text):
            params = text.split(" ")
            if len(params) != 2:
                return

            all_settings = MonetizationManager.getGeneralSettings()
            setting = params[0]
            if setting not in all_settings:
                _Log("[DevToDebug] setting {!r} not found".format(setting), err=True)
                return

            value = int(params[1]) if params[1].isdigit() else params[1]
            _Log("[DevToDebug] changed setting {!r} from {!r} to {!r}".format(setting, all_settings[setting], value))
            all_settings[setting] = value

        w_settings = Menge.createDevToDebugWidgetCommandLine("change_settings")
        w_settings.setTitle("Change settings (from list above)")
        w_settings.setPlaceholder("Syntax: <setting_name> <new_value>")
        w_settings.setCommandEvent(_updateSetting)
        tab.addWidget(w_settings)

    def __remDevToDebug(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return

        if Menge.hasDevToDebugTab("Monetization") is True:
            Menge.removeDevToDebugTab("Monetization")