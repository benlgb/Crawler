# -*- coding: utf-8 -*-

class Middleware:
    def before_request(self, req):
        pass

    def after_request(self, res):
        pass

    def request_exception(self, req, error):
        pass

class UserAgentMiddleware(Middleware):
    def before_request(self, req):
        headers = getattr(req, 'headers', {})
        headers.update   ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        })
        req.headers = headers