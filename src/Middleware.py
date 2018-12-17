# -*- coding: utf-8 -*-

class Middleware:
    def before_request(self, req, crawler):
        pass

    def after_request(self, res, crawler):
        pass

    def request_exception(self, req, error, crawler):
        pass

class UserAgentMiddleware(Middleware):
    def before_request(self, req, crawler):
        headers = getattr(req, 'headers', {})
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        })
        req.headers = headers

class ProxiesMiddleware(Middleware):
    def __init__(self, proxies = None):
        self.proxies = proxies or {
            'http': 'http://127.0.0.1:1080',
            'https': 'http://127.0.0.1:1080'
        }

    def before_request(self, req, crawler):
        req.proxies = self.proxies

class ShowUrlMiddleware(Middleware):
    def before_request(self, req, crawler):
        print('[+] request for: ', req.url)
