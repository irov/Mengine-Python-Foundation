from Foundation.DemonManager import DemonManager
from Foundation.GroupManager import GroupManager
from Foundation.MonetizationManager import MonetizationManager
from Foundation.AccountManager import AccountManager
from Foundation.SecureStringValue import SecureStringValue
from Foundation.SecureValue import SecureValue
from Foundation.System import System
from Foundation.SystemManager import SystemManager
from Foundation.Systems.SystemAnalytics import SystemAnalytics
from Foundation.TaskManager import TaskManager
from Foundation.Utils import SimpleLogger, getCurrentPublisher
from Foundation.Providers.PaymentProvider import PaymentProvider
from Notification import Notification

_Log = SimpleLogger("SystemMonetization", option="monetization")

ALIAS_GLOBAL_ADVERT_COUNTER = "$AliasGlobalAdvertCounter"


class SystemMonetization(System):
    storage = {}
    components = {}
    _session_purchased_products = []
    _session_delayed_products = []

    game_store_name = None

    @staticmethod
    def __isActive():
        if MonetizationManager.isMonetizationEnable() is False:
            if _DEVELOPMENT is False:
                return False

            # send possible reasons for developers
            _Log("Monetization is enabled in Config, but it doesn't work. Possible reasons:"
                 "\n - you tries to enable it on PC, but `OnlyMobile` is True (set it to False)"
                 "\n - game is not CE, but `OnlyCE` is True (set it to False)", err=True)

            return False
        return True

    def _onInitialize(self):
        if SystemMonetization.__isActive() is False:
            return

        SystemMonetization.game_store_name = MonetizationManager.getGeneralSetting("GameStoreName", "GameStore")

        AccountManager.addCreateAccountExtra(SystemMonetization.addExtraAccountSettings)

    def _onRun(self):
        if SystemMonetization.__isActive() is False:
            return True

        self._setupParams()
        self.setupObservers()
        self.setupPolicies()
        self._addAnalytics()

        # self.__addDevToDebug()

        return True

    def _onStop(self):
        for component in SystemMonetization.components.values():
            component.stop()
        SystemMonetization.components = {}

        # self.__remDevToDebug()

        return True

    def setupPolicies(self):
        self._setupPolicies()

    @staticmethod
    def _setupPolicies():
        """ override it for specific behaviour """
        pass

    # --- Payment ------------------------------------------------------------------------------------------------------

    @staticmethod
    def pay(prod_id):
        if SystemMonetization.__isActive() is False:
            return

        real_prod_id = MonetizationManager.getProductRealId(prod_id)

        if SystemMonetization.isPurchaseDelayed(real_prod_id) is True:
            Notification.notify(Notificator.onReleasePurchased, real_prod_id)
            return

        PaymentProvider.pay(real_prod_id)

    @staticmethod
    def scopePay(source, prod_id, scopeSuccess=None, scopeFail=None, scopeTimeout=None):
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

            pay.addFunction(SystemMonetization.pay, prod_id=prod_id)

    # observers

    @staticmethod
    def _onPaySuccess(prod_id):
        product = MonetizationManager.getProductInfo(prod_id)

        if product is None:
            _Log("Unknown product id {!r} ({})".format(prod_id, type(prod_id)), err=True, force=True)
            return False

        SystemMonetization._session_purchased_products.append(prod_id)
        SystemMonetization.sendReward(prod_id=prod_id)

        if product.group_id is not None:
            if SystemMonetization.isProductGroupPurchased(product.group_id) is False:
                SystemMonetization.addStorageListValue("PurchasedProductGroups", product.group_id)

                if product.group_id in MonetizationManager.getGeneralSetting("DoubledGroupOnFirstPurchase", []):
                    SystemMonetization.sendReward(prod_id=prod_id)

        if product.isConsumable() is True:
            return False

        # save non-consumable product
        SystemMonetization.addStorageListValue("purchased", prod_id)

        return False

    @staticmethod
    def _onProductAlreadyOwned(prod_id):
        product = MonetizationManager.getProductInfo(prod_id)
        if product.isConsumable() is True:
            _Log("Product {!r} is consumable and can't be restored".format(prod_id), err=True, force=True)
            return False

        if SystemMonetization.isProductPurchased(prod_id) is True:
            _Log("Product {!r} already owned and applied for game".format(prod_id))
            Notification.notify(Notificator.onPayComplete, prod_id)
            return False

        _Log("Product {!r} already owned, but not applied - fix it".format(prod_id))
        Notification.notify(Notificator.onPaySuccess, prod_id)
        Notification.notify(Notificator.onPayComplete, prod_id)
        return False

    @staticmethod
    def _onDelayPurchased(prod_id):
        """ these products already purchased, but we shouldn't send rewards at this moment """

        if MonetizationManager.hasProductInfo(prod_id) is False:
            _Log("Unknown product id {!r} ({})".format(prod_id, type(prod_id)), err=True, force=True)
            return False

        if SystemMonetization.isPurchaseDelayed(prod_id) is True:
            _Log("Purchase already delayed {!r}".format(prod_id), err=True, optional=True)
            return False

        SystemMonetization._session_delayed_products.append(prod_id)
        _Log("Delay purchase {!r}".format(prod_id), optional=True)

        return False

    @staticmethod
    def _onReleasePurchased(prod_id):
        if SystemMonetization.isPurchaseDelayed(prod_id) is False:
            _Log("Product {!r} not purchased or delayed".format(prod_id), err=True, force=True)
            return False

        SystemMonetization._session_delayed_products.remove(prod_id)
        _Log("Release delayed purchase {!r}...".format(prod_id), optional=True)
        Notification.notify(Notificator.onPaySuccess, prod_id)

        return False

    @staticmethod
    def _onPayFailed(prod_id):
        _Log("Failed purchase launch flow {!r}".format(prod_id), err=True, force=True)
        return False

    # --- Gold ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def _onPayGold(gold=None, descr=None):
        """ Main method for pay gold, where 'gold' may be None, but you need
            setup special 'descr' (i.e. 'Hint', 'SkipPuzzle'... check more in class attr 'components') """
        component = SystemMonetization.components[descr] if descr in SystemMonetization.components else None

        if component is not None:
            gold = component.getProductPrice()

        if isinstance(gold, (int, float)) is False:
            Trace.log("System", 0, "SystemMonetization.payGold: can't pay gold if it's None or NaN (gold={!r}, descr={!r})".format(gold, descr))
            Notification.notify(Notificator.onGameStorePayGoldFailed, descr)
            return False

        if gold > 0:
            balance = SystemMonetization.getBalance()
            if balance < gold:
                _Log("Not enough money: you have {} only, but you need {} (descr: {!r})".format(balance, gold, descr), err=True, optional=True)

                if MonetizationManager.getGeneralSetting("AllowPayGoldAfterPurchase", False) is False:
                    Notification.notify(Notificator.onGameStorePayGoldFailed, descr)

                Notification.notify(Notificator.onGameStoreNotEnoughGold, gold - balance, descr)
                return False

            SystemMonetization.withdrawGold(gold)
        else:
            _Log("gold wasn't withdrawn - current price for {} is 0".format(descr), optional=True)

        Notification.notify(Notificator.onGameStorePayGoldSuccess, gold, descr)

        return False

    @staticmethod
    def scopePayGold(source, gold=None, descr=None, scopeSuccess=None, scopeFail=None, **kwargs):
        """ Payment logic. Params 'gold' and 'descr' are must have.
                - scopeSuccess: scope method will be called if gold is paid successfully;
                - scopeFail: scope method will be called if gold payment failed;
            Use this kwargs:
                - ShouldAcceptPrice: if user decline - payment will be failed;
        """
        if SystemMonetization.isGameStoreEnable() is False:
            Trace.log("System", 0, "Try to pay gold while store is not enable!!!!!!!!!!!!")
            return False

        should_accept_price = kwargs.get("ShouldAcceptPrice", False) or SystemMonetization.shouldAcceptPrice()
        price = SystemMonetization.components[descr].getProductPrice() if descr in SystemMonetization.components else gold

        def _isPriceAccepted():
            if price == 0:
                return True
            if should_accept_price is False:
                return True
            return SystemMonetization.isPriceAccepted(descr) is True

        if price != 0 and should_accept_price is True:
            source.addScope(SystemMonetization.scopeTryAcceptPrice, amount=price, currency="Gold", descr=descr)

        with source.addIfTask(_isPriceAccepted) as (true, false):
            with true.addParallelTask(2) as (response, pay):
                response.addScope(SystemMonetization._scopePGResponse, scopeSuccess, scopeFail)
                pay.addNotify(Notificator.onGameStorePayGold, gold=gold, descr=descr)
            false.addDummy()
        return True

    @staticmethod
    def scopeTryAcceptPrice(source, amount, currency, descr):
        if SystemMonetization.isPriceAccepted(descr) is True:
            return

        if DemonManager.hasDemon("DialogWindow") is False:
            _Log("scopeTryAcceptPrice demon DialogWindow not found", err=True, force=True)
            return

        GameStore = DemonManager.getDemon(SystemMonetization.game_store_name)
        DialogWindow = DemonManager.getDemon("DialogWindow")

        # ----------------------------------------
        # setup icon
        prototype_template = {
            "Gold": "Movie2_Coin_{publisher}",
            "default": "Movie2_{currency}_{publisher}",
        }
        prototype_name = prototype_template.get(currency, prototype_template["default"]).format(
            publisher=getCurrentPublisher(),
            currency=currency
        )
        icon = GameStore.generateIcon("Icon", prototype_name, Enable=True)

        # setup text
        text_args = dict(icon_value=[amount])

        # find and setup preset
        preset_names = [
            "{}AcceptPrice_{}".format(descr, currency),
            "{}AcceptPrice".format(descr),
            "AcceptPrice_{}".format(currency),
            "AcceptPrice"
        ]
        preset_name = next((name for name in preset_names if DialogWindow.hasPreset(name)), None)
        if preset_name is None:
            _Log("Not found any presets for AcceptPrice. Looked for: {!r}".format(preset_names), err=True, force=True)
            return
        # ----------------------------------------

        source.addFunction(DialogWindow.runPreset, preset_name,
                           content_style="icon", icon_obj=icon, text_args=text_args)

        with source.addRaceTask(2) as (confirm, cancel):
            confirm.addListener(Notificator.onDialogWindowConfirm)
            confirm.addFunction(SystemMonetization.acceptPrice, descr)
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
            if scopeSuccess is not None:
                success.addScope(scopeSuccess)

            fail.addListener(Notificator.onGameStorePayGoldFailed)
            if scopeFail is not None:
                fail.addScope(scopeFail)

            no_money.addListener(Notificator.onGameStoreNotEnoughGold)
            with no_money.addRaceTask(2) as (confirm, cancel):  # wait close window
                confirm.addListener(Notificator.onDialogWindowConfirm)
                cancel.addListener(Notificator.onDialogWindowCancel)

    @staticmethod
    def withdrawGold(num, immediately_save=True):
        _Log("withdrawGold num={}".format(num), optional=True)
        SystemMonetization.storage["gold"].subtractValue(num)
        if immediately_save is True:
            SystemMonetization.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, SystemMonetization.getBalance())
        return True

    @staticmethod
    def addGold(num, immediately_save=True):
        _Log("addGold num={}".format(num), optional=True)
        SystemMonetization.storage["gold"].additiveValue(num)
        if immediately_save is True:
            SystemMonetization.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, SystemMonetization.getBalance())
        return True

    @staticmethod
    def setGold(num, immediately_save=True):
        _Log("set num={}".format(num), optional=True)
        SystemMonetization.storage["gold"].setValue(num)
        if immediately_save is True:
            SystemMonetization.saveData("gold")
        Notification.notify(Notificator.onUpdateGoldBalance, SystemMonetization.getBalance())
        return True

    @staticmethod
    def rollbackCurrency(prod_id=None, component_tag=None):
        _prod_id = None

        if prod_id is not None:
            _prod_id = prod_id
        elif component_tag in SystemMonetization.components:
            _prod_id = SystemMonetization.components[component_tag].getProductId()

        if _prod_id is None:
            return False

        product = MonetizationManager.getProductInfo(_prod_id)
        if product is None:
            return False

        currency = product.getCurrency()
        if currency == "Gold":
            return SystemMonetization.addGold(product.price)
        elif currency == "Energy":
            return SystemMonetization.addEnergy(product.price)

    @staticmethod
    def rollbackGold(prod_id=None, component_tag=None):    # DEPRECATED
        _Log("DEPRECATED warning: `rollbackGold` is deprecated, use `rollbackCurrency` instead", err=True)
        return SystemMonetization.rollbackCurrency(prod_id, component_tag)

    @staticmethod
    def getBalance():
        balance = SystemMonetization.getStorageValue("gold")
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

    @staticmethod
    def _getPossibleRewards():
        rewards = {
            "Gold": SystemMonetization.addGold,
            "Energy": SystemMonetization.addEnergy,
            "EnergyInfinity": SystemMonetization.setInfinityEnergy,
            "DisableInterstitialAds": SystemMonetization.disableInterstitialAds
        }
        return rewards

    @staticmethod
    def sendReward(rew_dict=None, prod_id=None):
        """ sends reward according to custom dict or product reward info. Select one: `rew_dict` or `prod_id`.
            @param rew_dict: dict with reward info, allowed keys:
                "Gold" (adds gold), "Chapter" (unlocks chapter), "SceneUnlock" (unlocks scene),
                "Energy" (adds energy), "DisableInterstitialAds" (disable interstitial adverts)
            @param prod_id: id of product, which has reward info """

        if MonetizationManager.isMonetizationEnable() is False:
            return False

        reward = {}
        if prod_id is not None:
            reward = MonetizationManager.getProductReward(prod_id)
        elif rew_dict is not None:
            reward = rew_dict

        if not (isinstance(reward, dict) and len(reward) > 0):
            if _DEVELOPMENT is True:
                Trace.log("System", 0, "SystemMonetization.sendReward wrong reward dict {!r} (your input: {!r}, id={!r})".format(reward, rew_dict, prod_id))
            return False

        rewards = SystemMonetization._getPossibleRewards()
        for reward_type, arg in reward.items():
            fn = rewards.get(reward_type)
            if callable(fn):
                fn(arg)
            else:
                _Log("Not found reward function for type {!r} (prod_id={!r})".format(reward_type, prod_id), err=True)

        Notification.notify(Notificator.onGameStoreSentRewards, prod_id, reward)
        return True

    @staticmethod
    def addEnergy(energy):
        Notification.notify(Notificator.onEnergyIncrease, energy)

    @staticmethod
    def setInfinityEnergy(code):
        if code == 1:
            Notification.notify(Notificator.onEnergySet, "inf")
        else:
            _Log("Invalid infinity energy code {} - must be 1 to set infinity".format(code), err=True)

    @staticmethod
    def unlockChapter(chapter_id):
        Notification.notify(Notificator.onChapterSelectionBlock, chapter_id, False)
        _Log("unlock chapter '{}'".format(chapter_id))

        if MonetizationManager.getGeneralSetting("CompleteProductsOnChapterUnlock", True) is False:
            return

        for product in MonetizationManager.getProductsInfo().values():
            reward_chapter_id = product.reward.get("Chapter")
            if reward_chapter_id != chapter_id:
                continue
            if SystemMonetization.isProductPurchased(product.id) is False:
                SystemMonetization.addStorageListValue("purchased", product.id)
                _Log("autosave product {!r} - chapter {!r} is already unlocked!".format(
                    product.id, chapter_id), optional=True)

    @staticmethod
    def disableInterstitialAds(*args):
        if MonetizationManager.isMonetizationEnable() is False:
            return
        if SystemManager.hasSystem("SystemAdvertising") is False:
            return
        #SystemAdvertising = SystemManager.getSystem("SystemAdvertising")
        #SystemAdvertising.disableForever()
        _Log("disabled interstitial ads", optional=True)

    # --- Advertisements -----------------------------------------------------------------------------------------------

    @staticmethod
    def updateAvailableAds():
        if MonetizationManager.isMonetizationEnable() is False:
            return

        """ resets `today_viewed_ads` if `last_viewed_date` is different from today date"""
        today_date = SystemMonetization.__getTodayDate()

        for ad_name in MonetizationManager.getAdvertNames("Rewarded"):
            storage_keys = SystemMonetization.__getAdvertStorageKeys(ad_name)
            last_viewed_date = storage_keys["last_viewed_date"]
            today_viewed_ads = storage_keys["today_viewed_ads"]

            if SystemMonetization.storage[last_viewed_date].isEqual(today_date) is True:
                continue  # reset today viewed ads only if it's another day
            SystemMonetization.storage[today_viewed_ads].setValue(0)
            SystemMonetization.saveData(today_viewed_ads)

            SystemMonetization._updateAdvertCounterText(ad_name)
            Notification.notify(Notificator.onAvailableAdsNew, ad_name)

    @staticmethod
    def __getTodayDate():
        """ :return: 'YEAR/MONTH/DAY' """
        time = Mengine.getLocalDateStruct()
        today_date = "{}/{}/{}".format(time.year, time.month, time.day)
        return today_date

    @staticmethod
    def __getAdvertStorageKeys(ad_name="Rewarded"):
        """ returns storage keys for adverts """
        # deprecated keys: "lastViewedAdDate", "todayViewedAds"
        return {
            "last_viewed_date": "LastViewed{}AdDate".format(ad_name),
            "today_viewed_ads": "TodayViewed{}Ads".format(ad_name),
        }

    @staticmethod
    def isAdsEnded(AdUnitName="Rewarded"):
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        """ :return: True if ads ended """
        today_viewed_ads = SystemMonetization.getAdvertStorageKey(AdUnitName, "today_viewed_ads")

        viewed_ads = SystemMonetization.getStorageValue(today_viewed_ads)
        ads_per_day = MonetizationManager.getGeneralSetting("AdsPerDay")    # todo: make it unique for each ad unit
        return viewed_ads >= ads_per_day

    @staticmethod
    def _initAdvertCounterText():
        text_id = MonetizationManager.getGeneralSetting("AdvertGlobalTextId", "ID_GLOBAL_ADVERT_COUNTER")

        for ad_name in MonetizationManager.getAdvertNames("Rewarded"):
            Mengine.setTextAlias(ad_name, ALIAS_GLOBAL_ADVERT_COUNTER, text_id)
            Mengine.setTextAliasArguments(ad_name, ALIAS_GLOBAL_ADVERT_COUNTER, 0, 0)

    @staticmethod
    def _updateAdvertCounterText(ad_name):
        today_viewed_ads = SystemMonetization.getAdvertStorageKey(ad_name, "today_viewed_ads")

        viewed_ads = int(SystemMonetization.getStorageValue(today_viewed_ads))
        max_ads = MonetizationManager.getGeneralSetting("AdsPerDay")    # todo: make it unique for each ad unit
        Mengine.setTextAliasArguments(ad_name, ALIAS_GLOBAL_ADVERT_COUNTER, viewed_ads, max_ads)

    # callbacks

    @staticmethod
    def _onAdUserRewarded(ad_type, ad_name, params):  # react on showAd()
        _Log("onAdvertisementReward type: {} name: {} params: {}".format(ad_type, ad_name, params))

        advert_product = MonetizationManager.findProduct(lambda pr: pr.currency == "Advert" and pr.name == ad_name)
        if advert_product is None:
            Trace.log("System", 0, "Not found advert product for ad {!r} (set product currency to 'Advert' and name to {!r})".format(ad_name, ad_name))
            return False

        storage_keys = SystemMonetization.__getAdvertStorageKeys(ad_name)
        last_viewed_date = storage_keys["last_viewed_date"]
        today_viewed_ads = storage_keys["today_viewed_ads"]

        last_date = SystemMonetization.getStorageValue(last_viewed_date)
        today_date = SystemMonetization.__getTodayDate()
        SystemMonetization.storage[last_viewed_date].setValue(today_date)

        if SystemMonetization.isAdsEnded(ad_name) is False:
            SystemMonetization.sendReward(prod_id=advert_product.id)

            if last_date == today_date:
                SystemMonetization.storage[today_viewed_ads].additiveValue(1)
            else:  # imagine if today was 0 viewed ads, and we increase it by 1
                SystemMonetization.storage[today_viewed_ads].setValue(1)

        SystemMonetization.saveData(today_viewed_ads, last_viewed_date, "gold")
        SystemMonetization._updateAdvertCounterText(ad_name)

        if SystemMonetization.isAdsEnded(ad_name) is True:
            Notification.notify(Notificator.onAvailableAdsEnded, ad_name)
            _Log("onAvailableAdsEnded {!r}".format(ad_name))

        return False

    # --- Check components ---------------------------------------------------------------------------------------------

    @staticmethod
    def shouldAcceptPrice():
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        return MonetizationManager.getGeneralSetting("ShouldAcceptPrice", True)

    @staticmethod
    def isGameStoreEnable():
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        if GroupManager.hasGroup(SystemMonetization.game_store_name) is False:
            return False
        demon = DemonManager.getDemon(SystemMonetization.game_store_name)
        return demon.isStoreEnable()

    @staticmethod
    def isComponentEnable(name):
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        if name not in SystemMonetization.components:
            return False

        b_store = SystemMonetization.isGameStoreEnable() is True
        b_component = SystemMonetization.components[name].isEnable() is True

        return all([b_store, b_component])

    @staticmethod
    def getComponent(name):
        if SystemMonetization.hasComponent(name) is False:
            return None
        return SystemMonetization.components[name]

    @staticmethod
    def hasComponent(name):
        return name in SystemMonetization.components

    @staticmethod
    def isProductPurchased(prod_id):
        if _DEVELOPMENT is True:
            if isinstance(prod_id, str) is False:
                Trace.log("System", 0, "Wrong product id type {}, must be str".format(type(prod_id)))
                return False

        if MonetizationManager.isMonetizationEnable() is False:
            return False

        items = SystemMonetization.getStorageListValues("purchased")
        if items is None:
            return False

        is_purchased = str(prod_id) in items

        if _DEVELOPMENT is True:
            _Log("  isProductPurchased {} in {}: {}".format(prod_id, items, is_purchased), optional=True)

        return is_purchased

    @staticmethod
    def isProductGroupPurchased(group_id):
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        items = SystemMonetization.getStorageListValues("PurchasedProductGroups")
        if items is None:
            return False

        is_purchased = str(group_id) in items
        return is_purchased

    @staticmethod
    def isPurchaseDelayed(prod_id):
        if MonetizationManager.isMonetizationEnable() is False:
            return False

        return prod_id in SystemMonetization._session_delayed_products

    # --- Observers ----------------------------------------------------------------------------------------------------

    def setupObservers(self):
        self.addObserver(Notificator.onSelectAccount, self._onSelectAccount)

        # payment
        self.addObserver(Notificator.onProductAlreadyOwned, self._onProductAlreadyOwned)
        self.addObserver(Notificator.onPaySuccess, self._onPaySuccess)
        self.addObserver(Notificator.onDelayPurchased, self._onDelayPurchased)
        self.addObserver(Notificator.onReleasePurchased, self._onReleasePurchased)
        self.addObserver(Notificator.onPayFailed, self._onPayFailed)
        self.addObserver(Notificator.onGameStorePayGold, self._onPayGold)

        # other
        self.addObserver(Notificator.onAdUserRewarded, self._onAdUserRewarded)
        self.addObserver(Notificator.onAppRated, self._onAppRated)

        self._setupObservers()

    def _setupObservers(self):
        """ override it for specific behaviour """
        pass

    def _onSelectAccount(self, account_id):
        self._saveSessionPurchases()

        self._initAdvertCounterText()
        self.updateAvailableAds()
        return False

    @staticmethod
    def _onChangeGold(account_id, value):
        """ `gold` observer in addExtraAccountSettings """
        balance = SystemMonetization.getBalance()
        Notification.notify(Notificator.onUpdateGoldBalance, balance)

    def _onAppRated(self):
        rate_reward = MonetizationManager.getGeneralSetting("RateUsReward")
        if rate_reward is not None:
            self.sendReward(rew_dict={"Gold": int(rate_reward)})
            return True

        rate_product = MonetizationManager.getGeneralProductInfo("RateUsProductID")
        if rate_product is not None:
            self.sendReward(prod_id=rate_product.id)
            return True

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

        SystemAnalytics.addAnalytic("earn_currency_by_purchase", Notificator.onGameStoreSentRewards,
                                    service_key="earn_currency", params_method=_cbEarnCurrency,
                                    check_method=lambda _, rewards: 'Gold' in rewards or 'Energy' in rewards)
        SystemAnalytics.addAnalytic("spent_currency_gold", Notificator.onGameStorePayGoldSuccess,
                                    service_key="spent_currency",
                                    params_method=lambda gold, descr: {'amount': gold, 'description': descr, 'name': 'gold'})

        # `onGiftExchangeRedeemResult` notification identity is located in HOPA framework !!!!!
        if Notification.validateIdentity("onGiftExchangeRedeemResult") is True:
            SystemAnalytics.addAnalytic("got_promocode_reward", Notificator.onGiftExchangeRedeemResult, None,
                                    lambda label, result: {'type': str(label), 'result': str(result)})
        SystemAnalytics.addAnalytic("got_purchase_reward", Notificator.onGameStoreSentRewards,
                                    lambda prod_id, *_: prod_id != advert_prod_id, _cbSentRewardParams)
        SystemAnalytics.addAnalytic("got_ad_reward", Notificator.onGameStoreSentRewards,
                                    lambda prod_id, *_: prod_id == advert_prod_id,
                                    lambda prod_id, rewards: rewards.copy())
        SystemAnalytics.addAnalytic("not_enough_gold", Notificator.onGameStoreNotEnoughGold, None,
                                    lambda value, descr: {"not_enough_value": value, "description": descr})

        def _cbAdsEnded(ad_name):
            storage_keys = SystemMonetization.__getAdvertStorageKeys(ad_name)
            today_viewed_ads = storage_keys["today_viewed_ads"]
            last_viewed_date = storage_keys["last_viewed_date"]
            return {
                "today_viewed_ads": SystemMonetization.getStorageValue(today_viewed_ads),
                "fingerprint": SystemMonetization.getStorageValue(last_viewed_date)
            }
        SystemAnalytics.addAnalytic("rewarded_ads_reached_limit", Notificator.onAvailableAdsEnded, None, _cbAdsEnded)

    @staticmethod
    def __initStorage():
        storage = {
            "gold": SecureValue("gold", int(MonetizationManager.getGeneralSetting("StartBalance", 0))),
            "skippedMGs": SecureStringValue("skippedMGs", ""),
            "acceptPrice": SecureStringValue("acceptPrice", ""),
            "purchased": SecureStringValue("purchased", ""),  # "{}, "...
            "PurchasedProductGroups": SecureStringValue("PurchasedProductGroups", "")
        }
        for ad_name in MonetizationManager.getAdvertNames("Rewarded"):
            storage_keys = SystemMonetization.__getAdvertStorageKeys(ad_name)
            today_viewed_ads = storage_keys["today_viewed_ads"]
            last_viewed_date = storage_keys["last_viewed_date"]
            storage[today_viewed_ads] = SecureValue(today_viewed_ads, 0)
            storage[last_viewed_date] = SecureStringValue(last_viewed_date, "")

        SystemMonetization.storage = storage

    def _setupParams(self):
        SystemMonetization.__initStorage()

        SystemMonetization._setDebugCurrency()

        for name, ComponentType in MonetizationManager.getComponentsType().items():
            component = ComponentType()
            if component.initialize(self) is True:
                component.run()
                SystemMonetization.components[component.component_id] = component

    @staticmethod
    def _setDebugCurrency():
        MonetizationManager.setDebugCurrency()

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

        for product_id in SystemMonetization._session_purchased_products:
            if SystemMonetization.isProductPurchased(product_id) is True:
                continue
            Notification.notify(Notificator.onPaySuccess, product_id)

        SystemMonetization._session_purchased_products = []

    @staticmethod
    def addStorageListValue(key, value):
        raw_items = SystemMonetization.getStorageValue(key)
        if raw_items is None:
            return

        items = raw_items.strip(", ").split(", ")

        if str(value) in items:
            _Log("value {!r} is already in '{}': {}".format(value, key, items), err=True, optional=True)
            return

        raw_items += "{}, ".format(str(value))
        SystemMonetization.storage[key].setValue(raw_items)

        SystemMonetization.saveData(key)

        _Log("successfully append {!r} to '{}' list: {}".format(value, key, raw_items), optional=True)

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

    @staticmethod
    def getAdvertStorageKey(ad_name, lookup_value):
        storage_keys = SystemMonetization.__getAdvertStorageKeys(ad_name)
        lookup_storage_key = storage_keys[lookup_value]
        return lookup_storage_key

    # --- storage interaction

    @staticmethod
    def saveData(*keys):
        """ Apply Mengine.saveAccounts
            :param keys: str keys, they must be in storage.
                if 0 keys: saves all values from storage
        """

        if len(keys) == 0:
            _Log("Saver: save all data on device...", optional=True)
            for key, value in SystemMonetization.storage.items():
                save = value.getSave()
                Mengine.changeCurrentAccountSetting(key, unicode(save))

        else:
            for key in keys:
                if key not in SystemMonetization.storage:
                    _Log("Saver: storage key {!r} not found".format(key), err=True, optional=True)
                    continue
                save = SystemMonetization.storage[key].getSave()
                _Log("Saver: save {!r} on device... [{}]".format(key, save), optional=True)
                Mengine.changeCurrentAccountSetting(key, unicode(save))

        Mengine.saveAccounts()
        _Log("Saver: save complete...")

    @staticmethod
    def addExtraAccountSettings(account_id, isGlobal):
        if isGlobal is True:
            return

        observers = {
            # add here key from storage and function that will be called if setting would be changed
            "gold": SystemMonetization._onChangeGold,
        }

        for key in SystemMonetization.storage.keys():
            fn = observers.get(key)
            Mengine.addCurrentAccountSetting(key, u'None', fn)

        # calls only on Create Account

        _Log("added storage settings to account {} params".format(account_id), optional=True)

    @staticmethod
    def loadData():
        if SystemMonetization.__isActive() is False:
            return
        _Log("restore storage from USER saves...")

        for key in SystemMonetization.storage.keys():
            value_save = str(Mengine.getCurrentAccountSetting(key))
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

        save = {
            "components": self.saveComponents()
        }

        return save

    def _onLoad(self, save):
        if SystemMonetization.__isActive() is False:
            return

        # load saves from account params
        self.loadData()
        self.loadComponents(save.get("components", {}))

        return

    def saveComponents(self):
        save_data = {}
        for name, component in self.components.items():
            save = component.save()
            save_data[name] = save
        return save_data

    def loadComponents(self, save_data):
        for name, save in save_data.items():
            component = self.components.get(name)
            if component is None:
                _Log("[loadComponents] ERROR while load component {!r} saves: not found in components list {}."
                     " Please check your save files and game configurations.".format(
                      name, self.components.keys() if _DEVELOPMENT else len(self.components)), err=True, force=True)
                continue
            component.load(save)

    # --- DevToDebug ---------------------------------------------------------------------------------------------------

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if self.__isActive() is False:
            return
        if Mengine.hasDevToDebugTab("Monetization") is True:
            return

        tab = Mengine.addDevToDebugTab("Monetization")

        # buttons

        for ad_name in MonetizationManager.getAdvertNames("Rewarded"):
            w_show_ad = Mengine.createDevToDebugWidgetButton("show_ad_{}".format(ad_name))
            w_show_ad.setTitle("Show {!r} ad with current provider".format(ad_name))
            w_show_ad.setClickEvent(self.showAd, "Rewarded", ad_name)
            tab.addWidget(w_show_ad)

        w_upd_ads = Mengine.createDevToDebugWidgetButton("update_ads")
        w_upd_ads.setTitle("Update available ads")
        w_upd_ads.setClickEvent(self.updateAvailableAds)
        tab.addWidget(w_upd_ads)

        # command lines

        def _addGold(text):
            gold = int(text)
            self.addGold(gold)

        w_add = Mengine.createDevToDebugWidgetCommandLine("add_gold")
        w_add.setTitle("Add gold")
        w_add.setPlaceholder("Input here positive integer")
        w_add.setCommandEvent(_addGold)
        tab.addWidget(w_add)

        def _withdrawGold(text):
            gold = int(text)
            self.withdrawGold(gold)

        w_withdraw = Mengine.createDevToDebugWidgetCommandLine("withdraw_gold")
        w_withdraw.setTitle("Withdraw gold")
        w_withdraw.setPlaceholder("Input here positive integer")
        w_withdraw.setCommandEvent(_withdrawGold)
        tab.addWidget(w_withdraw)

        def _setGold(text):
            gold = int(text)
            self.setGold(gold)

        w_set = Mengine.createDevToDebugWidgetCommandLine("set_gold")
        w_set.setTitle("Set gold")
        w_set.setPlaceholder("Input here positive integer")
        w_set.setCommandEvent(_setGold)
        tab.addWidget(w_set)

        def _sendReward(product_id):
            self.sendReward(prod_id=product_id)

        w_send_reward = Mengine.createDevToDebugWidgetCommandLine("send_reward")
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
            Notification.notify(Notificator.onGameStorePayGold, gold, descr)

        w_pay_gold = Mengine.createDevToDebugWidgetCommandLine("pay_gold")
        w_pay_gold.setTitle("Pay gold")
        w_pay_gold.setPlaceholder("Syntax: <gold_num> [descr]")
        w_pay_gold.setCommandEvent(_payGold)
        tab.addWidget(w_pay_gold)

        w_pay = Mengine.createDevToDebugWidgetCommandLine("pay")
        w_pay.setTitle("Payment with `{}`".format(PaymentProvider.getName()))
        w_pay.setPlaceholder("Syntax: <product_id>")
        w_pay.setCommandEvent(self.pay)
        tab.addWidget(w_pay)

        def _showSpecialPromo(special_prod_id, demon_name="SpecialPromo"):
            if DemonManager.hasDemon(demon_name) is False:
                _Log("[DevToDebug] {} demon not found".format(demon_name), err=True)
                return
            demon = DemonManager.getDemon(demon_name)
            _Log("[DevToDebug] run {} {}".format(demon_name, special_prod_id))
            demon.run(special_prod_id)

        w_special_promo = Mengine.createDevToDebugWidgetCommandLine("show_special_promo")
        w_special_promo.setTitle("Show special promotion")
        w_special_promo.setPlaceholder("Syntax: <product_id>")
        w_special_promo.setCommandEvent(_showSpecialPromo, "SpecialPromotion")
        tab.addWidget(w_special_promo)

        w_limited_promo = Mengine.createDevToDebugWidgetCommandLine("show_limited_promo")
        w_limited_promo.setTitle("Show limited promotion")
        w_limited_promo.setPlaceholder("Syntax: <product_id>")
        w_limited_promo.setCommandEvent(_showSpecialPromo, "LimitedPromo")
        tab.addWidget(w_limited_promo)

        # info texts

        def _getSettingsWidgetTitle():
            title = "**Monetization settings**"
            title += "".join(["\n* {}: `{}`".format(key, val)
                              for key, val in MonetizationManager.getGeneralSettings().items()])
            return title

        w_settings_descr = Mengine.createDevToDebugWidgetText("monetization_settings_descr")
        w_settings_descr.setText(_getSettingsWidgetTitle)
        tab.addWidget(w_settings_descr)

        def _updateSetting(text):
            params = text.split(" ")
            if len(params) != 2:
                return

            all_settings = MonetizationManager.getGeneralSettings()
            setting, raw_value = params

            if setting not in all_settings:
                _Log("[DevToDebug] setting {!r} not found".format(setting), err=True)
                return

            cast_types = [int, float, bool]
            for type_ in cast_types:
                prefix = "({})".format(type_.__name__)
                if raw_value.startswith(prefix) is True:
                    value = type_(raw_value[len(prefix):])
                    break
            else:
                # if no cast prefix found
                value = raw_value

            _Log("[DevToDebug] changed setting {!r} from {!r} to {!r}".format(setting, all_settings[setting], value))
            all_settings[setting] = value

        w_settings = Mengine.createDevToDebugWidgetCommandLine("change_settings")
        w_settings.setTitle("Change settings (from list above) | cast prefixes: (bool) (int) (float)")
        w_settings.setPlaceholder("Syntax: <setting_name> [cast_prefix]<new_value>")
        w_settings.setCommandEvent(_updateSetting)
        tab.addWidget(w_settings)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        if Mengine.hasDevToDebugTab("Monetization") is True:
            Mengine.removeDevToDebugTab("Monetization")