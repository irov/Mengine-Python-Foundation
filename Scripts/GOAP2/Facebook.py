from Manager import Manager

class Facebook(Manager):
    token = 'EAAO2ZCgDXgLUBAA2gPRnW7JvOUdnTR19MwZBWfogElf77hqXMKLraVxRq1wmEGUqUQkYL7E9Slhjp022XLz3byTxV858WsJ7fqsxvCeN6h8kmIzP0LcgglnjFBbZBWxd8g8C6n8SE0pRbPaWjCX9ObG6RQSpeWSTvtHcyaWoYT1WteADQSYHhCfGZAzUDawZD'
    clientId = ''
    redirectUri = ''
    client_ip = None

    def __init__(self):
        self.token = ''
        self.scope = []
        self.graphAPIurl = 'https://graph.facebook.com/v2.9/me'
        pass

    @staticmethod
    def _onInitialize(*args):
        # if _PLUGINS.get("Facebook", False) is True:
        #     Menge.androidMethod("Facebook", "initialize")
        Facebook.clientId = Menge.getConfigString('Facebook', 'clientId', '1045626982203573')
        Facebook.redirectUri = Menge.getConfigString('Facebook', 'redirectUri', 'http://localhost:8888/token')
        pass

    @staticmethod
    def setUser(user_token):
        Facebook.token = user_token

    @staticmethod
    def send_post_message(data):
        if data['message'] is None:
            print
            'Not all arguments are presented'
            return

        if Facebook.token is None:
            print
            'Authorize before posting'
            return

        data = Facebook.removeNone(data)
        data['access_token'] = Facebook.token
        post_url = 'https://graph.facebook.com/v2.9/me/feed'

        def cb(num, data, status, code, bool):
            pass
        data['message'] += "\n(Test msg from Menge)"
        Menge.postMessage(post_url, data, cb)
        pass

    @staticmethod
    def get_users_data(data, cb):
        if Facebook.token is None:
            print
            'Authorize before posting'
            return

        data['access_token'] = Facebook.token
        get_url = 'https://graph.facebook.com/v2.9/me'
        Menge.getMessage(Facebook.bad_convert(get_url, data), cb)
        pass

    @staticmethod
    def auth_user(data):
        data['client_id'] = Facebook.clientId
        data['redirect_uri'] = Facebook.redirectUri + '?ip=' + Facebook.client_ip
        auth_url = 'https://www.facebook.com/v2.9/dialog/oauth'
        print
        unicode(Facebook.bad_convert(auth_url, data), "utf-8")
        Menge.openUrlInDefaultBrowser(unicode(Facebook.bad_convert(auth_url, data), "utf-8"))
        pass

    @staticmethod
    def removeNone(data):
        new_data = dict()
        for key, value in data.iteritems():
            if value is not None:
                new_data[key] = value
        return new_data

    @staticmethod
    def bad_convert(post_url, data):
        post_url += '?'
        for key, value in data.iteritems():
            if value is not None:
                post_url += key + '=' + value + '&'
            pass
        post_url = post_url[:-1]
        return post_url

    pass