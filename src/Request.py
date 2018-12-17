# -*- coding: utf-8 -*-

'''
请求响应基本结构
'''

from bs4 import BeautifulSoup

def cb(*args, **kwargs):
    pass

class Request:
    def __init__(self, url, method='get', cb=cb, item=None, **kwargs):
        self.url = url
        self.method = method.lower()
        self.cb = cb
        self.item = item
        self.kwargs = kwargs

    def __getattr__(self, attr):
        try:
            return self.kwargs[attr]
        except KeyError:
            msg = '\'Request\' object has no attribute \'%s\''
            raise AttributeError(msg % attr)

    def __setattr__(self, attr, value):
        if attr in ['url', 'method', 'cb', 'item', 'kwargs']:
            object.__setattr__(self, attr, value)
        else:
            self.kwargs[attr] = value

class Response:
    def __init__(self, res, req):
        self.res = res
        self.req = req

    def __getattr__(self, attr):
        try:
            return getattr(self.res, attr)
        except AttributeError:
            return getattr(self.req, attr)
    
    def cb(self):
        return self.req.cb(self)