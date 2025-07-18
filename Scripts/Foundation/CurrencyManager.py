from Foundation.DefaultManager import DefaultManager


class CurrencyManager(object):
    s_current_currency = None

    CURRENCY_TEXTS_IDS = {  # find them in Framework Texts.xml
        "ID_CURRENCY_DOLLAR": ["USD"],
        "ID_CURRENCY_POUND": ["GBP"],
        "ID_CURRENCY_EURO": ["EUR"],
        "ID_CURRENCY_HRYVNIA": ["UAH"],
        "ID_CURRENCY_YUAN": ["CNY", "JPY"],
    }

    @staticmethod
    def addCurrencyCode(currency_code, text_id):
        CurrencyManager.CURRENCY_TEXTS_IDS.setdefault(text_id, [])
        if currency_code in CurrencyManager.CURRENCY_TEXTS_IDS[text_id]:
            return
        CurrencyManager.CURRENCY_TEXTS_IDS[text_id].append(currency_code)

    @staticmethod
    def setCurrentCurrencyCode(currency_code):
        """ set current ISO 4217 currency code. `currency_code` must be str! """
        if currency_code is None:
            CurrencyManager.s_current_currency = None
            return True
        if isinstance(currency_code, str) is False:
            Trace.log("Manager", 0, "setCurrentCurrencyCode {!r} must be str, not {}"
                      .format(currency_code, type(currency_code)))
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

        if DefaultManager.getDefaultBool("MonetizationShowCurrencySymbol", True) is False:
            return cur_currency

        currency_text_ids = CurrencyManager._getCurrencyTextIds()
        symbol_text_id = currency_text_ids.get(cur_currency, None)

        if symbol_text_id is None:
            if code_if_none is True:
                return cur_currency
            return None

        if Mengine.existText(symbol_text_id) is False:
            if _DEVELOPMENT is True:
                Trace.log("Manager", 1, "textId {} not found for currency {}".format(symbol_text_id, cur_currency))
            if code_if_none is True:
                return cur_currency
            return None

        if only_text_id is True:
            return symbol_text_id

        symbol = Mengine.getTextFromId(symbol_text_id)
        return symbol

    @staticmethod
    def setDebugCurrency():
        if _DEVELOPMENT is False:
            return

        default_currency_code = Mengine.getConfigString("Monetization", "DebugCurrencyCode", "USD")
        if default_currency_code.lower() != "none":
            CurrencyManager.setCurrentCurrencyCode(default_currency_code)

    @staticmethod
    def updateCurrencyText(env, alias, text_id, currency_type="symbol"):
        """ @param currency_type: "symbol" | "code" """
        if currency_type == "symbol":
            currency = CurrencyManager.getCurrentCurrencySymbol() or ""
        elif currency_type == "code":
            currency = CurrencyManager.getCurrentCurrencyCode()
        else:
            Trace.log("Manager", 0, "Unknown currency_type {}".format(currency_type))
            return

        Mengine.setTextAlias(env, alias, text_id)
        Mengine.setTextAliasArguments(env, alias, currency)
