# -*- coding: utf-8 -*-

'''
请求响应基本结构
'''

from bs4 import BeautifulSoup

def cb(*args, **kwargs):
    pass

class Request:
    def __init__(self, url, method='get', cb=cb, **kwargs):
        self.url = url
        self.method = method.lower()
        self.cb = cb
        self.kwargs = kwargs

    def __getattr__(self, attr):
        return self.kwargs[attr]

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

    def soup(self):
        return BeautifulSoup(self.content, 'lxml')