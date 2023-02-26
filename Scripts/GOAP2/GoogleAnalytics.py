import re

from Manager import Manager

class GoogleAnalytics(Manager):

    def __init__(self, tid="UA-98225798-1", v='1'):
        self.url_collect = 'http://www.google-analytics.com/collect'
        self.version = v
        self.tid = tid
        self.min_params = ['cid', 't']
        pass

    version = ''
    tid = ''
    TimeDimension = ''
    TimeMetric = ''
    @staticmethod
    def _onInitialize(*args):
        GoogleAnalytics.version = Menge.getConfigString('GoogleAnalytics', 'Version', '1')
        GoogleAnalytics.tid = Menge.getConfigString('GoogleAnalytics', 'Tid', 'UA-98225798-1')
        GoogleAnalytics.TimeDimension = Menge.getConfigString('GoogleAnalytics', 'TimeDimension', 'dimension1')
        GoogleAnalytics.TimeMetric = Menge.getConfigString('GoogleAnalytics', 'TimeMetric', 'metric1')
        pass

    @staticmethod
    def send_analytics(params):
        action = params.get('action', None)
        category = params.get('category', None)
        type = params.get('type', 'event')
        label = params.get('label', None)
        value = params.get('value', None)
        cid = params.get('clientID', None)
        cDict = params.get('client_definition', {})

        data = dict(cid=cid, ec=category, ea=action, t=type, el=label, ev=value, )
        # remove empty fields
        new_dict = {}
        for key, value in data.iteritems():
            if value is not None:
                new_dict[key] = value
        # check min count of parameters
        for param in ['cid', 't']:
            if param not in new_dict.keys():
                print
                'Not all parameters are present'
                print
                new_dict
                return
        # set default param
        new_dict['v'] = GoogleAnalytics.version
        new_dict['tid'] = GoogleAnalytics.tid
        url_collect = 'http://www.google-analytics.com/collect'
        for key, value in cDict.iteritems():
            list_d = re.findall("dimension(\d+)", key)
            if len(list_d) == 1:
                new_dict['cd{}'.format(list_d[0])] = value

            list_m = re.findall("metric(\d+)", key)
            if len(list_m) == 1:
                new_dict['cm{}'.format(list_m[0])] = value
        # send analytics

        def cb(*args):
            # print "-GoogleAnalytics-cb-"
            # print "1 '{}'".format(one)
            # print "2 '{}'".format(two)
            # print "3 '{}'".format(three)
            # print "4 '{}'".format(four)
            pass
        msg = GoogleAnalytics.bad_convert(url_collect, new_dict)

        # debug
        # print "send_analytics:", url_collect, new_dict, msg

        Menge.getMessage(msg, cb)
        pass

    def change_params(self, **data):
        # change version of google analytics or tid
        param = data.get('v')
        if param is not None:
            self.version = param
        param = data.get('tid')
        if param is not None:
            self.tid = param
        pass

    @staticmethod
    def bad_convert(post_url, data):
        post_url += '?'
        for key, value in data.iteritems():
            if value is not None:
                post_url += key + '=' + str(value) + '&'
            pass
        post_url = post_url[:-1]
        print
        'Look at my URL \n', post_url, '\n is It Cool?'
        return post_url
    pass