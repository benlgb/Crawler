# -*- coding: utf-8 -*-

class Middleware:
    def before_request(self, req, controller, crawler):
        pass

    def after_request(self, res, controller, crawler):
        pass

    def request_exception(self, req, error, controller, crawler):
        pass

class UserAgentMiddleware(Middleware):
    def before_request(self, req, **kwargs):
        headers = getattr(req, 'headers', {})
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        })
        req.headers = headers

class ProxyMiddleware(Middleware):
    def __init__(self, proxies = None):
        self.proxies = proxies or {
            'http': 'http://127.0.0.1:1080',
            'https': 'http://127.0.0.1:1080'
        }

    def before_request(self, req, **kwargs):
        req.proxies = self.proxies

class ProxyAsyncMiddleware(Middleware):
    def __init__(self, proxy = None):
        self.proxy = proxy or 'http://127.0.0.1:1080'

    def before_request(self, req, **kwargs):
        req.proxy = self.proxy

class ShowUrlMiddleware(Middleware):
    def before_request(self, req, controller, **kwargs):
        if controller._TYPE == 'ASYNC':
            print('[+] %d controller request for: %s' % (controller.number, req.url))
        else:
            print('[+] controller request for: ', req.url)
